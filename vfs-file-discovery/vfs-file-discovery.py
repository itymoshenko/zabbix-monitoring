import argparse
import fnmatch
import os
import json

__author__ = 'itymoshenko'

# parser is used to specify input options and parse arguments.
parser = argparse.ArgumentParser(description='Custom low-level discovery of files in a directory')
parser.add_argument('-p', '--path', help='Input directory path', required=True)
parser.add_argument('-n', '--name', help='Input file name', required=True)
args = parser.parse_args()

log_dir = args.path
file_name = args.name


def file_list():
    """
    Get list of files inside specific directory that matches regex and store the data into json.
    log_dir = "." - can be used for testing purpose.
    """
    data = []
    for file in os.listdir(log_dir):
        if fnmatch.fnmatch(file, file_name):
            path = os.path.join(log_dir, file)
            data.append({'{#LOGFILENAME}': path})
    json_data = json.dumps({"data": data})
    return json_data


print(file_list())
