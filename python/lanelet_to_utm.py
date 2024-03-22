import xml.etree.ElementTree as ET
from pyproj import Proj, transform


def lanelet_to_utm(input:str, output:str, x_offset:float=0.0, y_offset:float=0.0, verbose:bool=True):
    """
    Converts the coordinates of nodes in a lanelet OSM file from WGS84 to UTM projection and add it as attributes to the nodes.

    Parameters:
    - input (str): The path to the input lanelet OSM file.
    - output (str): The path to the output lanelet OSM file.
    - x_offset (float): The offset to be applied to the UTM x-coordinate.
    - y_offset (float): The offset to be applied to the UTM y-coordinate.
    - verbose (bool): If True, print progress information.

    Returns:
    None
    """
    wgs84 = Proj(init='epsg:4326')
    utm = Proj(init='epsg:32633')

    tree = ET.parse(input)
    root = tree.getroot()

    c = 1
    length = len(root.findall('.//node'))
    for node in root.findall('.//node'):
        lon = float(node.get('lon'))
        lat = float(node.get('lat'))
        x, y = transform(wgs84, utm, lon, lat)

        ET.SubElement(node, 'tag', {'k': 'local_x', 'v': str(x + x_offset)})
        ET.SubElement(node, 'tag', {'k': 'local_y', 'v': str(y + y_offset)})

        if verbose and c % 100 == 0:
            print(f'Nodes: {c}/{length}')
        c += 1

    print(f'Finished: {c-1}/{length} nodes')

    tree.write(output)
