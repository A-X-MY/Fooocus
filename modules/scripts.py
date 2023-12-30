import os
import json
import random
import re
import requests
from bs4 import BeautifulSoup

listdynamice = {}


listdynamice = {}

class Script:
    def __init__(self):
        pass

    


def loadjsonfiles(path, dic):
    files = os.listdir(path)
    for item in files:
        if item.endswith(".json"):
            filepath = os.path.join(path, item)
            filename = os.path.splitext(item)[0]
            with open(filepath, "r", encoding="utf-8-sig") as f:
                res = json.loads(f.read())
                dic[filename] = res

def loadRandomList(pathrandom):
    jsonlist = []
    files = os.listdir(pathrandom)
    for item in files:
        if item.endswith(".json"):
            filepath = os.path.join(pathrandom, item)
            with open(filepath, "r", encoding="utf-8-sig") as f:
                jsondata = json.loads(f.read())
                jsonlist.extend(jsondata)
    return jsonlist

def traverse_dict(d, clsName=None):
    for k, v in d.items():
        if isinstance(v, dict):
            traverse_dict(v, k)
        else:
            listdynamice[clsName] = d
            break

def get_content(text):
    try:
        localtran = "https://dict.youdao.com/w/"
        response = requests.get(localtran + text)
        if response.status_code == 200:
            return response.text
        else:
            print(f"err_code：{response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"err：{e}")
        return None

def tanslate(text):
    html_content = get_content(text)
    if html_content is not None:
        dom = BeautifulSoup(html_content, 'html.parser')
        ydhtml = dom.find('div', id='fanyiToggle')
        if ydhtml:
            div = ydhtml.find('div', class_='trans-container')
            childhtml = div.find_all('p')
            return childhtml[1].get_text()
        shot = dom.find('a', class_='search-js')
        if shot:
            return shot.text.strip()
        tWebTrans = dom.find('div', id='tWebTrans')
        if tWebTrans is not None:
            span = tWebTrans.find('span')
            text = span.next_sibling.replace("\n", "")
            return text.strip()
    return None

def LoadTagsFile(path1, path2):
    dic = {}
    loadjsonfiles(path1, dic)
    loadjsonfiles(path2, dic)
    traverse_dict(dic)
    obj = json.dumps(dic, ensure_ascii=False)
    return obj

def extract_classesTags(prompt):
    pattern = r'#\[(.*?)\]'
    matches = re.findall(pattern, prompt)
    if len(matches) == 0:
        return None
    for match in matches:
        arr = match.split('#')
        randlist = []
        for classesKey in arr:
            if classesKey in listdynamice:
                randlist.append(listdynamice[classesKey])
        if len(randlist) == 0:
            continue
        random.seed(getSeed())
        rdindex = random.randint(0, len(randlist) - 1)
        newtext = ''
        for item in randlist[rdindex]:
            newtext += randlist[rdindex][item] + '#'
        prompt = prompt.replace(match, newtext, 1)
    return prompt

def extract_tags(prompt):
    pattern = r'#\[(.*?)\]'
    matches = re.findall(pattern, prompt)
    text = prompt
    if len(matches) == 0:
        return None
    for item in matches:
        arr = item.split('#')
        random.seed(getSeed())
        rdindex = random.randint(0, len(arr) - 1)
        rdtext = arr[rdindex]
        text = re.sub(pattern, rdtext, text, count=1)
    return text

def getSeed():
    seed = random.random()
    return seed
