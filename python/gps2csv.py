from helper_functions.mcap_tools import read_mcap
from helper_functions.quaternion_tools import quaternion_to_euler
from glob import glob
import csv
import os 

def gps2csv(root:str, topic:str="/current_pose") -> None:
    """
    Convert GPS data from .mcap files to .csv format.

    Args:
        root (str): The root directory containing the .mcap files.

    Returns:
        None
    """
    files = glob(f'{root}/bags/**/*.mcap')

    if not os.path.exists(f'{root}/csv'):
        os.mkdir(f'{root}/csv')

    file_count = len(files)
    finished_file_counter = 0

    for input in files:
        with open(f'{root}/csv/{os.path.splitext(os.path.basename(input))[0]}_gps.csv', 'w') as file:
            writert = csv.writer(file)
            writert.writerow(['t', 'x', 'y', 'z', 'roll', 'pitch', 'yaw'])

            t0 = 0

            for tp, msg, timestamp in read_mcap(input, topics=[topic]):
                t0 = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
                break

            for tp, msg, timestamp in read_mcap(input, topics=[topic]):
                t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9 - t0
                
                writert.writerow([t, msg.pose.position.x, msg.pose.position.y, msg.pose.position.z] + quaternion_to_euler(msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w))
        
        finished_file_counter += 1
        print(f'{finished_file_counter}/{file_count}\t{os.path.split(input)[-1]}')
