import argparse

'''
Assumptions:
1. File is properly formatted
2. Double quotes are used
'''
tags = []


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start


def getProp(toSearch: str, prop: str) -> list:
    comp = toSearch[toSearch.find(prop.replace(" ", "")+"=") + len(prop):]
    return comp[:find_nth(comp, "\"", 2)].replace("{", "").replace("}", "").replace("\"", "").replace("`", "").replace(
        "=", "").strip().replace("  ", "").split(" ")


def setProp(str, prop, rep):
    start = str.strip().find(" ") + 1

    if "/" in str and not " " in str:  # handle edge case (<br/> or similar)
        start = str.find("/") + 1

    if start == 0:
        start = len(str)
    return str[:start] + " {}={} ".format(prop, rep) + str[start:]


def deleteProp(toSearch, prop) -> str:
    start = toSearch.find(prop) + 1
    end = find_nth(toSearch[start + len(prop):], "\"", 2) + start + len(prop)
    return toSearch[:start - 1] + toSearch[end + 1:]


def processTag(tag: str) -> str:
    tag = tag.strip().replace("\t", "")
    newClasses = []
    if "id" in tag:
        newClasses.append(prefix + getProp(tag, "id")[0])
        tag = deleteProp(tag, "id")

    if "className" in tag:
        newClasses.extend(list(map(lambda c: prefix + c, getProp(tag, "className"))))
        tag = deleteProp(tag, "className")

    tagType = tag.strip().split(" ")[0].replace("<", "").strip()
    if any(tagType in item for item in tags):
        newClasses.append(prefix + tagType)

    if (len(newClasses) == 0):
        return tag
    classes = "{`"
    first = True
    for c in newClasses:
        if not first:
            classes += " "
        else:
            first = False
        classes += "${style." + c + "}"
    classes += "`}"

    return setProp(tag, "className", classes)


parser = argparse.ArgumentParser(description='Migrate CSS to CSS Modals',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-js", type=str, dest="js",
                    help='js or ts react file')

parser.add_argument("-css", type=str, dest="css",
                    help='Css file')

parser.add_argument("-sufix", type=str, dest="sufix", default="",
                    help='What to append to converted styles')

args = parser.parse_args()

js = args.js
css = args.css
prefix = args.sufix

with open(css, "r") as file_object:
    CSSdata = file_object.read().split("\n")
    file_object.close()

    # Go over the CSS file
    for i in range(len(CSSdata)):
        line = CSSdata[i]
        if "{" in line and "@" not in line and "/*" not in line:
            # case 1: Regular class => no change
            # case 2: id => migrate to class
            # case 3: element => migrate to class
            line = line.strip()
            CSSdata[i] = line.replace("#", ".{}".format(prefix))

            line = CSSdata[i]
            if not line.startswith("."):
                tags.append(line.split("{")[0].split(">")[0].strip())
                CSSdata[i] = ".{}".format(prefix) + line
            pass
    file_object = open(css, "w")
    file_object.writelines("\n".join(CSSdata))

    file_object.close()

with open(js, "r") as file_object:
    JSdata = file_object.read()
    file_object.close()

    start = -1
    out = ""
    wrappers = []
    for i in range(len(JSdata)):
        if JSdata[i] == '<' and JSdata[i + 1] != "/":
            start = i
        if start == -1:
            out += JSdata[i]
        elif JSdata[i] == '>' and len(wrappers) == 0:
            s = JSdata[start:i]
            # if "Car" in s:
            #     input("a")
            out += processTag(JSdata[start:i]) + ">"
            start = -1
        else: #handle escape chars
            c = JSdata[i]
            if len(wrappers)>0 and c == wrappers[-1]:
                wrappers.pop(-1)
            elif c == '\"' or c == "\'" or c == "`":
                wrappers.append(c)
            elif c == "{":
                wrappers.append("}")

    file_object = open(js, "w")
    file_object.writelines(out)
