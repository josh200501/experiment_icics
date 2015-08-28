import sys
import os
from gdl2graph import *

CUCKOO = False
ZEROWINE = True

def main(fcg_dir, trace_dir):
    fcgs = os.listdir(fcg_dir)
    traces = os.listdir(trace_dir)
    for fcg in fcgs:
        target = fcg[:-4]
        for trace in traces:
            if target in trace:
                fp_trace = os.path.join(trace_dir, trace)
                break
        fp_fcg = os.path.join(fcg_dir, fcg)
        paths_fcg = convert(fp_fcg)
        paths_fcg = reduce_path(paths_fcg)
        draw_path(paths_fcg)

        if CUCKOO:
            api_calls = load_cuckoo_tracefile(fp_trace)
        elif ZEROWINE:
            api_calls = load_zerowine_tracefile(fp_trace)
        paths_exe = prepare_execution_paths(api_calls)

        print ("[o] path metrics for static fcg:")
        static_met = compute_paths_metrics(paths_fcg)

        print ("[o] path metrics for execution:")
        exe_met = compute_paths_metrics(paths_exe)

        print ("[o] execution progress:")
        prog_num = exe_met[0]*1.0/static_met[0]
        prog_len = exe_met[1]*1.0/static_met[1]
        #print ("exe_met: {0}".format(exe_met))
        #print ("static_met: {0}".format(static_met))
        print ("execution path number ratio: {0}".format(round(prog_num, 2)))
        print ("execution path length ratio: {0}".format(round(prog_len, 2)))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print ("usage: program <fcg_dir> <trace_dir>")
        sys.exit(0)
    else:
        fcg_dir = sys.argv[1]
        trace_dir = sys.argv[2]
        main(fcg_dir, trace_dir)
