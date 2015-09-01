#coding:utf8
import json
import sys
import os

reload(sys)
sys.setdefaultencoding("gbk")

ORG = True
FILTER = False
DST = False

def main(fp_path):
    fp = open(fp_path, 'r')
    cont = fp.read()
    fp.close()
    cont_dict = json.loads(cont)
    sample_info = cont_dict["target"]
    if sample_info["category"] == "file":
        file_info = sample_info["file"]
        file_name = file_info["name"]
        file_md5 = file_info["md5"]
    else:
        print ("sample is not a file.")
        sys.exit(0)

    processes = cont_dict["behavior"]["processes"]
    for process in processes:
        if process["process_name"] == file_name:
            file_proc = process
            break
    calls = file_proc["calls"]

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

    res = {"name":file_name, "md5":file_md5, "api_calls":api_calls}
    res_dir = os.path.dirname(fp_path)
    res_name = file_name+'_'+file_md5+".json"
    if DST:
        res_dir_name = os.path.join(res_dir, res_name)
    else:
        res_dir_name = res_name
    fp = open(res_dir_name,'w')
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
