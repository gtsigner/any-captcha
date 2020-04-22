from PIL import Image
import sys
import os
import numpy as np


def slider_pos(bg_path, full_bg_path):
    """
    滑块验证码
    :param bg_path:
    :param full_bg_path:
    :return:
    """
    if os.path.isfile(bg_path) is not True or os.path.isfile(full_bg_path) is not True:
        raise Exception("bg is not a file")
    _recover_img(bg_path, bg_path)  # 修复2账图片
    _recover_img(full_bg_path, full_bg_path)  # 修复第二张图片
    return _gee_offset(full_bg_path, bg_path)


def img_icon_pos(im_path):
    """
    图片点选验证码
    :param im_path:
    :return:
    """


def img_word_pos():
    """
    文字点选
    :return:
    """


gee_offsets = [[
    157, 145, 265, 277, 181, 169, 241, 253, 109, 97,
    289, 301, 85, 73, 25, 37, 13, 1, 121, 133,
    61, 49, 217, 229, 205, 193
], [
    145, 157, 277, 265, 169, 181, 253, 241, 97, 109,
    301, 289, 73, 85, 37, 25, 1, 13, 133, 121,
    49, 61, 229, 217, 193, 205
]]


def _recover_img(filename, name):
    im = Image.open(filename)
    width, height = im.size
    new_img = Image.new('RGB', (260, height))
    im_list_up = []
    im_list_down = []
    for y, loc in enumerate(gee_offsets):
        for y1, x in enumerate(loc):
            if y == 0:
                im_list_up.append(im.crop((x, height // 2, x + 10, height)))
            if y == 1:
                im_list_down.append(im.crop((x, 0, x + 10, height // 2)))

    off = 0
    for img in im_list_up:
        new_img.paste(img, (off, 0))
        off += img.size[0]

    off = 0
    for img in im_list_down:
        new_img.paste(img, (off, height // 2))
        off += img.size[0]
    new_img.save(name)
    return new_img


def _gee_offset(fp, bp):
    """
    :param fp: full_bg path
    :param bp: bg path
    :return: int offset
    """
    full_bg = Image.open(fp)
    bg = Image.open(bp)
    left = 0  # left offset
    for i in range(left, full_bg.size[0]):
        for j in range(full_bg.size[1]):
            if not _pixel_equal(full_bg, bg, i, j):
                left = i
                return left
    return -1


def _pixel_equal(img1, img2, x, y):
    pix1 = img1.load()[x, y]
    pix2 = img2.load()[x, y]
    threshold = 60
    if (abs(pix1[0] - pix2[0] < threshold) and abs(pix1[1] - pix2[1] < threshold) and abs(
            pix1[2] - pix2[2] < threshold)):
        return True
    else:
        return False


if __name__ == "__main__":
    ps = os.path.dirname(sys.argv[0])
    id = "3a916e2a-a5ff-4d56-a021-68c97e7856ba"
    ps = os.path.join(ps, "../tmp/gee/" + id)
    res = slider_pos(ps + ".jpg", ps + "_full.jpg")
    print(res)
