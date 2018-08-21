import requests
from lxml import etree
import re
import time
import logging
import json

logging.getLogger("food_heat")
logging.basicConfig(level="INFO", format='%(asctime)s %(levelname)s %(message)s', )

headers = {'User-Agent': "Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko"}


def __get_html(url):
    try:
        responds = requests.get(url)
        html = etree.HTML(responds.text)
        return html
    except:
        print("[WARNING] get_html return None: {}".format(url))


# def match(food, foods):
#     for food_ in foods:
#         if food in food_ or food_ in food:
#             return True
#     return False


# def norm(s):
#     s = s.replace("又叫", "")
#     s = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", " ", s)
#     return s.split()


def __find_max(foods):
    top = {}
    for food in foods:
        detail = foods[food]
        for key in detail:
            if key == "title": continue
            if key not in top:
                top[key] = {"value": detail[key], "food": food}
            else:
                if top[key]["value"] < detail[key]:
                    top[key] = {"value": detail[key], "food": food}
    return top


def get_abst(foods):
    with open("resources/nutrition.json") as f:
        nutrition = json.load(f)
    top = __find_max({food: nutrition.get(food, {}) for food in foods})
    result = {k: "" for k in foods}
    for key in top:
        if result[top[key]['food']] == "":
            result[top[key]['food']] = "富含"
        else:
            result[top[key]['food']] += "、"
        result[top[key]['food']] += re.sub("[(].*[)]", "", key)

    return result


def get_heat(foods):
    with open("resources/nutrition.json") as f:
        nutrition = json.load(f)
    results = {}
    for food in foods:
        detail = nutrition.get(food, {})
        heat = detail.get("热量", "")
        if "水果" in food:
            heat = ""
        results[food] = heat
    return results


def get_nutrition(recipes):
    url = "http://www.boohee.com/food/search?keyword="
    base_url = "http://www.boohee.com"
    results = {}
    for food in set(recipes):
        if food in ["水果"]:
            continue
        results[food] = {}
        html = __get_html(url + food)
        if html is None:
            continue
        try:
            title = html.xpath("//*[@id='main']/div/div[1]/ul/li[1]/div[2]/h4/a/text()")[0]
            results[food]["title"] = title

            detail_url = html.xpath("//*[@id='main']/div/div[1]/ul/li[1]/div[2]/h4/a/@href")[0]

            html = __get_html(base_url + detail_url)
            if html is None:
                continue

            heat = html.xpath('//*[@id="main"]/div/div[2]/div[2]/div/dl[2]/dd[1]/span[2]/span/text()')[0]
            results[food]["热量"] = float(heat)
            for i in [2, 3, 4]:
                for j in [1, 2]:
                    try:
                        k = html.xpath(
                            "//*[@id='main']/div/div[2]/div[2]/div/dl[{i}]/dd[{j}]/span[1]/text()".format(i=i, j=j))[0]
                        v = html.xpath(
                            "//*[@id='main']/div/div[2]/div[2]/div/dl[{i}]/dd[{j}]/span[2]/text()".format(i=i, j=j))[0]
                        results[food][k] = float(v) if v != "一" else 0
                    except:
                        continue
        except Exception as e:
            print(e)
        time.sleep(1)
    print('Finished!')
    return results


def init(foods):
    with open("resources/nutrition.json", "r") as f:
        try:
            foods_done = set(json.load(f).keys())
            details = json.load(f)
        except:
            foods_done = []
            details = {}
    foods = [food for food in foods if food not in foods_done]
    details.update(get_nutrition(foods))
    with open("resources/nutrition.json", "w") as f:
        f.write(json.dumps(details))
    print("Write nutrition.json Finished!")


if __name__ == '__main__':
    recipes = []
    with open("resources/recipe.json") as f:
        recipe = json.load(f)
    #
    foods = set()
    for day in ["0820", "0821", "0822", "0823", "0824"]:
        for when in recipe["2018" + day]:
            for food in recipe["2018" + day][when]:
                # foods[food] = foods.get(food, 0) + 1
                foods.add(food)
    # details = get_nutrition(recipes[:3])
    # for k in details:
    #     print("food: {} details: {}".format(k, details[k]))
    init(foods)
    abst = get_abst(['一品排骨', "干煸双豆", "米饭"])
    print(abst)
