#! /usr/bin/env python
# coding:utf-8

# built-in packages
import json

# third-part packages

# custom packages

"""
作者：hzzhu2@iflytek.com
功能：将涉及json文本中的某一句转换成指定html格式文本
时间：2019/08/08
"""

def convertFormatBetweenJsonAndPython(jsonfilepath):
    with open(jsonfilepath, 'r', encoding='UTF-8') as jsoncontent: # Error2
        # pydict = json.loads(jsoncontent) # Error1
        pydict = json.load(jsoncontent)
        print(pydict["id"])

    if pydict['type'] == "Listening_Script":
        for item1 in pydict["questions"]:
            for item2 in item1["answers"]:
                item2["english"] = convertJsonToHtml_1(item2["english"])

        for item3 in pydict["tail"]:
            item3["english"] = convertAllWord(item3["english"])

    if pydict["type"] == "Role Play":
        for item1 in pydict["questions"]:
            item1["english"] = convertAllWord(item1["english"])

    if pydict["type"] == "Speaking_Model Speech_1" or pydict["type"] == "Speaking_Model Speech_2":
        for item1 in pydict["questions"]:
            item1["english"] = convertAllWord(item1["english"])

    newjsoncontent = json.dumps(pydict)
    # with open(r"E:/paper.json", "w", encoding='UTF-8') as f:
    with open(jsonfilepath, "w", encoding='UTF-8') as f:
        f.writelines(newjsoncontent)
        f.flush()

    print("Convert OK")


# Convert "①　If you show pet-induced symptoms, you should reduce stress."
# To "<span><font color=\"black\">①  If </font><font color=\"black\">you </font><font color=\"black\">show </font>
#     <font color=\"black\">pet-induced </font><font color=\"black\">symptoms, </font><font color=\"black\">you </font>
#     <font color=\"black\">should </font><font color=\"black\">reduce </font><font color=\"black\">stress. </font></span>"
def convertJsonToHtml_1(jsoninfo):
    text = jsoninfo.split()
    flag = text[0] +"  "+ text[1]
    textpart = text[2:]
    textpart.reverse() # reverse() and append() have no return
    textpart.append(flag)
    textpart.reverse()
    newtext = "<span>{}</span>".format("".join(['<font color="blue">{} </font>'.format(i) for i in textpart]))
    print(newtext)
    # return newtext



# Convert "①　If you show pet-induced symptoms, you should reduce stress."
# To "<span>①  <font color=\"black\">If </font><font color=\"black\">you </font><font color=\"black\">show </font>
#     <font color=\"black\">pet-induced </font><font color=\"black\">symptoms, </font><font color=\"black\">you </font>
#     <font color=\"black\">should </font><font color=\"black\">reduce </font><font color=\"black\">stress. </font></span>"
def convertJsonToHtml_2(jsoninfo):
    text = jsoninfo.split()
    flag = text[0]
    textpart = text[1:]
    newtext = "<span>{0} {1}</span>".format(flag, "".join(['<font color="blue">{} </font>'.format(i) for i in textpart]))
    # print(newtext)
    return newtext


# Convert "What was found in the studies mentioned in the passage?  Answer by choosing one of the four choices you will hear."
# To "<span><font color=\"black\">It </font><font color=\"black\">was </font><font color=\"black\">found </font>
#     <font color=\"black\">that </font><font color=\"black\">the </font><font color=\"black\">subjects </font>
#     <font color=\"black\">who </font><font color=\"black\">watched </font><font color=\"black\">the </font>
#     <font color=\"black\">fish </font><font color=\"black\">were </font><font color=\"black\">much </font>
#     <font color=\"black\">more </font><font color=\"black\">relaxed </font><font color=\"black\">than </font>
#     <font color=\"black\">those </font><font color=\"black\">who </font><font color=\"black\">did </font><font color=\"black\">not </font>
#     <font color=\"black\">watch </font><font color=\"black\">the </font><font color=\"black\">fish </font><font color=\"black\">prior </font>
#     <font color=\"black\">to </font><font color=\"black\">the </font><font color=\"black\">surgery. </font></span>"
def convertAllWord(jsoninfo):
    text = jsoninfo.split()
    newtext = "<span>{}</span>".format(
                        "".join(['<font color="blue">{} </font>'.format(i) for i in text]))
    # print(newtext)
    return newtext



if __name__ == '__main__':
    paths = ["E:/94143/ls-94143-1", \
             "E:/94143/ls-94143-2", \
             "E:/94143/ls-94143-3", \
             "E:/94143/ls-94143-4", \
             "E:/94143/ls-94143-5", \
             "E:/94143/rp-94143-1", \
             "E:/94143/rp-94143-2", \
             "E:/94143/rp-94143-3", \
             "E:/94143/rp-94143-4", \
             "E:/94143/rp-94143-5", \
             "E:/94143/smp1-94143-1", \
             "E:/94143/smp1-94143-2", \
             "E:/94143/smp1-94143-3", \
             "E:/94143/smp1-94143-4", \
             "E:/94143/smp1-94143-5", \
             "E:/94143/smp2-94143-1", \
             "E:/94143/smp2-94143-3", \
             "E:/94143/smp1-94143-5", \
             "E:/94145/ls-94145-1", \
             "E:/94145/ls-94145-2", \
             "E:/94145/ls-94145-3", \
             "E:/94145/ls-94145-4", \
             "E:/94145/ls-94145-5", \
             "E:/94145/rp-94145-1", \
             "E:/94145/rp-94145-2", \
             "E:/94145/rp-94145-3", \
             "E:/94145/rp-94145-4", \
             "E:/94145/rp-94145-5", \
             "E:/94145/smp1-94145-1", \
             "E:/94145/smp1-94145-2", \
             "E:/94145/smp1-94145-3", \
             "E:/94145/smp1-94145-4", \
             "E:/94145/smp1-94145-5", \
             "E:/94145/smp2-94145-1", \
             "E:/94145/smp2-94145-4"]
    for route in paths:
        path = r"{}/paper.json".format(route)
        convertFormatBetweenJsonAndPython(path)

    # jsonwords = "①　If you show pet-induced symptoms, you should reduce stress."
    # convertJsonToHtml_1(jsonwords)





# bugs 处理
'''
  Error1: loads --> load
  File "E:/ImportantFiles/create_user_demo/json_process.py", line 25, in convertformatbetweenjsonandpython
    pydict = json.loads(jsoncontent)
  File "D:\python36\lib\json\__init__.py", line 348, in loads
    'not {!r}'.format(s.__class__.__name__))
TypeError: the JSON object must be str, bytes or bytearray, not 'TextIOWrapper
'''

'''
    Error2: open(filepath, "mode") --> open(filepath, "mode", encoding="utf-8")
    UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 in position 205: illegal multibyte sequence
'''


# 操作记录信息
"""
ls-94143-1
Convert OK
ls-94143-2
Convert OK
ls-94143-3
Convert OK
ls-94143-4
Convert OK
ls-94143-5
Convert OK
rp-94143-1
Convert OK
rp-94143-2
Convert OK
rp-94143-3
Convert OK
rp-94143-4
Convert OK
rp-94143-5
Convert OK
smp-94143-1_1
Convert OK
smp-94143-2_1
Convert OK
smp-94143-3_1
Convert OK
smp-94143-4_1
Convert OK
smp-94143-5_1
Convert OK
smp-94143-1_2
Convert OK
smp-94143-3_2
Convert OK
smp-94143-5_1
Convert OK
ls-94145-1
Convert OK
ls-94145-2
Convert OK
ls-94145-3
Convert OK
ls-94145-4
Convert OK
ls-94145-5
Convert OK
rp-94145-1
Convert OK
rp-94145-2
Convert OK
rp-94145-3
Convert OK
rp-94145-4
Convert OK
rp-94145-5
Convert OK
smp-94145-1_1
Convert OK
smp-94145-2_1
Convert OK
smp-94145-3_1
Convert OK
smp-94145-4_1
Convert OK
smp-9143-1_1
Convert OK
smp-94145-1_2
Convert OK
smp-94145-4_2
Convert OK
"""