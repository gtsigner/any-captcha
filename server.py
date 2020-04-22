import math

from flask import Flask
from flask import request, logging, make_response, jsonify

from gee import crack_gee
from utils.download import download_image_as_jpeg, download_image_as_jpg
import utils.crack_qq as crack_qq
import os
import uuid
import asyncio
import time

loop = asyncio.new_event_loop()
app = Flask(__name__)
logger = logging.create_logger(app)


@app.route('/')
def root():
    return 'godtoy\'s python api , Use WeChat：zhaojunlike to contact me'


@app.route('/tx/image', methods=['POST'])
def image():
    try:
        json = request.get_json()
        url = json['url']
        # 1.下载图片
        file = os.path.join(os.path.dirname(__file__), "tmp", str(uuid.uuid4()) + "_captcha.jpg")
        _, code = loop.run_until_complete(download_image_as_jpeg(url, file))
        if not code == 200:
            return make_response(jsonify({'message': "解析失败Code:" + code}), 400)
        # 2.识别图片
        res = crack_qq.qq_mark_pos(file)
        dis = res.x.values[0]
        tacks = crack_qq.get_track_list(dis)  # 模拟加速度
        app.logger.debug("解析成功,需要移动距离:{},点数:{}".format(dis, len(tacks)))
        os.remove(file)  # 解析后删除文件就可以了
        return make_response(jsonify({'message': "解析成功", 'data': {'x': dis, 'list': tacks, 'url': url}}), 200)
    except Exception as e:
        print("e：", e)
        return make_response(jsonify({'message': "解析失败,请重新尝试"}), 400)


@app.route("/gee/slider/offset", methods=["POST"])
def gee_slider_offset():
    json = request.get_json()
    bg = json.get("bg")
    full_bg = json.get('full_bg')
    need_remove = json.get("remove")
    if bg == "" or bg is None or full_bg == "" or full_bg is None:
        return make_response({'message': "请提交文件URL"}, 400)

    name = str(uuid.uuid4())
    bg_path = os.path.join(os.path.dirname(__file__), "tmp", name + "_bg.jpg")
    full_bg_path = os.path.join(os.path.dirname(__file__), "tmp", name + ".jpg")
    tasks = [
        download_image_as_jpg(bg, bg_path),
        download_image_as_jpg(full_bg, full_bg_path),
    ]
    t = time.perf_counter()
    # 1.下载图片
    loop.run_until_complete(asyncio.wait(tasks))

    # 2.识别图片
    res = crack_gee.slider_pos(bg_path, full_bg_path)

    app.logger.debug("GeeTest 解析成功 {} {} , Offset:{}".format(bg_path, full_bg_path, res))
    if need_remove is not None:
        os.remove(bg_path)
        os.remove(full_bg_path)
    t = time.perf_counter() - t
    return make_response({'message': "解析成功", 'offset': res, "t": round(t, 2)}, 200)


if __name__ == '__main__':
    app.run()
