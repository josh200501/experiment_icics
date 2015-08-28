"""
This program convert function call graph (produced by IDA Pro) to graphviz format.
"""

import sys
import json
from graphviz import Digraph
import networkx as nx
import numpy as np
from zerowine_pre_process import load_zerowine_tracefile

G = nx.DiGraph()
num2text = {}
start_func = ["START", "MAIN", "_START", "_MAIN"]
start_num = None
DEBUG = False

CUCKOO = False
ZEROWINE = True

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

def draw_path(paths_seq):
    "convert path sequences to graphviz graph file."
    dot = Digraph("All paths from main to endpoint.")
    time_stamp = str(time.time())
    for i in paths_seq:
        path = paths_seq[i]
        for node in path:
            dot.node(node, num2text[node])
        edges = nodes2edges(path)
        for edge in edges:
            dot.edge(edge["src"], edge["dst"])
    return dot.render('cfg/'+time_stamp+'.gv', view=True)

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
            #print ("to {0}: {1}".format(i, path))
            print ("========")
            print_text(path)
    paths_len_array = np.array(paths_len)
    path_sum = np.sum(paths_len_array)
    path_mean = np.mean(paths_len_array)
    path_std_var = np.std(paths_len_array)
    print ("path number: {0}".format(path_num))
    print ("path total length: {0}".format(path_sum))
    print ("path mean depth: {0}".format(path_mean))
    print ("path diversity: {0}".format(path_std_var))
    return (path_num, path_sum, path_mean, path_std_var)

def load_cuckoo_tracefile(fp_trace):
    "extrace api calls from cuckoo report file."
    fp = open(fp_trace, 'r')
    cont = fp.read()
    fp.close()
    cont_dict = json.loads(cont)
    calls = cont_dict["calls"]
    calls_filter = set()
    for apicall in calls:
        if apicall["category"] == "system":
            pass
        else:
            calls_filter.add(apicall["api"])
    return calls_filter

def locate_func_num(func_name):
    for i in num2text:
        if num2text[i] == func_name:
            return i
    return None

def prepare_execution_paths(api_calls):
    api_match_in_num = []
    for api in api_calls:
        if api in num2text.values():
            num = locate_func_num(api)
            if num != None:
                api_match_in_num.append(num)
    paths_match = {}
    for api in api_match_in_num:
        paths_match[api] = nx.shortest_path(G, source=start_num, target=api)
    return paths_match

def main(fp_fcg, fp_trace):
    global DEBUG
    paths_fcg = convert(fp_fcg)
    if CUCKOO:
        api_calls = load_cuckoo_tracefile(fp_trace)
    elif ZEROWINE:
        api_calls = load_zerowine_tracefile(fp_trace)
    paths_exe = prepare_execution_paths(api_calls)

    print ("[x]path metrics for static fcg:")
    static_met = compute_paths_metrics(paths_fcg)
    draw_path(paths_fcg)
    sys.exit(0)

    print ("[x]path metrics for execution:")
    DEBUG = True
    exe_met = compute_paths_metrics(paths_exe)
    prog_num = exe_met[0]*1.0/static_met[0]
    prog_len = exe_met[1]*1.0/static_met[1]
    print ("execution path number ratio: {0}".format(prog))
    print ("execution path length ratio: {0}".format(prog))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: program <gdlfile> <tracefile>")
        sys.exit(1)
    else:
        fp_fcg = sys.argv[1]
        fp_trace = sys.argv[2]
        main(fp_fcg, fp_trace)

