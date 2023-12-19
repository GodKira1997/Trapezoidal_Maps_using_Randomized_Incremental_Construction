"""
file: trapezoidal_maps.py
description: This program implements the random increemental algorithm to
create trapezoidal map for given space containing lines.
language: python3
author: Anurag Kallurwar, ak6491@rit.edu
author: Neel Chaudhary, nc5834@rit.edu
"""


import math
import sys
import csv
from structure import *


class TrapezoidalMap:
    """
    This class holds the trapezoidal map and matrix
    """
    __slots__ = "root", "trapezoidal_nodes", "pointPs", "pointQs", \
                "segments", "matrix"

    # Methods
    def __init__(self, root, segments):
        """
        Constructor
        :param root: Root of the directed acyclic graph
        :param segments: Input segments
        """
        self.root = root
        self.trapezoidal_nodes = []
        self.pointPs = []
        self.pointQs = []
        self.segments = segments
        self.matrix = []

    def get_all_Trapezoids(self):
        """
        Finds all leaf nodes/trapezoidal nodes
        :return: None
        """
        self.trapezoidal_nodes = []
        self.find_trapezoids(self.root)

    def find_trapezoids(self, node: TreeNode):
        """
        Recursively searches for the leaf nodes
        :param node: TreeNode
        :return: None
        """
        if not node:
            return None
        if not node.leftChild and not node.rightChild:
            if node not in self.trapezoidal_nodes:
                self.trapezoidal_nodes.append(node)
            return None
        if node.leftChild:
            self.find_trapezoids(node.leftChild)
        if node.rightChild:
            self.find_trapezoids(node.rightChild)

    def set_trapezoid_names(self):
        """
        Set names for the trapezoids
        :return: None
        """
        id = 1
        for node in self.trapezoidal_nodes:
            node.value.id = "T" + str(id)
            id += 1

    def create_adjacency_matrix(self):
        """
        Creates the adjacency matrix for the directed acyclic graph
        :return: None
        """
        # Collecting all nodes
        for segment in self.segments:
            if segment.start not in self.pointPs:
                self.pointPs.append(segment.start)
            if segment.end not in self.pointQs:
                self.pointQs.append(segment.end)
        # Creating dictionary of indices for the nodes
        node_dict = dict()
        index = 1
        for point in self.pointPs:
            node_dict[point.id] = index
            index += 1
        for point in self.pointQs:
            node_dict[point.id] = index
            index += 1
        for segment in self.segments:
            node_dict[segment.id] = index
            index += 1
        for node in self.trapezoidal_nodes:
            node_dict[node.value.id] = index
            index += 1
        # Initializing matrix
        keys = list(node_dict.keys())
        self.matrix = [['NAN'] + keys]
        for index in range(0, len(keys)):
            row = [keys[index]]
            row += [0] * len(keys)
            self.matrix.append(row)
        # Updating matrix with paths
        self.add_path_to_matrix(self.root, node_dict)
        self.add_sums()

    def add_path_to_matrix(self, node: TreeNode, node_dict: dict):
        """
        Recursively searches for throught the tree and updates matrix
        simultaneously
        :param node: TreeNode
        :param node_dict: Dictionary of indices
        :return: None
        """
        if not node:
            return None
        if not node.leftChild and not node.rightChild:
            return None
        else:
            left = node_dict[node.leftChild.value.id]
            right = node_dict[node.rightChild.value.id]
            # Updating the matrix with path
            current = node_dict[node.value.id]
            self.matrix[left][current] += 1
            self.matrix[right][current] += 1
            # print(node.value.id + "->" + node.leftChild.value.id + ", "
            #       + node.rightChild.value.id)
        if node.leftChild:
            self.add_path_to_matrix(node.leftChild, node_dict)
        if node.rightChild:
            self.add_path_to_matrix(node.rightChild, node_dict)

    def add_sums(self):
        """
        Calculating sums for every row and column
        :return: None
        """
        sums = [0] * (len(self.matrix[1]) - 1)
        print(self.matrix[0])
        self.matrix[0].append('SUM')
        for index1 in range(1, len(self.matrix)):
            row_sum = sum(self.matrix[index1][1:])
            for index2 in range(1, len(self.matrix[index1])):
                sums[index2 - 1] += self.matrix[index1][index2]
            self.matrix[index1].append(row_sum)
        self.matrix.append(['SUM'] + sums + [sum(sums)])



def read_input(file_name: str):
    """
    Read input from file
    :param file_name: name of file
    :return: None
    """
    str_lines = []
    segments = []
    with open(file_name, 'r') as file:
        str_lines = file.readlines()
    number_of_segments = int(str_lines[0])
    # Bounding box trapezoid
    bounding_box = [float(a) for a in str_lines[1].split(' ')]
    initial_trapezoid = Trapezoid(Segment(Point(bounding_box[0],
                                                bounding_box[3], 'Pb1'),
                                          Point(bounding_box[2],
                                                bounding_box[3], 'Qb1'), 'Sb1'),
                                  Segment(Point(bounding_box[0],
                                                bounding_box[1], 'Pb2'),
                                          Point(bounding_box[2],
                                                bounding_box[1], 'Qb2'),
                                          'Sb2'), Point(bounding_box[0],
                                                bounding_box[3], 'Pb1'),
                                  Point(bounding_box[2], bounding_box[3],
                                        'Qb1'))
    # Segments with unique points
    count = 1
    unique_points = []
    for str_line in str_lines[2:]:
        if str_line.strip() == '\n' or str_line.strip() == '':
            break
        coords = [float(a) for a in str_line.strip().split(' ')]
        if coords[0] < coords[2]:
            P = Point(coords[0], coords[1], 'P'+str(count))
            Q = Point(coords[2], coords[3], 'Q'+str(count))
        else:
            P = Point(coords[2], coords[3], 'P' + str(count))
            Q = Point(coords[0], coords[1], 'Q' + str(count))
        flagP = True
        flagQ = True
        for index in range(len(unique_points)):
            if P == unique_points[index]:
                P = unique_points[index]
                flagP = True
            if Q == unique_points[index]:
                Q = unique_points[index]
                flagQ = True
        if flagP: unique_points.append(P)
        if flagQ: unique_points.append(Q)
        segment = Segment(P, Q, 'S'+str(count))
        segments.append(segment)
        count += 1
    return number_of_segments, initial_trapezoid, segments


def write_output(file_name: str, matrix: list):
    """
    Write adjacency matrix to file
    :param file_name: name of file
    :param intersections: intersection points
    :return: None
    """
    print("WRITING TO OUPUT FILE: " + file_name)
    with open(file_name, 'w', newline='') as file:
        csvwriter = csv.writer(file, delimiter=',')
        for row in matrix:
            csvwriter.writerow(row)


def compute_intersecting_trapezoids(node: TreeNode, segment: Segment,
                                    trapezoidal_nodes: list = []):
    """
    Compute Trapezoids intersecting with the segment
    :param node: Tree Node
    :param segment: Segment Object
    :param trapezoidal_nodes: list of nodes of intersecting trapezoids
    :return: None
    """
    # If leaf node
    if node.is_leaf():
        if node.value.contains_segment(segment):
            if node not in trapezoidal_nodes:
                trapezoidal_nodes.append(node)
    # If node is X-node
    elif node.get_type() == Type.POINT:
        if segment.start.x >= node.value.x:
            compute_intersecting_trapezoids(node.rightChild, segment,
                                            trapezoidal_nodes)
        else:
            compute_intersecting_trapezoids(node.leftChild, segment,
                                            trapezoidal_nodes)
            if segment.end.x >= node.value.x:
                compute_intersecting_trapezoids(node.rightChild, segment,
                                                trapezoidal_nodes)
    # If node is Y-node
    else:
        if node.value.is_above(segment.start):
            compute_intersecting_trapezoids(node.leftChild, segment,
                                            trapezoidal_nodes)
        else:
            compute_intersecting_trapezoids(node.rightChild, segment,
                                            trapezoidal_nodes)


def handle_full_segment(map: TrapezoidalMap, segment: Segment,
                        trapezoidal_nodes: list):
    """
    Cases when segment is full inside the trapezoid
    :param map: Trapezoidal map
    :param segment: Segment Object
    :param trapezoidal_nodes: Intersecting Trapezoidal Nodes
    :return: None
    """
    trapezoid = trapezoidal_nodes[0].value
    # All trimmed trapezoids
    left_trapezoid = TreeNode(Trapezoid(trapezoid.top, trapezoid.bottom,
                               trapezoid.left, segment.start))
    right_trapezoid = TreeNode(Trapezoid(trapezoid.top, trapezoid.bottom,
                                         segment.end, trapezoid.right))
    above_trapezoid = TreeNode(Trapezoid(trapezoid.top, segment, segment.start,
                                segment.end))
    below_trapezoid = TreeNode(Trapezoid(segment, trapezoid.bottom,
                                         segment.start, segment.end))
    # Creating Subtree
    s_node = TreeNode(segment, above_trapezoid, below_trapezoid)
    q_node = TreeNode(segment.end, s_node, right_trapezoid)
    p_node = TreeNode(segment.start, left_trapezoid, q_node)
    if not trapezoidal_nodes[0].update_node(p_node):
        map.root = p_node


def handle_partial_segment(map: TrapezoidalMap, segment: Segment,
                        trapezoidal_nodes: list):
    """
    Cases when segment is intersecting multiple trapezoids
    :param map: Trapezoidal map
    :param segment: Segment Object
    :param trapezoidal_nodes: Intersecting Trapezoidal Nodes
    :return: None
    """
    upper_trapezoid = None # upper trim
    lower_trapezoid = None # lower trim
    upper_to_be_merged = False # If upper trim is to be merged
    # For all intersecting trapezoidal nodes
    for current_node in trapezoidal_nodes:
        trapezoid = current_node.value
        # If P of Segment is inside a trapezoid
        if trapezoid.contains_point(segment.start):
            # Left Trimmed trapezoid
            left_trapezoid = TreeNode(Trapezoid(trapezoid.top, trapezoid.bottom,
                                                trapezoid.left, segment.start))
            # If upper is to be merged
            if segment.is_above(trapezoid.right):
                upper_trapezoid = TreeNode(Trapezoid(trapezoid.top, segment,
                                                  segment.start,
                                                  trapezoid.right))
                lower_trapezoid = TreeNode(Trapezoid(segment, trapezoid.bottom,
                                                  segment.start, None))
                upper_to_be_merged = False
            else: # Else lower is to be merged
                upper_trapezoid = TreeNode(Trapezoid(trapezoid.top, segment,
                                                  segment.start, None))
                lower_trapezoid = TreeNode(Trapezoid(segment, trapezoid.bottom,
                                                  segment.start,
                                                     trapezoid.right))
                upper_to_be_merged = True
            # If Point P X-Node already visited
            if segment.start.visited:
                continue
            # Creating subtree
            s_node = TreeNode(segment, upper_trapezoid, lower_trapezoid)
            p_node = TreeNode(segment.start, left_trapezoid, s_node)
            if not current_node.update_node(p_node):
                map.root = current_node
        # If Q of Segment is inside a trapezoid
        elif trapezoid.contains_point(segment.end):
            # Right Trimmed trapezoid
            right_trapezoid = TreeNode(Trapezoid(trapezoid.top,
                                             trapezoid.bottom,
                                             segment.end, trapezoid.right))
            # If upper is to be merged
            if upper_to_be_merged:
                upper_trapezoid.value.right = segment.end
                lower_trapezoid = TreeNode(Trapezoid(segment,
                                                  trapezoid.bottom,
                                                  trapezoid.left,
                                                  segment.end))
            else: # Else lower is to be merged
                upper_trapezoid = TreeNode(Trapezoid(trapezoid.top,
                                                  segment, trapezoid.left,
                                                  segment.end))
                lower_trapezoid.value.right = segment.end
            # If Point Q X-Node already visited
            if segment.end.visited:
                continue
            s_node = TreeNode(segment, upper_trapezoid, lower_trapezoid)
            q_node = TreeNode(segment.end, s_node, right_trapezoid)
            if not current_node.update_node(q_node):
                map.root = current_node
        # Else Segment is fully trimming a trapezoid
        else:
            # If upper is to be merged
            if upper_to_be_merged:
                lower_trapezoid = TreeNode(Trapezoid(segment, trapezoid.bottom,
                                                  trapezoid.left, None))
            else: # Else lower is to be merged
                upper_trapezoid = TreeNode(Trapezoid(trapezoid.top, segment,
                                                  trapezoid.left, None))
            # Updating the trapezoids
            if segment.is_above(trapezoid.right):
                upper_trapezoid.value.right = trapezoid.right
                upper_to_be_merged = False
            else:
                lower_trapezoid.value.right = trapezoid.right
                upper_to_be_merged = True
            # Creating Subtree
            s_node = TreeNode(segment, upper_trapezoid, lower_trapezoid)
            if not current_node.update_node(s_node):
                print("NO PARENT")
                map.root = current_node


def generate_map(initial_trapezoid, segments: list):
    """
    Implement random increemental algorithm to generate a trapezoidal map
    :param initial_trapezoid: Boundin box trapezoid
    :param segments: Input segments
    :return: None
    """
    # Initializing trapezoidal map
    map = TrapezoidalMap(TreeNode(initial_trapezoid), segments)
    # Looping over input segments
    for segment in segments:
        # Computing intersecting trapezoids by tracing along the segment
        trapezoidal_nodes = []
        compute_intersecting_trapezoids(map.root, segment, trapezoidal_nodes)
        if len(trapezoidal_nodes) < 1:
            continue;
        # If segment is fully inside the trapezoid
        elif len(trapezoidal_nodes) == 1:
            handle_full_segment(map, segment, trapezoidal_nodes)
        # If segment is partially inside the trapezoid
        else:
            handle_partial_segment(map, segment, trapezoidal_nodes)
    # Fetch all trapezoids
    map.get_all_Trapezoids()
    # Set names for trapezoids
    map.set_trapezoid_names()
    # Create adjacency matrix
    map.create_adjacency_matrix()
    trapezoids = []
    for node in map.trapezoidal_nodes:
        trapezoids.append(node.value)
    return map.matrix, trapezoids


def main():
    """
    The main function
    :return: None
    """
    # Check for CLI paramters
    if len(sys.argv) < 2:
        print("Please provide an input file")
        print("USAGE: trapezoidal_maps.py <filename.txt>")
        return
    file_name = str(sys.argv[1])
    output_file_name = "output_dag_matrix.csv"
    # file_name = input("Input file name: ")

    # Reading input
    print("\n============================================================")
    print("READING INPUT FILE: " + file_name)
    number_of_segments, bounding_box, segments = read_input(file_name)

    # Trapezoidal Map
    print("\n============================================================")
    dag_matrix, trapezoids = generate_map(bounding_box, segments)
    print("Trapezoids")
    for trapezoid in trapezoids:
        print(repr(trapezoid))
    print("\n============================================================")
    print("Adjacency Matrix")
    for row in dag_matrix:
        print(row)

    # Writing output to file
    print("\n============================================================")
    write_output(output_file_name, dag_matrix)


if __name__ == '__main__':
    main()  # Calling Main Function
