i
port json
import argparse

parser = argparse.ArgumentParser(description="Split SQuAD vi")
parser.add_argument("input_file", metavar="file.json", type=str, nargs="+", help="file input")
parser.add_argument("begin", metavar="N", type=int, nargs="+", help="split squad from context num N")
parser.add_argument("end", metavar="E", type=int, nargs="+", help="split squad end at context num E")
parser.add_argument("output_file", metavar="out.json", type=str, nargs="+", help="output file")
args = parser.parse_args()

with open(args.input_file, "r", encoding="utf-8") as reader:
    data = json.load(reader)["data"]

contexts = data[0]["paragraphs"][args.begin:args.end]
lite = {
    "data": [
        {
            "title": "translated",
            "paragraphs": [context for context in contexts]
        }
    ]
}

with open(args.output_file, "w", encoding="utf-8") as writer:
    json.dump(lite, writer, indent=4, ensure_ascii=False) 
