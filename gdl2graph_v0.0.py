import sys
from graphviz import Digraph
import networkx as nx

"""
This program convert function call graph (produced by IDA Pro) to graphviz format.
"""
dot = Digraph(comment="test")
dot2 = Digraph(comment="short")
#G = nx.Graph()
G = nx.DiGraph()
fp_path1 = 'test.gdl'
num2text = {}

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
    fp = open(fp_path, 'r')
    count = 0
    #DEBUG = True
    DEBUG = False
    while True:
        line = fp.readline()
        if not line:
            #print ("EOF")
            break
        elif line.startswith('node'):
            title = line.split(' ')[3][1:-1]
            label = line.split(' ')[5][1:-1]
            num2text[title] = label
            if label.startswith("sub") or label.startswith('_'):
                pass
            else:
                dot.node(title, label)
                G.add_node(title)
            if DEBUG:
                print("title: {0}".format(title))
                print("label: {0}".format(label))
                count += 1
                if count == 100:
                    print ("counting down")
                    break
        else:
            continue
    fp.close()

    fp = open(fp_path, 'r')
    count = 0
    while True:
        line = fp.readline()
        if not line:
            break
        elif line.startswith('edge'):
            row = line.split(' ')[3][1:-1]
            colum = line.split(' ')[5][1:-1]
            if row.startswith("sub") and colum.startswith("sub"):
                pass
            else:
                dot.edge(row, colum)
                G.add_edge(row, colum)
            if DEBUG:
                print("source: {0}".format(row))
                print("destination: {0}".format(colum))
                count += 1
                if count == 100:
                    break
        else:
            continue

    "1======================="
    path = nx.shortest_path(G,source="97",target="212")
    print ("path from <start> to <RemoveDIrectoryA>\n {0}".format(path))
    print_text(path)
    for node in path:
        dot2.node(node, num2text[node])
    edges = nodes2edges(path)
    for edge in edges:
        dot2.edge(edge["src"], edge["dst"], color="red", label="1")

    "2======================="
    path = nx.shortest_path(G,source="97",target="199")
    print ("path from <start> to <CreateDirectoryA>\n {0}".format(path))
    print_text(path)

    for node in path:
        dot2.node(node, num2text[node])
    edges = nodes2edges(path)
    for edge in edges:
        dot2.edge(edge["src"], edge["dst"], color="green", label="2")

    "3======================="
    path = nx.shortest_path(G,source="97",target="218")
    print ("path from <start> to <FindFirstFileA>\n {0}".format(path))
    print_text(path)

    for node in path:
        dot2.node(node, num2text[node])
    edges = nodes2edges(path)
    for edge in edges:
        dot2.edge(edge["src"], edge["dst"], color="blue", label="3")

    "4======================="
    path = nx.shortest_path(G,source="97",target="215")
    print ("path from <start> to <DeleteFileA>\n {0}".format(path))
    print_text(path)

    for node in path:
        dot2.node(node, num2text[node])
    edges = nodes2edges(path)
    for edge in edges:
        dot2.edge(edge["src"], edge["dst"], color="black", label="4")

    "5======================="
    path = nx.shortest_path(G,source="97",target="180")
    print ("path from <start> to <RegOpenKeyExA>\n {0}".format(path))
    print_text(path)

    for node in path:
        dot2.node(node, num2text[node])
    edges = nodes2edges(path)
    for edge in edges:
        dot2.edge(edge["src"], edge["dst"], label="5")
    "6======================="
    path = nx.shortest_path(G,source="97",target="182")
    print ("path from <start> to <RegQueryValueExA>\n {0}".format(path))
    print_text(path)

    for node in path:
        dot2.node(node, num2text[node])
    edges = nodes2edges(path)
    for edge in edges:
        dot2.edge(edge["src"], edge["dst"], label="6")
    "7======================="
    path = nx.shortest_path(G,source="97",target="181")
    print ("path from <start> to <RegSetValueExA>\n {0}".format(path))
    print_text(path)

    for node in path:
        dot2.node(node, num2text[node])
    edges = nodes2edges(path)
    for edge in edges:
        dot2.edge(edge["src"], edge["dst"], label="7")
    "8======================="
    path = nx.shortest_path(G,source="97",target="178")
    print ("path from <start> to <RegCloseKey>\n {0}".format(path))
    print_text(path)

    for node in path:
        dot2.node(node, num2text[node])
    edges = nodes2edges(path)
    for edge in edges:
        dot2.edge(edge["src"], edge["dst"], label="8")
    "9======================="
    path = nx.shortest_path(G,source="97",target="183")
    print ("path from <start> to <RegCreateKeyExA>\n {0}".format(path))
    print_text(path)

    for node in path:
        dot2.node(node, num2text[node])
    edges = nodes2edges(path)
    for edge in edges:
        dot2.edge(edge["src"], edge["dst"], label="9")
    "10======================="
    path = nx.shortest_path(G,source="97",target="179")
    print ("path from <start> to <RegDeleteValueA>\n {0}".format(path))
    print_text(path)

    for node in path:
        dot2.node(node, num2text[node])
    edges = nodes2edges(path)
    for edge in edges:
        dot2.edge(edge["src"], edge["dst"], label="10")
    "11======================="
    path = nx.shortest_path(G,source="97",target="243")
    print ("path from <start> to <CreateProcessA>\n {0}".format(path))
    print_text(path)

    for node in path:
        dot2.node(node, num2text[node])
    edges = nodes2edges(path)
    for edge in edges:
        dot2.edge(edge["src"], edge["dst"], label="11")
    "12======================="
    path = nx.shortest_path(G,source="97",target="233")
    print ("path from <start> to <ExitProcess>\n {0}".format(path))
    print_text(path)

    for node in path:
        dot2.node(node, num2text[node])
    edges = nodes2edges(path)
    for edge in edges:
        dot2.edge(edge["src"], edge["dst"], label="12")
    "13======================="
    path = nx.shortest_path(G,source="97",target="189")
    print ("path from <start> to <GetLastError>\n {0}".format(path))
    print_text(path)

    for node in path:
        dot2.node(node, num2text[node], shape="box")
    edges = nodes2edges(path)
    for edge in edges:
        dot2.edge(edge["src"], edge["dst"], label="13")

    path_all = nx.all_shortest_paths(G,source="97",target="233")
    print ("all path from <start> to <ExitProcessA>")
    for i in path_all:
        print i

    path_all = nx.all_shortest_paths(G,source="97",target="189")
    print ("all path from <start> to <GetLastError>")
    for i in path_all:
        print i

    dot3 = Digraph("all_Path")
    path_all_n = nx.shortest_path(G,source="97")
    print ("all path from <start>")
    j = 0
    "log length for every path starting from <start>"
    paths_len = []
    for i in path_all_n:
        path = path_all_n[i]
        paths_len.append(len(path))
        print path
        for node in path:
            dot3.node(node, num2text[node])
        edges = nodes2edges(path)
        for edge in edges:
            dot3.edge(edge["src"], edge["dst"], label=str(j))
        j += 1

    "1======================="
    path = nx.shortest_path(G,source="97",target="212")
    print ("path from <start> to <RemoveDIrectoryA>\n {0}".format(path))
    print_text(path)
    #for node in path:
    #    dot2.node(node, num2text[node])
    edges = nodes2edges(path)
    for edge in edges:
        dot3.edge(edge["src"], edge["dst"], color="blue", label="1")
    "1======================="
    """
    path = nx.shortest_path(G,source="97",target="189")
    print ("path from <start> to <GetLastError>\n {0}".format(path))
    print_text(path)
    #for node in path:
    #    dot2.node(node, num2text[node])
    edges = nodes2edges(path)
    for edge in edges:
        dot3.edge(edge["src"], edge["dst"], color="green", label="o")
    """
    """
    path_error = nx.shortest_path(G, target="189")
    print ("all path to <GetLastError>")
    for i in path_error:
        #print (i, path_error[i])
        path = path_error[i]
        for node in path:
            dot3.node(node, num2text[node])
        edges = nodes2edges(path)
        for edge in edges:
            dot3.edge(edge["src"], edge["dst"], color="blue", label="e")
    """
    path_error = nx.all_simple_paths(G, source="97", target="189")
    print ("all path from <start> to <GetLastError>")
    #for i in path_exit:
    #    print i
    for path in path_error:
        edges = nodes2edges(path)
        for edge in edges:
            dot3.edge(edge["src"], edge["dst"], color="red", label='e')

    path_exit = nx.all_simple_paths(G, source="97", target="233")
    print ("all path from <start> to <ExitProcessA>")
    #for i in path_exit:
    #    print i
    for path in path_exit:
        edges = nodes2edges(path)
        for edge in edges:
            dot3.edge(edge["src"], edge["dst"], color="green", label='x')

    import numpy as np
    data = np.array(paths_len)
    print ("path mean: {0}".format(np.mean(data)))
    print ("path var:  {0}".format(np.var(data)))
    print ("path std var:  {0}".format(np.std(data)))
    #print ("path num: {0}".format(len(path_all)))
    #print path_all

    #dot.save(filename='cfg/'+fp_path+'.gv')
    #for i in path_all:
    #    print i
    #dot2.render('cfg/'+fp_path+'.gv', view=True)
    dot3.render('cfg/'+fp_path+'.gv', view=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: program <gdlfile>")
        sys.exit(1)
    else:
        fp = sys.argv[1]
        convert(fp)

