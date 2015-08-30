import json
import sys
import os

ORG = True
FILTER = False

def main(fp_path):
    fp = open(fp_path, 'r')
    cont = fp.read()
    fp.close()
    cont_dict = json.loads(cont)
    if ORG:
        proc = cont_dict["behavior"]["processes"][1]
    else:
        proc = cont_dict["processes"][0]
    calls = proc["calls"]
    name = proc["process_name"]

    calls_filter = set()
    for apicall in calls:
        if apicall["category"] == "system":
            if FILTER:
                pass
            else:
                calls_filter.add(apicall["api"])
        else:
            calls_filter.add(apicall["api"])
    print ("apis number: {0}".format(len(calls_filter)))
    #print ("apis: {0}".format(calls_filter))
    api_calls = []
    for api_call in calls_filter:
        api_calls.append(api_call)
    res = {"name":name, "api_calls":api_calls}
    fp = open(os.path.basename(fp_path)+".proc",'w')
    res = json.dumps(res, indent=4)
    fp.write(res)
    fp.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("usage: program <cuckooreport>")
        sys.exit(0)
    else:
        fp_path = sys.argv[1]
        main(fp_path)
