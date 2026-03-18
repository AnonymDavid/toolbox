import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from helper_functions.mcap_tools import read_mcap, msg2dict, get_mcap_topics
from helper_functions.quaternion_tools import quaternion_to_euler
from glob import glob
import csv
from typing import List, Tuple, Dict
from dataclasses import dataclass


def bag2csv(source:str, topic:str, output_folder:str="csv", stamp_to_seconds:bool=False, quaternion_to_rpy:bool=False, topic_in_header:bool=False, verbose:bool=True) -> None:
    """
    Convert MCAP files to CSV format.

    Args:
        source (str): The path to the MCAP file or directory containing MCAP files.
        topic (str): The topic name to extract from the bag file(s). If nothing is given, every topic will be exported to different files.
        output_folder (str, optional): The folder to save the generated CSV file(s) relative to source. Defaults to "csv".
        stamp_to_seconds (bool, optional): Convert timestamps to seconds. Defaults to False.
        quaternion_to_rpy (bool, optional): Convert quaternion values to roll-pitch-yaw angles. Defaults to False.
        topic_in_header (bool, optional): Include the topic name in the CSV header. Defaults to False.
        verbose (bool, optional): Print progress information. Defaults to True.
    """

    @dataclass
    class TimestampObject:
        sec_idx:int
        nsec_idx:int

    @dataclass
    class QuaternionObject:
        x_idx:int
        y_idx:int
        z_idx:int
        w_idx:int
    
    if source.endswith('.mcap'):
        if not os.path.exists(source):
            raise ValueError("The source file does not exist.")
        
        files = [source]

        sourceDir = os.path.dirname(os.path.abspath(source))
    elif os.path.isdir(source):
        files = glob(f'{source}/**/*.mcap', recursive=True)

        sourceDir = os.path.abspath(source)
    else:
        raise ValueError("Invalid source. Must be a .mcap file or a directory containing .mcap files.")
    
    if not os.path.exists(f'{sourceDir}/{output_folder}'):
        os.mkdir(f'{sourceDir}/{output_folder}')


    file_count = len(files)
    file_counter = 0
    timestamps:List[TimestampObject] = []
    quaternions:List[QuaternionObject] = []

    headers = []
    try:
        for input in files:
            topics_to_process = [topic] if len(topic) > 0 else get_mcap_topics(input)
            topic_counter = 0
            topic_count = len(topics_to_process)
            for current_topic in topics_to_process:
                for tp, msg, timestamp in read_mcap(input, topics=[current_topic]):
                    headers = list(msg2dict(msg, pretag=("".join([tp, "/"]) if topic_in_header else "")).keys())
                    break
                
                if stamp_to_seconds:
                    for h in headers:
                        if 'stamp.sec' in h:
                            sec_attr = h
                            nsec_attr = h.replace('stamp.sec', 'stamp.nanosec')

                            tsobj = TimestampObject(headers.index(sec_attr), headers.index(nsec_attr))
                            timestamps.append(tsobj)

                            headers[tsobj.sec_idx] = h.replace('stamp.sec', 'timestamp')
                    for ts in timestamps:
                        headers.pop(ts.nsec_idx)
                
                if quaternion_to_rpy:
                    for h in headers:
                        if 'orientation.x' in h:
                            x_attr = h
                            y_attr = h.replace('orientation.x', 'orientation.y')
                            z_attr = h.replace('orientation.x', 'orientation.z')
                            w_attr = h.replace('orientation.x', 'orientation.w')

                            qobj = QuaternionObject(headers.index(x_attr), headers.index(y_attr), headers.index(z_attr), headers.index(w_attr))
                            quaternions.append(qobj)

                            headers[qobj.x_idx] = h.replace('orientation.x', 'orientation.roll')
                            headers[qobj.y_idx] = h.replace('orientation.x', 'orientation.pitch')
                            headers[qobj.z_idx] = h.replace('orientation.x', 'orientation.yaw')
                    for idxs in quaternions:
                        headers.pop(idxs.w_idx)
                
                filename_in_output_name = f'{os.path.splitext(os.path.basename(input))[0]}' if len(files) > 1 else ""
                out_file_name_base = f'{sourceDir}/{output_folder}/{filename_in_output_name}{current_topic.lstrip("/").replace("/", "_")}'

                with open(f'{out_file_name_base}.csv', 'w') as file:
                    if verbose:
                        print(f'Writing {topic} topic to {out_file_name_base}.csv')
                    
                    writert = csv.writer(file)
                    writert.writerow(headers)
                    
                    for tp, msg, timestamp in read_mcap(input, topics=[current_topic]):
                        msg_attr_list = list(msg2dict(msg, pretag=("".join([tp, "/"]) if topic_in_header else "")).values())

                        if stamp_to_seconds:
                            for ts in timestamps:
                                msg_attr_list[ts.sec_idx] = msg_attr_list[ts.sec_idx] + msg_attr_list[ts.nsec_idx] * 1e-9
                            for ts in timestamps:
                                msg_attr_list.pop(ts.nsec_idx)
                        
                        if quaternion_to_rpy:
                            for idxs in quaternions:
                                (msg_attr_list[idxs.x_idx], msg_attr_list[idxs.y_idx], msg_attr_list[idxs.z_idx]) = quaternion_to_euler(msg_attr_list[idxs.x_idx], msg_attr_list[idxs.y_idx], msg_attr_list[idxs.z_idx], msg_attr_list[idxs.w_idx])
                            for idxs in quaternions:
                                msg_attr_list.pop(idxs.w_idx)
                        
                        writert.writerow(msg_attr_list)

                if verbose:
                    topic_counter += 1
                    print(f'{topic_counter}/{topic_count} topic\t{os.path.split(input)[-1]}')

            if verbose:
                file_counter += 1
                print(f'{file_counter}/{file_count}\t{os.path.split(input)[-1]}')

    except ModuleNotFoundError as err:
        raise ValueError("The topic has unknown message types. Try sourcing the workspace with the message definition and running the script again.\n" + str(err))
