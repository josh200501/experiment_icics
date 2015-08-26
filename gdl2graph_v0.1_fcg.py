import sys
import json
from graphviz import Digraph
import networkx as nx
import numpy as np

"""
This program convert function call graph (produced by IDA Pro) to graphviz format.
"""
G = nx.DiGraph()
num2text = {}
start_func = ["START", "MAIN", "_START", "_MAIN", "START_1"]
start_num = None
DEBUG = False

def print_text(num_seq):
    for i in num_seq:
        print(num2text[i]+'-->')


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
            if label.upper() in start_func:
                start_num = title
            if label.startswith("sub") or label.startswith('_'):
                pass
            else:
                G.add_node(title)

    fp.seek(0)
    while True:
        line = fp.readline()
        if not line:
            break
        elif line.startswith('edge'):
            src = line.split(' ')[3][1:-1]
            dst = line.split(' ')[5][1:-1]
            if src.startswith("sub") and dst.startswith("sub"):
                pass
            else:
                G.add_edge(src, dst)
    fp.close()

    if start_num == None:
        print ("no start function was found.")
        sys.exit(1)
    else:
        paths_from_start = nx.shortest_path(G, source=start_num)


    return paths_from_start

    #dot.save(filename='cfg/'+fp_path+'.gv')
    #dot3.render('cfg/'+fp_path+'.gv', view=True)
def compute_paths_metrics(paths_seq):
    "compute path number, depth and diversity."
    path_num = 0
    paths_len = []
    path_mean = 0
    path_std_var = 0
    if DEBUG:
        print ("=====paths=====")
    for i in paths_seq:
        path = paths_seq[i]
        path_num += 1
        paths_len.append(len(path))
        if DEBUG:
            print ("to {0}: {1}".format(i, path))
    paths_len_array = np.array(paths_len)
    path_mean = np.mean(paths_len_array)
    path_std_var = np.std(paths_len_array)
    print ("path number: {0}".format(path_num))
    print ("path mean depth: {0}".format(path_mean))
    print ("path diversity: {0}".format(path_std_var))
    return (path_num, path_mean, path_std_var)

def load_cuckoo_tracefile(fp_trace):
    "extrace api calls from cuckoo report file."
    fp = open(fp_trace, 'r')
    cont = fp.read()
    fp.close()
    cont_dict = json.loads(cont)
    calls = cont_dict["calls"]
    calls_filter = []
    for apicall in calls:
        if apicall["category"] == "system":
            pass
        else:
            calls_filter.append(apicall["api"])
    return calls_filter

def locate_func_num(func_name):
    for i in num2text:
        if num2text[i] == func_name:
            return i
    return None

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: program <gdlfile>")
        sys.exit(1)
    else:
        fp_fcg = sys.argv[1]
        paths_fcg = convert(fp_fcg)
        compute_paths_metrics(paths_fcg)

