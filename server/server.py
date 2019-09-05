import tornado.ioloop
import tornado.web
import json
import os
import time
import webbrowser
import threading
from datasetOrm import *

with open('../web/src/config/config.json','r')as f:
    js=json.loads(f.read())
    serverport=js['port']
    sip=js['ip']
class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Credentials', 'true')

    def get(self):
        self.render('../web/dist/index.html')

    def post(self):
        self.set_default_headers()
        js = json.loads(self.request.body)
        print(js)
        month_money = Food.month_sales * Food.price
        limits = js.get('num')
        if limits == -1:
            doans = False
            limits = 10
        else:
            doans = True
        quer = Food.select(Food, Shop.id, Shop.latitude, Shop.longitude, Shop.name, Shop.address,
                           month_money.alias('month_money'),
                           Food.rating.alias('rating'),
                           Food.month_sales.alias('month_sales'),
                           Food.price.alias('price')
                           ).join(Shop, on=(Food.id == Shop.id))
        if js.get('op') == 'query':
            # 食品筛选 店铺筛选
            if len(js['foodname']) != 0:
                quer = quer.where(Food.food_name % f"*{js['foodname']}*")
            if len(js['shopname']) != 0:
                quer = quer.where(Shop.name % f"*{js['shopname']}*")
            if len(js['address']) != 0:
                quer = quer.where(Shop.address % f"*{js['address']}*")
            res = {
                'ans': [],
                'top10': []
            }
            if js['type'] == False:
                # 只显示有关店铺
                quer = quer.select(Shop.id, Shop.latitude, Shop.longitude, Shop.name, Shop.address,
                                   fn.SUM(month_money).alias('month_money'),
                                   fn.AVG(Food.rating).alias('rating'),
                                   fn.SUM(Food.month_sales).alias('month_sales'),
                                   fn.AVG(Food.price).alias('price')
                                   ).group_by(Shop.id)
            if js['heat'] == '无':
                if doans:
                    for item in quer:
                        res['ans'].append([item.shop.longitude, item.shop.latitude, 1])
                quer = quer.limit(limits)
            elif js['heat'] == '月销量':
                if doans:
                    for item in quer:
                        res['ans'].append([item.shop.longitude, item.shop.latitude, item.month_sales])
                quer = quer.order_by(SQL('month_sales').desc()).limit(limits)
            elif js['heat'] == '月销售额':
                if doans:
                    for item in quer:
                        res['ans'].append([item.shop.longitude, item.shop.latitude, item.month_money])
                quer = quer.order_by(SQL('month_money').desc()).limit(limits)
            elif js['heat'] == '价格':
                if doans:
                    for item in quer:
                        res['ans'].append([item.shop.longitude, item.shop.latitude, item.price])
                quer = quer.order_by(SQL('price').desc()).limit(limits)
            elif js['heat'] == '评分':
                if doans:
                    for item in quer:
                        res['ans'].append([item.shop.longitude, item.shop.latitude, item.rating])
                quer = quer.order_by(SQL('rating').desc()).limit(limits)

            for item in quer.dicts().iterator():
                res['top10'].append(item)

            midd = 0
            all_num = len(res['ans'])
            for item in res['ans']:
                midd += item[2] / all_num
            res['midd'] = int(midd + 1)
            print(res['midd'])
            self.write(json.dumps(res))
            print('finish')
            return
        self.write('end')


settings = {
    "static_path": "../web/dist/static",
}


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ], **settings)


def start_browser():
    time.sleep(5)
    webbrowser.open(f"http://{sip}:{serverport}")


if __name__ == "__main__":
    app = make_app()
    app.listen(serverport)
    # build构建后 直接使用Python作为http server拉起浏览器启动
    # threading.Thread(target=start_browser).start()
    print('open web finish')
    tornado.ioloop.IOLoop.current().start()
