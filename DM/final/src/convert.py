import json
import argparse

parser = argparse.ArgumentParser(description="convert from utf-8-sig to utf-8")
parser.add_argument("input_file", metavar="input.json", type="str", nargs="+", help="put utf-8-sig path here")
parser.add_argument("output_file", metavar="output.json", type="str", help="name of utf-8 json file")
args = parser.parse_args()

with open(args.input_file, "r", encoding="utf-8") as reader:
    data = json.load(reader)

with open(args.output_file, "w", encoding="utf-8") as writer:
    json.dump(writer, data, indent=4, ensure_ascii=False)

