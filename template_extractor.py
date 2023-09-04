# 此脚本用于根据 Resources/screencaps 中的截图按类别生成模板

# 导入模块
import os
import numpy as np
from PIL import Image

import cv2 as cv

SCREENCAPS = ["Resources","screencaps"]
TEMPLATES = ["Resources","templates"]

def LoadImage(path):
    return np.array(Image.open(path))

def ExtractTemplate(path:str):
    images = [os.path.join(path, filename) for filename in os.listdir(path)]
    templateName = "{}.png".format(path.split("\\")[-1])
    
    # 所有图片
    imageData = np.concatenate([LoadImage(imagePath).reshape(1, 1280, 720,4) for imagePath in images])
    
    # 颜色
    minData = imageData.min(axis=0)
    maxData = imageData.max(axis=0)
    
    colorTemplate = maxData.copy()
    colorTemplate[(minData != maxData).any(axis=2)] = 0
    
    Image.fromarray(colorTemplate).save(os.path.join(*TEMPLATES, "Color", templateName))

    # 边缘

    edges = np.concatenate(cv.Canny(img, 100, 200).reshape(1, 1280, 720) for img in imageData)

    edgeTemplate = edges.min(axis=0)

    Image.fromarray(edgeTemplate).save(os.path.join(*TEMPLATES, "Edge", templateName))


    

    
if __name__ == "__main__":
    clses = [path for path in os.listdir(os.path.join(*SCREENCAPS)) if os.path.isdir(os.path.join(*SCREENCAPS, path))]
    for cls in clses:
        print(os.path.join(*SCREENCAPS, cls))
        ExtractTemplate(os.path.join(*SCREENCAPS, cls))