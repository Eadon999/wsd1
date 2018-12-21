
import pandas as pd
import re

def feature_list(path):
    with open(path) as f:
        l = f.readlines()
    l_replace = [re.sub("[(\'\')0-9\s]", "", s).rstrip(",,") for s in l]
    l_tolist = [s.split(",,") for s in l_replace]
    return l_tolist

def feature_regular(path):
    with open(path) as f:
        l = f.readlines()
    l_replace = [re.sub("[(\'\')0-9\s]", "", s).rstrip(",,") for s in l]
    l_regular = [s.replace(",,", "|") for s in l_replace]
    return l_regular

if __name__ == "__main__":
    import sys
    args = sys.argv
    l = feature_list(args[1])
    print(l)
    l = feature_regular(args[1])
    print(l)
