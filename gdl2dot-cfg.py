import sys
from graphviz import Digraph

dot = Digraph(comment="test")
fp_path1 = 'test.gdl'

def convert(fp_path):
    fp = open(fp_path, 'r')
    count = 0
    #DEBUG = True
    DEBUG = False
    all_lines = fp.read()
    lines = all_lines.split("node: ")
    for line in lines:
        if not line.startswith('{'):
            continue
        else:
            title = line.split(' ')[2][1:-1]
            label_tmp = line.split('label: ')[1][1:]
            index_1 = label_tmp.index("}")
            label_tmp = label_tmp[:index_1]
            index_2 = label_tmp.rindex("\"")
            label = label_tmp[:index_2]
            dot.node(title, label)
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
            dot.edge(row, colum)
            if DEBUG:
                print("source: {0}".format(row))
                print("destination: {0}".format(colum))
                count += 1
                if count == 100:
                    break
        else:
            continue

    dot.render('cfg/'+fp_path+'.gv', view=False)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: program <gdlfile>")
        sys.exit(1)
    else:
        fp = sys.argv[1]
        convert(fp)

