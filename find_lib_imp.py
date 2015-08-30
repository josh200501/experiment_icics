"""
This program convert gdl file to dot file, find all
the path from src node to target node.
Initially this program was used to find out how api
functions was implemented.

@@Author: johnson
@@Date: Auguest 30th, 2015
"""
import sys
from graphviz import Digraph
import networkx as nx
import time

G = nx.DiGraph()
num2text = {}

def draw_path(paths_seq):
    """
    input format:
    {1:[], 2:[], 3:[], ...}
    """
    "convert path sequences to graphviz graph file."
    dot = Digraph("All paths from main to endpoint.")
    time_stamp = str(time.time())
    "filter out duplication"
    edges_pool = []
    for i in paths_seq:
        path = paths_seq[i]
        for node in path:
            dot.node(node, num2text[node])
        edges = nodes2edges(path)
        for edge in edges:
            edge_sign = edge["src"]+edge["dst"]
            if edge_sign not in edges_pool:
                dot.edge(edge["src"], edge["dst"])
                edges_pool.append(edge_sign)
    dot.render('cfg/'+time_stamp+'.gv', view=True)

def convert(fp_path):
    global start_num
    fp = open(fp_path, 'r')
    while True:
        line = fp.readline()
        if not line:
            break
        elif line.startswith('node'):
            title = line.split(' ')[3][1:-1]
            label = line.split(' ')[5][1:-1]
            " save relationship between number and text."
            num2text[title] = label
            G.add_node(title)

    fp.seek(0)
    while True:
        line = fp.readline()
        if not line:
            break
        elif line.startswith('edge'):
            src = line.split(' ')[3][1:-1]
            dst = line.split(' ')[5][1:-1]
            G.add_edge(src, dst)
    fp.close()

def nodes2edges(nodes_seq):
    last_node = None
    edges = []
    for node in nodes_seq:
        if last_node == None:
            last_node = node
        else:
            edges.append({"src":last_node, "dst":node})
            last_node = node
    return edges

def locate_func_num(func_name):
    for i in num2text:
        if num2text[i].upper() == func_name.upper():
            return i
    return None

def find_path(src_name, dst_name):
    src_num = locate_func_num(src_name)
    dst_num = locate_func_num(dst_name)
    if src_num == None:
        print ("Error: source number None")
        sys.exit(0)
    if dst_num == None:
        print ("Warning: target number was not set, find all path.")
        paths_from_src = nx.shortest_path(G, source=src_num)
        return paths_from_src
    else:
        paths_from_src_to_target = nx.all_simple_paths(G, source=src_num, target=dst_num)
        paths_seq = {}
        j = 0
        for path in paths_from_src_to_target:
            paths_seq[j] = path
            j += 1
        return paths_seq

def check_path_api(path):
    """
    check if there was api functions in one path
    (filter out functions start with sub_xxxxxx, nullsub_, _, lower case letter)
    """
    for node in path:
        if check_node_api(node):
            return True
    return False

def check_node_api(node):
    """
    check if a node was api function.
    """
    if not num2text[node].startswith("sub_") and \
            not num2text[node].startswith("nullsub_") and \
            not num2text[node].startswith("_"):
        return True
    else:
        return False

def reduce_path(paths_seq):
    "drop functions that was not API func."
    res = {}
    j = 0
    for i in paths_seq:
        path = paths_seq[i]
        "check apis in path"
        if check_path_api(path):
            while len(path):
                "check whether a node was api call"
                if not check_node_api(path[-1]):
                    del path[-1]
                else:
                    break
            if path:
                res[str(j)] = path
                j += 1
    return res

def main(fp, src, dst):
    convert(fp)
    paths_seq = find_path(src, dst)
    #draw_path(paths_seq)
    paths_seq = reduce_path(paths_seq)
    draw_path(paths_seq)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("usage: program <gdlfile> src_func dst_func")
        sys.exit(1)
    else:
        fp = sys.argv[1]
        src = sys.argv[2]
        dst = sys.argv[3]
        main(fp, src, dst)

