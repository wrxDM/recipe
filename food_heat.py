import requests
from lxml import etree
import re
import time
import logging

logging.getLogger("food_heat")
logging.basicConfig(level="INFO", format='%(asctime)s %(levelname)s %(message)s',)

headers = {'User-Agent': "Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko"}


def match(food, foods):
    for food_ in foods:
        if food in food_ or food_ in food:
            return True
    return False


def norm(s):
    s = s.replace("又叫", "")
    s = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", " ", s)
    return s.split()


def get_heat(recipes):
    url = "http://www.boohee.com/food/search?keyword="
    result = {}
    for food in set(recipes):
        if food in ["水果"]:
            continue
        responds = requests.get(url + food)
        html = etree.HTML(responds.text)
        try:
            title = html.xpath("//*[@id='main']/div/div[1]/ul/li[1]/div[2]/h4/a/text()")[0]

            heat = html.xpath("//*[@id='main']/div/div[1]/ul/li[1]/div[2]/p/text()")[0]

            # if match(food, norm(title)):
            #     print("food: {} foods: {} heat: {}".format(food, title, heat))
            #     result.append({"food": food, "find": title, "head": heat, "match": 1})
            # else:
            #     print("NOT MATCH! food: {} foods: {} heat: {}".format(food, title, heat))
            #     result.append({"food": food, "find": title, "head": heat, "match": 0})
            result[food] = heat
        except:
            logging.info("food not found: {}".format(food))
            # result.append({"food": food, "find": "", "head": "", "match": 0})
        time.sleep(3)
    return result


if __name__ == '__main__':
    recipes = """一品排骨	虎眼丸子	川香酸菜鱼	樟茶鸭	风味香酥鸡
    干煸双豆	木须肉	小炒肉	香辣毛血旺	干锅散花
    水煮肉片	干锅千叶豆腐	肉丝豇豆	蒜苗炒腊肉	鱼香肉丝
    麻酱茄子	家常土豆丝	什锦花生米	烧二冬	豉油包菜
    木耳蒯菜	圆白菜粉条	三色藕片	香菇油菜	素烧茄子
    米饭	米饭	米饭	米饭	米饭
    馒头花卷	馒头花卷	馒头花卷	馒头花卷	馒头花卷
    玉米发糕	煎饺	手撕饼	芝麻烧饼	鸡蛋饼
    疙瘩汤	绿豆汤	蛋花汤	酸梅汤	银耳汤
    素炒饼	蒸玉米	豆角焖面	蒸杂粮	爽口凉面
    时令水果	时令水果	时令水果	时令水果	时令水果""".split()
    heats = get_heat(recipes[:3])
    for k in heats:
        print("food: {} heat: {}".format(k, heats[k]))

