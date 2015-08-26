import json
import sys
from graphviz import Digraph

def proc(file_path):
    fp = open(file_path, 'r')
    cont = fp.read()
    fp.close()
    cont_dict = json.loads(cont)
    calls = cont_dict["calls"]
    calls_filter = []
    for i in calls:
        if i["category"] == "system":
            pass
        else:
            calls_filter.append(i["api"])

    dot = Digraph(comment="cuckoolog")
    last = None
    j = 0
    edges = set()
    for i in calls_filter:
        if last == None:
            last = i
        else:
            if last+i in edges:
                pass
            else:
                edges.add(last+i)
                dot.edge(last,i,label=str(j))
                j += 1
            last = i

    dot.render("cfg/"+file_path+'.gv', view=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("usage: program <cuckoo_log>")
        sys.exit(1)
    else:
        file_path = sys.argv[1]
        proc(file_path)
