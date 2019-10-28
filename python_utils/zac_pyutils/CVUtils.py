# author: zac
# create-time: 2019-10-28 16:54
# usage: -
import sys
import urllib.request
import numpy as np
from io import BytesIO
import importlib


def _get_module(name):
    # return sys.modules.get(name, default=__import__(name))
    return sys.modules.get(name, importlib.import_module(name))


def _is_url(inp_str):
    return inp_str.startswith("http://") or inp_str.startswith("https://")


class Load:
    @staticmethod
    def image_by_cv2_from(img_path: str):
        """
        automatic discern input between url and local-file
        default format is [BGR].
        return None if load url request failed
        """
        cv2 = _get_module("cv2")
        if _is_url(img_path):
            # load from url
            if ".webp" in img_path:
                assert False, "at 2019-10-28, cv2 does not support webp (it's a python-opencv binding bug)  " \
                              "refer to this: https://github.com/opencv/opencv/issues/14978\n\n" \
                              "*********** use Loader.load_image_by_pil_from() **********"
            try:
                url_response = urllib.request.urlopen(img_path)
                img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
                img = cv2.imdecode(img_array, -1)
                return img
            except Exception as e:
                print("load img from url failed: " + str(e))
                return None
        else:
            # load from file
            return cv2.imread(img_path)

    @staticmethod
    def image_by_pil_from(img_path: str):
        """
        automatic discern input between url and local-file
        default format is [RGB].
        return None if load url request failed
        """
        Image = _get_module("PIL.Image")
        if _is_url(img_path):
            # load from url
            try:
                url_response = urllib.request.urlopen(img_path)
                image = Image.open(BytesIO(url_response.read()))
                return image
            except Exception as e:
                print("[ERROR] load img from url failed: " + str(e))
                return None
        else:
            # load from file
            return Image.open(img_path)

    @staticmethod
    def image_by_caffe_from_fp(img_path: str):
        if _is_url(img_path):
            assert False, "caffe only support load from local file"
        caffe = _get_module("caffe")
        return [caffe.io.load_image(img_path)]


class Process:
    @staticmethod
    def pre_cv2caffe(img_inp):
        cv2 = _get_module("cv2")
        img = cv2.cvtColor(img_inp, cv2.COLOR_BGR2RGB) / 255.0
        return [img]

    @staticmethod
    def pre_cv2Image(img_inp):
        cv2 = _get_module("cv2")
        Image = _get_module("PIL.Image")
        img = cv2.cvtColor(img_inp, cv2.COLOR_BGR2RGB)
        return Image.fromarray(img)
