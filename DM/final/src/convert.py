import os
import json
import argparse

def parse_argument():
    parser = argparse.ArgumentParser(description="Process command line arguments")
    parser.add_argument("-path", type=dir_path)
    parser.add_argument("-path", type=dir_path)


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")




