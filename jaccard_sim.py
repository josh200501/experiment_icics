"""
This program convert function call graph (produced by IDA Pro) to graphviz format.
"""
import sys
import json
from zerowine_pre_process import load_zerowine_tracefile


DEBUG = False
CUCKOO = True
ZEROWINE = False
CUCKOOAPIS = "cuckooapis.txt"
CUCKOO_ORG = False

STATIC_APIS = set()
EXECUT_APIS = set()
MONITOR_APIS = set()
DUMMY_APIS = set()

DUMMY_PATH = "dummy.gdl"

def init_monitor_apis():
    global MONITOR_APIS
    fp = open(CUCKOOAPIS, 'r')
    cont = fp.read()
    fp.close()
    cont_dict = json.loads(cont)
    apis = cont_dict["apis"]
    MONITOR_APIS = set(apis)
    return apis

def convert(fp_path):
    global STATIC_APIS
    fp = open(fp_path, 'r')
    while True:
        line = fp.readline()
        if not line:
            break
        elif line.startswith('node'):
            label = line.split(' ')[5][1:-1]
            " eliminate user function "
            if label.startswith("sub_"):
                pass
            else:
                STATIC_APIS.add(label)

def load_dummy():
    global DUMMY_APIS
    fp = open(DUMMY_PATH, 'r')
    while True:
        line = fp.readline()
        if not line:
            break
        elif line.startswith('node'):
            label = line.split(' ')[5][1:-1]
            if label.startswith("sub_"):
                pass
            else:
                DUMMY_APIS.add(label)


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
    if DEBUG:
        print ("exe apis number: {0}".format(len(calls_filter)))
        print ("apis: {0}".format(calls_filter))
    return calls_filter

def load_cuckoo_apicalls(fp_apicalls):
    "load processed api calls"
    fp = open(fp_apicalls, 'r')
    cont = fp.read()
    fp.close()
    cont_dict = json.loads(cont)
    calls = cont_dict["api_calls"]
    if DEBUG:
        print ("exe apis number: {0}".format(len(calls)))
        print ("apis: {0}".format(calls))
    return calls

def init_execut_apis(fp_trace):
    "get apis in execution path"
    global EXECUT_APIS
    if CUCKOO:
        if CUCKOO_ORG:
            api_calls = load_cuckoo_tracefile(fp_trace)
        else:
            api_calls = load_cuckoo_apicalls(fp_trace)
    elif ZEROWINE:
        api_calls = load_zerowine_tracefile(fp_trace)
    apis_exe = set()
    for api in api_calls:
        apis_exe.add(api)
    EXECUT_APIS = apis_exe


def main(fp_fcg, fp_trace):
    load_dummy()
    convert(fp_fcg)
    init_execut_apis(fp_trace)

    if DEBUG:
        print "dummy===================="
        print DUMMY_APIS
        print "static===================="
        print STATIC_APIS
        print "execut===================="
        print EXECUT_APIS

    FCG_SET_WITH_NOISE = STATIC_APIS
    FCG_SET_WITHOUT_NOISE = STATIC_APIS - DUMMY_APIS

    if True:
        print "===================="
        print len(FCG_SET_WITH_NOISE)
        print "===================="
        print len(FCG_SET_WITHOUT_NOISE)
        print "===================="
        print len(EXECUT_APIS)

    jaccard_siml_noise = len(FCG_SET_WITH_NOISE & EXECUT_APIS)*1.0/len(FCG_SET_WITH_NOISE ^ EXECUT_APIS)
    jaccard_siml_nnoise = len(FCG_SET_WITHOUT_NOISE & EXECUT_APIS)*1.0/len(FCG_SET_WITHOUT_NOISE ^ EXECUT_APIS)

    print ("execution progress".center(2*30,'='))
    print "exe ratio noise (jaccard similarity):".rjust(30),"{0}".format(round(jaccard_siml_noise, 3)).ljust(30)
    print "exe ratio nnoise (jaccard similarity):".rjust(30),"{0}".format(round(jaccard_siml_nnoise, 3)).ljust(30)
    #print "exe ratio noise (jaccard similarity):".rjust(30),"{0}".format((jaccard_siml_noise)).ljust(30)
    #print "exe ratio nnoise (jaccard similarity):".rjust(30),"{0}".format((jaccard_siml_nnoise)).ljust(30)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: program <gdlfile> <tracefile>")
        sys.exit(1)
    else:
        fp_fcg = sys.argv[1]
        fp_trace = sys.argv[2]
        main(fp_fcg, fp_trace)


