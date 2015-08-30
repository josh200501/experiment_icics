"""
This program convert function call graph (produced by IDA Pro) to graphviz format.
"""
import sys
import json
from graphviz import Digraph
import networkx as nx
import numpy as np
import time
from zerowine_pre_process import load_zerowine_tracefile

G = nx.DiGraph()
num2text = {}
start_func = ["START", "MAIN", "_START", "_MAIN", "START_1"]
start_num = None
DEBUG = False

CUCKOO = True
ZEROWINE = False
CUCKOOAPIS = "cuckooapis.txt"
CUCKOO_ORG = False

def load_cuckooapis():
    fp = open(CUCKOOAPIS, 'r')
    cont = fp.read()
    fp.close()
    cont_dict = json.loads(cont)
    apis = cont_dict["apis"]
    return apis

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
            num2text[title] = filter_api(label)
            if label.upper() in start_func:
                start_num = title
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

    if start_num == None:
        print ("no start function was found.")
        sys.exit(1)
    else:
        paths_from_start = nx.shortest_path(G, source=start_num)

    return paths_from_start

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
    #print ("apis number: {0}".format(len(calls_filter)))
    #print ("apis: {0}".format(calls_filter))
    return calls_filter

def load_cuckoo_apicalls(fp_apicalls):
    "load processed api calls"
    fp = open(fp_apicalls, 'r')
    cont = fp.read()
    fp.close()
    cont_dict = json.loads(cont)
    calls = cont_dict["api_calls"]
    return calls

def locate_func_num(func_name):
    for i in num2text:
        if num2text[i] == func_name:
            return i
    return None

def filter_api(func_name):
    """
    delete postfix of windows api (Ex, W, A, etc)
    """
    if func_name.endswith("W") or func_name.endswith("A"):
        func_name = func_name[:-1]
    if func_name.endswith("Ex"):
        func_name = func_name[:-2]
    return func_name

def prepare_execution_paths(api_calls):
    api_match_in_num = []
    for api in api_calls:
        api = filter_api(api)
        if api in num2text.values():
            num = locate_func_num(api)
            if num != None:
                api_match_in_num.append(num)
    paths_match = {}
    for api in api_match_in_num:
        try:
            paths_match[api] = nx.shortest_path(G, source=start_num, target=api)
        except:
            pass
    return paths_match

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
    path_sum = np.sum(paths_len_array)
    path_mean = np.mean(paths_len_array)
    path_std_var = np.std(paths_len_array)
    print ("path number: {0}".format(path_num))
    print ("path length sum: {0}".format(path_sum))
    print ("path mean depth: {0}".format(round(path_mean, 2)))
    print ("path diversity: {0}".format(round(path_std_var, 2)))
    return (path_num, path_sum, path_mean, path_std_var)

def draw_path(paths_seq):
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

def draw_path_hybrid(fcg_path, exe_path):
    "draw execution path on static function call graph"
    dot = Digraph(".")
    time_stamp = str(time.time())
    "filter out duplication"
    edges_pool = []
    #nodes_pool = []
    "draw execution path"
    for i in exe_path:
        path = exe_path[i]
        for node in path:
            dot.node(node, num2text[node], color="red")
        edges = nodes2edges(path)
        for edge in edges:
            edge_sign = edge["src"]+edge["dst"]
            if edge_sign not in edges_pool:
                dot.edge(edge["src"], edge["dst"], color="red")
                edges_pool.append(edge_sign)
    "draw static function call graph"
    for i in fcg_path:
        path = fcg_path[i]
        for node in path:
            dot.node(node, num2text[node])
        edges = nodes2edges(path)
        for edge in edges:
            edge_sign = edge["src"]+edge["dst"]
            if edge_sign not in edges_pool:
                dot.edge(edge["src"], edge["dst"])
                edges_pool.append(edge_sign)
    dot.render('cfg/'+time_stamp+'.gv', view=True)


def check_path_api(path):
    """
    check if there was api functions in one path
    (filter out functions start with sub_xxxxxx, nullsub_, _, lower case letter)
    """
    for node in path:
        if not num2text[node].startswith("sub_") and \
                not num2text[node].startswith("nullsub_") and \
                not num2text[node].startswith("_"):
            if num2text[node].upper() not in start_func:
                return True
    return False

def check_node_api(node):
    """
    check if a node was api function.
    """
    "get apis in function call graph"
    fcg_apis = set(num2text.values())
    fcg_apis_plain = set()
    for api in fcg_apis:
        fcg_apis_plain.add(filter_api(api))

    "get apis in cuckoo monitor list"
    cuckoo_apis_plain = set(load_cuckooapis())

    "get apis in execution path"
    if CUCKOO:
        if CUCKOO_ORG:
            api_calls = load_cuckoo_tracefile(fp_trace)
        else:
            api_calls = load_cuckoo_apicalls(fp_trace)
    elif ZEROWINE:
        api_calls = load_zerowine_tracefile(fp_trace)
    cuckoo_apis_exe = set()
    for api in api_calls:
        cuckoo_apis_exe.add(filter_api(api))
    cuckoo_apis_plain = cuckoo_apis_plain | cuckoo_apis_exe

    "get common part of apis"
    common_apis = fcg_apis_plain & cuckoo_apis_plain

    "get node function name"
    name = num2text[node]
    name_plain = filter_api(name)
    if name_plain in common_apis:
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

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: program <gdlfile> <tracefile>")
        sys.exit(1)
    else:
        fp_fcg = sys.argv[1]
        fp_trace = sys.argv[2]

        paths_fcg = convert(fp_fcg)
        draw_path(paths_fcg)
        paths_fcg = reduce_path(paths_fcg)
        #print ("path num: {0}".len(paths_fcg))
        #print ("paths: {0}".format(paths_fcg))
        #for path in paths_fcg:
        #    print_text(path)
        draw_path(paths_fcg)

        if CUCKOO:
            if CUCKOO_ORG:
                api_calls = load_cuckoo_tracefile(fp_trace)
            else:
                api_calls = load_cuckoo_apicalls(fp_trace)
        elif ZEROWINE:
            api_calls = load_zerowine_tracefile(fp_trace)
        paths_exe = prepare_execution_paths(api_calls)

        print ("[o] path metrics for static fcg:")
        static_met = compute_paths_metrics(paths_fcg)

        print ("[o] path metrics for execution:")
        exe_met = compute_paths_metrics(paths_exe)

        draw_path_hybrid(paths_fcg, paths_exe)

        print ("[o] execution progress:")
        prog_num = exe_met[0]*1.0/static_met[0]
        prog_len = exe_met[1]*1.0/static_met[1]
        #print ("exe_met: {0}".format(exe_met))
        #print ("static_met: {0}".format(static_met))
        print ("execution path number ratio: {0}".format(round(prog_num, 2)))
        print ("execution path length ratio: {0}".format(round(prog_len, 2)))

