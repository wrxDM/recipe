import re
import pandas as pd
import json
import datetime
from food_heat import get_abst


def __parse(df):
    results = {}
    for i, line in df.iterrows():
        cell = line[0]
        if not cell:
            continue
        cell = cell.replace(" ", "")
        match = re.match("([0-9]+月[0-9]+日)至([0-9]+月[0-9]+日)([早午晚]餐).*", cell)
        #     print(line)
        if match:
            begin_date = datetime.datetime.strptime("2018年" + match[1], '%Y年%m月%d日')
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
        for day, one in enumerate(line):
            date = (begin_date + datetime.timedelta(days=day)).strftime("%Y%m%d")
            if one:
                if date not in results:
                    results[date] = {}
                one_day = results[date]
                if when + where not in results[date]:
                    one_day[when + where] = []
                one_day[when + where].append(one)
    return results


def run(path):
    df = pd.read_csv(path, names=['周一', "周二", "周三", "周四", "周五"])
    df = df.fillna("")
    results = __parse(df)
    with open("resources/recipe.json", "w") as f:
        f.write(json.dumps(results))


def get_recipe(date, ww):
    # ww: when where "午餐A"
    # date = "0820"
    date = "2018" + date
    with open("resources/recipe.json", "r") as f:
        results = json.load(f)
    day_recipe = results.get(date)
    if ww in day_recipe:
        recipe = day_recipe[ww]
    else:
        recipe = day_recipe[ww[:2] + 'AB']
    return get_abst(recipe)


if __name__ == '__main__':
    # run("resources/知乎三餐菜单 - 工作表1.csv")
    print(get_recipe("0821", "午餐A"))