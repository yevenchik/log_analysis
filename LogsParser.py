import argparse
import os
import json


def parse_args():
    """Read arguments from command line.
    received full path to metry directory and full path ro json configuration File
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="directory holding the metry files", type=str)
    parser.add_argument("configFile", help="configuration files ", type=str)
    return parser.parse_args()


def count_msg_in_files(msg, file_paths):
    """Counts number of sentence appearances in list of files."""
    counter = 0
    for logFile in file_paths:
        with open(logFile) as f:
            counter += (f.read()).count(msg)
    return counter


def get_files_fp(dir2parse):
    files = []
    _rec_get_files_in_dir(files, dir2parse)
    return files


def _rec_get_files_in_dir(files_paths, dir2parse):
    for root, dirs, files in os.walk(dir2parse):
        for file in files:
            file_pull_path = os.path.join(root, file)
            if file_pull_path not in files_paths:
                files_paths.append(file_pull_path)
        for dir2parse in dirs:
            _rec_get_files_in_dir(files_paths, os.path.join(root, dir2parse))


def main():
    """
    main function.
    """
    args = parse_args()

    filesPf = get_files_fp(args.dir)
    if not filesPf:
        print("directory", args.dir, "doesn't exist or empty")
        return

    with open(args.configFile) as file:
        countersDict = {msg: (count_msg_in_files(msg, filesPf)) for msg in json.load(file)["str2Count"]}

    for logMsg in countersDict:
        print("Msg '", logMsg, "' found ", countersDict[logMsg], "times in files")



#def count_all_msgs():
#    args = parse_args()
#    counters = []
#
#     with open(args.configFile) as file:
#         logMsgs = json.load(file)["str2Count"]
#
#     for root, dirs, files in os.walk(args.dir):
#         for msg in logMsgs:
#             counter = 0
#             for logFile in files:
#                 with open(os.path.join(root, logFile)) as f:
#                     counter += f.read().count(msg)
#             counters.append(counter)
#             print("Msg '", msg, "' found ", counter, "times in metry")


if __name__ == '__main__':
    main()