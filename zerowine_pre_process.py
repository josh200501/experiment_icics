import sys
import re

def check_if_start(line):
    target = r"Starting process"
    if re.search(target, line, re.I):
        #print ("line: {0}".format(line))
        if "malware.exe" in line:
            return True
    return False

def check_api_call(line):
    target = r"Call to (\b\w*\b)\s*\("
    res = re.search(target, line, re.I)
    if res:
        #print res.group()
        return res.groups()[0]
    return False

def load_zerowine_tracefile(fp_trace):
    fp = open(fp_trace, 'r')
    start = False
    api_calls = set()
    api_call = ""
    j = 0
    while True:
        j += 1
        line = fp.readline()
        if not line:
            break
        if not start:
            if check_if_start(line):
                start = True
        else:
            api_call = check_api_call(line)
            if api_call:
                api_calls.add(api_call)
    fp.close()
    #print ("all lines: {0}".format(j))
    #print ("api calls: {0}".format(api_calls))
    #print ("number of calls: {0}".format(len(api_calls)))
    return api_calls

def dummy_main(fp_trace):
    pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("usage: program <zerowine_tracefile>")
        sys.exit(0)
    else:
        fp_trace = sys.argv[1]
        dummy_main(fp_trace)
