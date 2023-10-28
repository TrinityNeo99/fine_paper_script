"""
@Project: 2022-2027-paper_script
@FileName: __init__.py
@Description: 画图相关脚本
@Author: Wei Jiangning
@version: 1.0.0a1.0
@Date: 2023/10/28 13:41 at PyCharm
"""
import os
import numpy as np
import cv2


def extract_pic_from_video(path):
    cap = cv2.VideoCapture(path)
    flat, pic = cap.read()
    return pic


def extract_pics_from_dataset(ds_path):
    print("extract...")
    videos = os.listdir(ds_path)
    pics = [extract_pic_from_video(os.path.join(ds_path, v)) for v in videos]
    return pics


def merge_pics(pics: list, w_s=10, h_s=10):
    """

    :param pics: list of pictures of same format, like H*W*3 for RGB
    :param w_s: the number of pictures in width
    :param h_s: the number of pictures in height
    :return: merged_pic
    """
    assert w_s * h_s <= len(pics), "the number of pictures in list is less than the required"
    print("merging...")
    pic_w = pics[0].shape[1]
    pic_h = pics[0].shape[0]
    pic_c = pics[0].shape[2]
    new_pics = []
    for i in pics:
        i = cv2.resize(i, (pic_w, pic_h))
        new_pics.append(i)
    merged_pic = np.zeros(shape=(h_s * pic_h + 1, 1, pic_c))
    for i in range(w_s):
        h_pic = np.zeros(shape=(1, pic_w, pic_c))
        for j in range(h_s):
            h_pic = np.vstack([h_pic, new_pics[i + h_s * j]])
        merged_pic = np.hstack([merged_pic, h_pic])
    merged_pic = cv2.resize(merged_pic, (pic_w, pic_h))
    print("writing...")
    cv2.imwrite("./merged_pic.png", merged_pic)
    return merged_pic


def dataset_merge_cover(path):
    merge_pics(extract_pics_from_dataset(path))


if __name__ == '__main__':
    dataset_merge_cover(r"F:\pingpong-all-data\2023-4-19_北体合作_动作示范视频_实验用小规模数据集")
