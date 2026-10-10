# 本文件把美术、角色、转场与可复用演出集中管理，剧情只需调用名字。
define me = Character("林予", color="#dccab0")
define k = Character("珂澜", color="#94c9c4")
define y = Character("犹夏", color="#c0b3df")
define n = Character("奈亚", color="#e0b69b")
define narrator = Character(None)
define _game_menu_screen = "preferences"

image bg cafe = Transform("images/cafe.png", xysize=(1600, 900))
# 异常空镜仍使用真实咖啡馆，只撤去暖色与亮度，绝不展示怪物实体。
image bg afterhours = Transform("images/cafe.png", xysize=(1600, 900), matrixcolor=SaturationMatrix(0.25) * BrightnessMatrix(-0.22))
image kelan = Transform("images/kelan.png", xysize=(680, 1020), fit="contain")
image youxia = Transform("images/youxia.png", xysize=(680, 1020), fit="contain")
image naiya = Transform("images/naiya.png", xysize=(680, 1020), fit="contain")

# 人物落在对话框后方。轻微淡入而非突然闪现，保持安静的恋爱氛围。
transform portrait_center:
    xalign 0.5
    ypos 10
    alpha 0.0
    ease 0.65 alpha 1.0

transform portrait_left:
    xalign 0.15
    ypos 10
    alpha 0.0
    ease 0.65 alpha 1.0

transform portrait_right:
    xalign 0.85
    ypos 10
    alpha 0.0
    ease 0.65 alpha 1.0

transform soft_in:
    alpha 0.0
    ease 0.7 alpha 1.0

transform slow_pulse:
    alpha 0.35
    ease 2.6 alpha 0.8
    ease 2.6 alpha 0.35
    repeat

init python:
    import math

    # 程序化细雨：每条雨丝的起点由序号计算，因此读档不会改变随机剧情状态。
    # 只在右侧玻璃区域少量绘制；可在设置中关闭，画面没有高频闪烁。
    class WindowRain(renpy.Displayable):
        def render(self, width, height, st, at):
            r = renpy.Render(1600, 900)
            if persistent.gentle_motion:
                return r
            canvas = r.canvas()
            for i in range(42):
                x = 35 + (i * 97) % 680
                yy = ((i * 71) + st * (64 + i % 4 * 11)) % 650
                canvas.line((174, 207, 205, 38), (x, yy), (x - 5, yy + 22 + i % 12), 1)
            renpy.redraw(self, 1.0 / 24.0)
            return r

    def remember_ending(code):
        # persistent 跨周目保存；普通剧情变量则由存档与回滚管理。
        persistent.endings.add(code)
        renpy.save_persistent()

    profiles = [
        ("kelan", "珂澜", "01 / 在梦里，先见过你", "海洋声学研究员 / 26 岁", "她说睡眠是另一种见面。\n点了热可可，却总把杯子握得像在取暖。", "深海 / 梦境 / 沉眠", "克苏鲁 / Cthulhu"),
        ("youxia", "犹夏", "02 / 想要一个未知答案", "建筑设计师 / 25 岁", "她记得所有没发生过的约会。\n唯独不愿提前知道，你会不会留下来。", "门扉 / 时空 / 可能性", "犹格 索托斯 / Yog-Sothoth"),
        ("naiya", "奈亚", "03 / 今晚，只做我自己", "品牌创意顾问 / 27 岁", "她可以成为任何人喜欢的样子。\n但这一次，她希望你不必满意。", "千面 / 信使 / 戏谑", "奈亚拉托提普 / Nyarlathotep")
    ]

