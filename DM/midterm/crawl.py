import os
import csv
import json
import requests
import pandas as pd

from tqdm import tqdm
from ast import literal_eval
from bs4 import BeautifulSoup


def get_soup(url):
    respone = requests.get(url)
    return BeautifulSoup(respone.content, "html.parser")

def get_href(url, tag, attr):
    soup = get_soup(url)
    temp = soup.find_all(tag, attrs={attr})
    return [ i.find('a').attrs["href"] for i in temp ]

def to_link(base, extends):
    return [ base + extend for extend in extends ]

def get_context(urls, tt, ta, pt, pa, islist=True):
    titles, paras = [], []
    if islist == False:
        soup = get_soup(urls)
        temp = soup.find(tt, attrs={ta}).text
        titles.append(temp.strip())
        temp = soup.find(pt, attrs={pa}).text
        paras.append(temp.strip())
        return titles, paras
    for url in urls:
        soup = get_soup(url)
        temp = soup.find(tt, attrs={ta}).text
        titles.append(temp.strip())
        temp = soup.find(pt, attrs={pa}).text
        paras.append(temp.strip())
    return titles, paras

def to_csv(filename, titles, paras):
    with open(filename, 'w') as f:
        fn = ['title', 'paragraphs']
        writer = csv.DictWriter(f, fieldnames=fn)
        writer.writeheader()
        for title, para in zip(titles, paras):
            writer.writerow({'title' : title, 'paragraphs' : [para]})

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

def sv_data():
    titles, paras = [], []
    sv_base_url = "https://student.tdtu.edu.vn"
    url = "https://student.tdtu.edu.vn/chinh-sach"
    urls = to_link(sv_base_url, get_href(url, "div", "action"))
    # # Các loại học bổng 
    hb_urls = to_link(sv_base_url, get_href(urls[0], "span", "field-content"))
    temp_title, temp_para = get_context(hb_urls, "h2", "node__title", "div", "node__content static-page clearfix")
    titles.extend(temp_title), paras.extend(temp_para)
    # # Khen thưởng
    temp_title, temp_para = get_context(urls[1], "h2", "node__title", "div", "node__content static-page clearfix", islist=False)
    titles.extend(temp_title), paras.extend(temp_para)
    # # Miễn giảm học phí
    mghp_urls = to_link(sv_base_url, get_href(urls[2], "div", "action"))
    temp_title, temp_title = get_context(mghp_urls, "h2", "node__title", "div", "node__content static-page clearfix")
    # # Xác nhận sinh viên
    temp_title, temp_para = get_context(urls[3], "h2", "node__title", "div", "node__content static-page clearfix", islist=False)
    titles.extend(temp_title), paras.extend(temp_para)
    
    return titles, paras

def hv_data():
    titles, paras = [], []
    hv_base_url = "https://undergrad.tdtu.edu.vn"
    url = "https://undergrad.tdtu.edu.vn/hoc-vu"
    temp = to_link(hv_base_url, get_href(url, "div", "action"))
    urls = get_href(temp[0], "span", "MsoHyperlink")
    urls.remove(urls[1])
    temp_title, temp_para = get_context(urls, "h1", "post-title", "div", "node__content article-page clearfix")
    titles.extend(temp_title), paras.extend(temp_para)
    return titles, paras

if __name__ == "__main__":
    titles, paras = [], []
    titles, paras = sv_data()
    t, p = hv_data()
    titles.extend(t)
    paras.extend(p)
    to_csv('./data/fix_data.csv', titles, paras)
    # df = pd.read_csv('./data/data.csv', converters={'paragraphs': literal_eval})
    # df2squad(df=df, squad_version='v1.1', output_dir='./data', filename='data')
