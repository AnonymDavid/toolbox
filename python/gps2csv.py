from mcap_read import read_mcap
from quaternion_functions import quaternion_to_euler
from glob import glob
import csv
import os 

def gps2csv(root:str):
    files = glob(f'{root}/bags/**/*.mcap')

    if not os.path.exists(f'{root}/csv'):
        os.mkdir(f'{root}/csv')

    file_count = len(files)
    finished_file_counter = 0

    tp = "/current_pose"
    for input in files:
        with open(f'{root}/csv/{os.path.splitext(os.path.basename(input))[0][:-4]}_gps.csv', 'w') as file:
            writert = csv.writer(file)
            writert.writerow(['t', 'x', 'y', 'z', 'roll', 'pitch', 'yaw'])

            t0 = 0

            for topic, msg, timestamp in read_mcap(input):
                if topic == tp:
                    t0 = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
                    break

            for topic, msg, timestamp in read_mcap(input):
                if topic == tp:
                    t = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9 - t0
                    
                    writert.writerow([t, msg.pose.position.x, msg.pose.position.y, msg.pose.position.z] + quaternion_to_euler(msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w))
        
        finished_file_counter += 1
        print(f'{finished_file_counter}/{file_count}\t{os.path.split(input)[-1]}')
