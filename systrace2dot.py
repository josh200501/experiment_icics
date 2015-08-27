"""
This program convert system call trace (produced by ether) to graph (graphviz format).
This way is not reasonable since the trace was just a sequence and did not contain any call information.
Should be revised latter.
"""
import sys
from graphviz import Digraph

def proc(file_path):
    syscalls = []
    dot = Digraph(comment="object call graph")
    fp = open(file_path, 'r')
    start = True
    while True:
        line = fp.readline().strip()
        if not line:
            break
        else:
            if start:
                dot.node(line,shape="box",color="red")
                start = False
            else:
                syscalls.append(line)
    fp.close()
    syscalls_set = set(syscalls)

    for i in syscalls_set:
        dot.node(i,i)

    fp = open(file_path, 'r')
    last_line = None
    edges = []
    while True:
        line = fp.readline().strip()
        if not line:
            break
        else:
            if not last_line:
                last_line = line
            else:
                edges.append(last_line+':'+line)
                last_line = line
    fp.close()

    j = 0
    edges_set = set(edges)
    edges_set = edges
    for i in edges_set:
        i_sp = i.split(':')
        dot.edge(i_sp[0], i_sp[1], label=str(j))
        j += 1
    dot.render("cfg/"+file_path+'.gv', view=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("usage: program <systrace>")
        sys.exit(1)
    else:
        file_path = sys.argv[1]
        proc(file_path)



