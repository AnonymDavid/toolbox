from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
import rosbag2_py
from typing import List, Dict

def msg2dict(msg, pretag:str="") -> Dict[str, any]:
    """
    Convert a ROS2 message to a dictionary.

    Args:
        msg (any): The ROS2 message object to convert.
        pretag (str, optional): Prefix tag for the dictionary keys.

    Returns:
        Dict[str, any]: The dictionary representation of the message.
    """
    attributes:Dict[str, any]={}

    for attr in msg.__slots__:
        if hasattr(getattr(msg, attr), '__slots__'):
            attributes.update(msg2dict(getattr(msg, attr), pretag="".join([pretag, attr.lstrip('_'), "."])))
        else:
            if hasattr(getattr(msg, attr), '__iter__') and type(getattr(msg, attr)) is not str:
                for i, item in enumerate(getattr(msg, attr)):
                    if hasattr(item, '__slots__'):
                        attributes.update(msg2dict(item, pretag="".join([pretag, attr.lstrip('_'), f"[{i}]."])))
                    else:
                        attributes[pretag + attr.lstrip('_') + f"[{i}]"] = item
            else:
                attributes[pretag + attr.lstrip('_')] = getattr(msg, attr)
        
    return attributes


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
