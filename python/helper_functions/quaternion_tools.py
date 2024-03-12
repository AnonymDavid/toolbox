from scipy.spatial.transform import Rotation as R
from numpy import ndarray


def euler_to_quaternion(roll:float, pitch:float, yaw:float, in_degrees:bool=True) -> ndarray:
    """
    Convert Euler angles to quaternion.

    Args:
        roll (float): The roll angle in degrees.
        pitch (float): The pitch angle in degrees.
        yaw (float): The yaw angle in degrees.
        in_degrees (bool, optional): If the input angles are in degrees. Defaults to True.

    Returns:
        numpy.ndarray: The quaternion representation of the Euler angles [x,y,z,w].
    """
    return R.from_euler('xyz', [roll, pitch, yaw], degrees=in_degrees).as_quat()

def euler_to_quaternion(rpy:ndarray, in_degrees:bool=True) -> ndarray:
    """
    Convert Euler angles to quaternion.

    Args:
        rpy (numpy.ndarray): The roll, pitch, and yaw angles in degrees.
        in_degrees (bool, optional): If the input angles are in degrees. Defaults to True.

    Returns:
        numpy.ndarray: The quaternion representation of the Euler angles [x,y,z,w].
    """
    if rpy.shape != (3,):
        raise ValueError("The input euler angles must be a 3x1 array.")

    return R.from_euler('xyz', rpy, degrees=in_degrees).as_quat()

def quaternion_to_euler(x:float, y:float, z:float, w:float, in_degrees:bool=True) -> ndarray:
    """
    Convert an quaternion to euler angles.

    Args:
        x (float): The x component of the quaternion
        y (float): The y component of the quaternion
        z (float): The z component of the quaternion
        w (float): The w component of the quaternion
        in_degrees (bool, optional): If the output angles should be in degrees. Defaults to True.

    Returns:
        numpy.ndarray: The euler representation of the quaternion [roll, pitch, yaw].
    """
    return R.from_quat([x, y, z, w]).as_euler('xyz', degrees=in_degrees)

def quaternion_to_euler(quat:ndarray, in_degrees:bool=True) -> ndarray:
    """
    Convert an quaternion to euler angles.

    Args:
        quat (numpy.ndarray): The quaternion [x, y, z, w].
        in_degrees (bool, optional): If the output angles should be in degrees. Defaults to True.

    Returns:
        numpy.ndarray: The euler representation of the quaternion [roll, pitch, yaw].
    """
    if quat.shape != (4,):
        raise ValueError("The input quaternion must be a 4x1 array.")
    
    return R.from_quat(quat).as_euler('xyz', degrees=in_degrees)
