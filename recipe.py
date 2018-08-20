import re
import pandas as pd
import json

days = ['周一', "周二", "周三", "周四", "周五"]


def parse(df):
    results = {}
    for i, line in df.iterrows():
        cell = line[0]
        if not cell:
            continue
        cell = cell.replace(" ", "")
        match = re.match("([0-9]+月[0-9]+日)至([0-9]+月[0-9]+日)([早午晚]餐).*", cell)
        #     print(line)
        if match:
            date = match[1]
            when = match[3]
            if "A" in cell:
                where = "A"
            elif "B" in cell:
                where = "B"
            else:
                where = "AB"
            continue
        if "周一" == cell:
            continue
        for day, one in zip(days, line):
            if one:
                if date + " " + day not in results:
                    results[date + " " + day] = {}
                one_day = results[date + " " + day]
                if when + where not in results[date + " " + day]:
                    one_day[when + where] = []
                one_day[when + where].append(one)
    return results


def run(path):
    df = pd.read_csv(path, names=['周一', "周二", "周三", "周四", "周五"])
    df = df.fillna("")
    results = parse(df)
    with open("resources/recipe.json", "w") as f:
        f.write(json.dumps(results))


def get_recipe(s):
    # s = "0820-1"
    day = days[int(s.split("-")[1])]
    date = "{}月{}日".format(int(s[:2]), int(s[2:4]))
    with open("recipe.json", "r") as f:
        results = json.load(f)
    return results.get(date + " " + day)


if __name__ == '__main__':
    run("resources/知乎三餐菜单 - 工作表1.csv")