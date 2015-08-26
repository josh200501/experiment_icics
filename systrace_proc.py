import sys

def proc(src, dst):
    syscalls = []
    fp_src = open(src, 'r')
    fp_dst = open(dst, 'w')
    while True:
        line = fp_src.readline()
        if not line:
            break
        else:
            if not line.startswith("CALL"):
                continue
            else:
                line_sp = line.split(',')
                syscall = line_sp[2].strip()
                syscall = syscall[:syscall.index('(')]
                fp_dst.write(syscall+'\n')
    fp_src.close()
    fp_dst.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print ("usage: program <src> <dst>")
        sys.exit(1)
    else:
        src = sys.argv[1]
        dst = sys.argv[2]
        proc(src, dst)
