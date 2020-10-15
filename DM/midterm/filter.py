import os
import csv
import json
import requests
import pandas as pd

from tqdm import tqdm
from ast import literal_eval

def df2squad(df, squad_version="v1.1", output_dir=None, filename=None):
    json_data = {}
    json_data["version"] = squad_version
    json_data["data"] = []

    for idx, row in tqdm(df.iterrows()):
        temp = {"title": row["title"], "paragraphs": []}
        for paragraph in row["paragraphs"]:
            temp["paragraphs"].append({"context": paragraph, "qas": []})
        json_data["data"].append(temp)

    if output_dir:
        with open(os.path.join(output_dir, "{}.json".format(filename)), "w", encoding="utf-8") as outfile:
            json.dump(json_data, outfile, ensure_ascii=False)

df = pd.read_csv('./data/finaldata.csv', converters={'paragraphs': literal_eval})
df2squad(df, output_dir='./data',filename='final_data')
