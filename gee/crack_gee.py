from PIL import Image
import sys
import os


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


def _recover_img(filename, name):
    im = Image.open(filename)
    width, height = im.size
    new_img = Image.new('RGB', (260, height))
    # split two area
    pos_list = [
        {'y': -58, 'x': -157},
        {'y': -58, 'x': -145},
        {'y': -58, 'x': -265},
        {'y': -58, 'x': -277},
        {'y': -58, 'x': -181},
        {'y': -58, 'x': -169},
        {'y': -58, 'x': -241},
        {'y': -58, 'x': -253},
        {'y': -58, 'x': -109},
        {'y': -58, 'x': -97},
        {'y': -58, 'x': -289},
        {'y': -58, 'x': -301},
        {'y': -58, 'x': -85},
        {'y': -58, 'x': -73},
        {'y': -58, 'x': -25},
        {'y': -58, 'x': -37},
        {'y': -58, 'x': -13},
        {'y': -58, 'x': -1},
        {'y': -58, 'x': -121},
        {'y': -58, 'x': -133},
        {'y': -58, 'x': -61},
        {'y': -58, 'x': -49},
        {'y': -58, 'x': -217},
        {'y': -58, 'x': -229},
        {'y': -58, 'x': -205},
        {'y': -58, 'x': -193},
        {'y': 0, 'x': -145},
        {'y': 0, 'x': -157},
        {'y': 0, 'x': -277},
        {'y': 0, 'x': -265},
        {'y': 0, 'x': -169},
        {'y': 0, 'x': -181},
        {'y': 0, 'x': -253},
        {'y': 0, 'x': -241},
        {'y': 0, 'x': -97},
        {'y': 0, 'x': -109},
        {'y': 0, 'x': -301},
        {'y': 0, 'x': -289},
        {'y': 0, 'x': -73},
        {'y': 0, 'x': -85},
        {'y': 0, 'x': -37},
        {'y': 0, 'x': -25},
        {'y': 0, 'x': -1},
        {'y': 0, 'x': -13},
        {'y': 0, 'x': -133},
        {'y': 0, 'x': -121},
        {'y': 0, 'x': -49},
        {'y': 0, 'x': -61},
        {'y': 0, 'x': -229},
        {'y': 0, 'x': -217},
        {'y': 0, 'x': -193},
        {'y': 0, 'x': -205}
    ]
    im_list_up = []
    im_list_down = []
    for loc in pos_list:
        if loc['y'] == -58:
            im_list_up.append(im.crop((abs(loc['x']), height // 2, abs(loc['x']) + 10, height)))
        if loc['y'] == 0:
            im_list_down.append(im.crop((abs(loc['x']), 0, abs(loc['x']) + 10, height // 2)))

    x_offset = 0
    for img in im_list_up:
        new_img.paste(img, (x_offset, 0))
        x_offset += img.size[0]

    x_offset = 0
    for img in im_list_down:
        new_img.paste(img, (x_offset, height // 2))
        x_offset += img.size[0]
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
