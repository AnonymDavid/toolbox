from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
import rosbag2_py
from typing import List


def read_mcap(input_bag: str, topics:List[str]=[]):
    """
    Read messages from a given ROS2 mcap file.

    Usage:
        for topic, msg, timestamp in read_messages(bag_path)

    Args:
        input_bag (str): The path to the input ROS bag file.
        topics (list, optional): A list of topics to filter by. If empty, all topics are returned (default).

    Yields:
        tuple: A tuple containing with the topic name, message, and timestamp.
    """
    reader = rosbag2_py.SequentialReader()
    reader.open(
        rosbag2_py.StorageOptions(uri=input_bag, storage_id="mcap"),
        rosbag2_py.ConverterOptions(
            input_serialization_format="cdr", output_serialization_format="cdr"
        ),
    )

    topic_types = reader.get_all_topics_and_types()

    def typename(topic_name):
        for topic_type in topic_types:
            if topic_type.name == topic_name:
                return topic_type.type
        raise ValueError(f"topic {topic_name} not in bag")

    while reader.has_next():
        topic, data, timestamp = reader.read_next()
        if topics and topic not in topics:
            continue
        msg_type = get_message(typename(topic))
        msg = deserialize_message(data, msg_type)
        yield topic, msg, timestamp
    del reader
