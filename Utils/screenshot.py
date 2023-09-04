
import os
import cv2 as cv
import numpy as np
from PIL import Image

# 模板类型及模板文件名
# 这个类由这个代码生成，要更新这个类，
# 请直接运行这个脚本，将输出覆盖这个类
class ScreenshotTemplates:
    ANNOUNCEMENT = 0
    ARENA_MAIN = 1
    ARENA_PREPARE = 2
    ARENA_RACING = 3
    ARENA_RESULT = 4
    ARENA_SELECT_ITEM = 5
    ARENA_SELECT_OPPONENT = 6
    ARENA_STATE = 7
    ARENA_SUMMARY = 8
    CONTINUE_CULTIVATE = 9
    CULTIVATE_EVENT_OPTIONS = 10
    CULTIVATE_MAIN = 11
    CULTIVATE_MENU = 12
    CULTIVATE_REST = 13
    CULTIVATE_TRAINING = 14
    HOME = 15
    LOADING = 16
    RACE = 17
    TITLE = 18
    template = {
        0: "announcement.png",
        1: "arena_main.png",
        2: "arena_prepare.png",
        3: "arena_racing.png",
        4: "arena_result.png",
        5: "arena_select_item.png",
        6: "arena_select_opponent.png",
        7: "arena_state.png",
        8: "arena_summary.png",
        9: "continue_cultivate.png",
        10: "cultivate_event_options.png",
        11: "cultivate_main.png",
        12: "cultivate_menu.png",
        13: "cultivate_rest.png",
        14: "cultivate_training.png",
        15: "home.png",
        16: "loading.png",
        17: "race.png",
        18: "title.png",
    }

# 截图检查模式枚举
class ScreenshotCheckMode:
    STRICT = 0
    LOOSE = 1

class ScreenshotConfig:
    method = cv.TM_CCORR_NORMED

# 截图类
# 封装了一些与模板对照的类
class Screenshot:
    def __init__(self, array:np.ndarray):
        self.img = array

    def CheckColorTemplate(self, template:int) -> bool:
        templatePath = os.path.join("Resources", "templates", "Color", ScreenshotTemplates.template[template])
        tpl = np.array(Image.open(templatePath))
        return (tpl/255 * self.img/255.0).sum() / (tpl/255).sum() > 0.875

    def CheckEdgeTemplate(self, template:int) -> bool:
        os.path.join("Resources", "templates", "Edge", ScreenshotTemplates.template[template])
        pass

    def CheckTemplate(self, template:str, mode:int = ScreenshotCheckMode.STRICT) -> bool:
        '''检查是否匹配模板'''
        if mode == ScreenshotCheckMode.STRICT:
            return self.CheckEdgeTemplate(template) and self.CheckColorTemplate(template)
        if mode == ScreenshotCheckMode.LOOSE:
            return self.CheckEdgeTemplate(template) or self.CheckColorTemplate(template)
        else:
            raise(ValueError("mode 参数无效。"))
        
if __name__ == "__main__":
    """
    templates = os.listdir(os.path.join("..", "Resources", "templates", "Color"))

    code1 = ""
    code1 += "class ScreenshotTemplates:\n"
    code2 = ""
    for i, template in enumerate(templates):
        code1 += f"    {template[:-4].upper()} = {i}\n"
        code2 += f"        {i}: \"{template}\",\n"
    code1 += "    template = {\n"
    code2 += "    }"
    print(code1 + code2)

    os.chdir("..")"""
    print(os.getcwd())
    ss = Screenshot(np.array(Image.open("D:\\Work Space\\Python\\Py-ADB-Framework\\Resources\\screencaps\\home\\1693820370.png")))
    for i in range(len(ScreenshotTemplates.template)):
        print(ScreenshotTemplates.template[i], end=": ")
        print(ss.CheckColorTemplate(i))
        print(ss.CheckColorTemplate(i))
