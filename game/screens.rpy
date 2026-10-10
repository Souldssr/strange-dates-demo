# 自定义界面。所有位置都以 1600×900 逻辑画布为准，字体与颜色在这里统一。
# Ren'Py 的 action 负责存读档 / 回滚 / 设置；没有另造一套存档系统。
init -10 python:
    config.overlay_screens.append("quick_menu")

style default:
    font "fonts/SourceHanSansLite.ttf"
    size 25
    color "#e5e6df"
    language "unicode"

style text:
    line_spacing 9

style button:
    padding (18, 10)
    background None
    hover_background Solid("#c9b38b22")

style button_text:
    size 23
    color "#c1c8c7"
    hover_color "#f4d4a1"
    selected_color "#f4d4a1"
    insensitive_color "#647276"

style bar:
    xsize 360
    ysize 6
    left_bar Solid("#bba17c")
    right_bar Solid("#35464c")
    thumb Solid("#e5d1ac", xsize=14, ysize=20)

style slider is bar
style slider:
    xsize 380
    ysize 8

style vscrollbar:
    xsize 5
    base_bar Solid("#25383d")
    thumb Solid("#ad9978")

style say_label:
    size 28
    bold False
    color "#d5bd94"

style say_dialogue:
    size 28
    color "#e7e5dd"
    line_spacing 13

style choice_button:
    background Solid("#10242aef")
    hover_background Solid("#29454cef")
    padding (30, 19)
    xsize 860

style choice_button_text:
    size 27
    color "#e7e4da"
    hover_color "#f4d4a1"
    xalign 0.5
    text_align 0.5

# 标题：左边是杂志式排版，右边叠放三位角色；标题绝不烘焙在美术图中。
screen main_menu():
    tag menu
    add "bg cafe"
    add Solid("#0c1b2360")
    add "images/youxia.png" xpos 920 ypos 104 xysize (500, 750)
    add "images/naiya.png" xpos 1180 ypos 154 xysize (470, 705)
    add "images/kelan.png" xpos 670 ypos 190 xysize (535, 803)
    add "gui/menu_veil.png"
    add "gui/vignette.png"
    add WindowRain()
    text "余 温  /  AFTER HOURS" xpos 84 ypos 57 size 20 color "#c5b38e" kerning 3
    text "一场恰好停在 21:17 的相亲" xpos 86 ypos 191 size 20 color "#9fbbb8" kerning 2
    text "我的相亲对象们" xpos 79 ypos 245 size 66 color "#f0e8d7" kerning 2
    text "有点怪" xpos 79 ypos 337 size 100 color "#d2b68d" kerning 10
    add Solid("#b99e7488", xsize=54, ysize=2) xpos 87 ypos 478
    text "她们都很喜欢你。\n只是，喜欢的方式不太一样。" xpos 87 ypos 511 size 24 color "#b3c1bf" line_spacing 11
    button:
        xpos 86 ypos 618 xsize 385 ysize 70
        background Solid("#c4ac84")
        hover_background Solid("#e2c798")
        action Start()
        text "赴 约                              →" size 26 color "#13262d" align (0.5, 0.5)
    hbox:
        xpos 71 ypos 718 spacing 8
        textbutton "继续" action Continue()
        textbutton "人物档案" action ShowMenu("profiles_screen")
        textbutton "回收册" action ShowMenu("collection")
        textbutton "设置" action ShowMenu("preferences")
    text "雨夜试约 / 短篇体验版" xpos 86 ypos 838 size 17 color "#8b9b9a"
    text "都市恋爱  /  视线之外的悬疑" xpos 1240 ypos 838 size 16 color "#a4b0ae"
    textbutton "离开" xpos 1468 ypos 42 action Quit(confirm=True) text_size 18

# 对话框上留足立绘空间；小说正文与操作提示保持明显的视觉层级。
screen say(who, what):
    window:
        id "window"
        background None
        xpos 0 ypos 660 xsize 1600 ysize 240
        add "gui/dialogue.png" xysize (1600, 240)
        add Solid("#b49c76", xsize=3, ysize=37) xpos 103 ypos 27
        if who:
            text who id "who" xpos 125 ypos 23
        else:
            text "雨夜 / 余温" xpos 125 ypos 26 size 20 color "#9eb2b1"
        text what id "what" xpos 125 ypos 78 xsize 1340 ysize 123
        text "◇" xpos 1490 ypos 168 size 24 color "#bda982"

screen quick_menu():
    zorder 100
    if not main_menu and renpy.get_screen("say") and not renpy.get_screen("choice"):
        hbox:
            xpos 841 ypos 853 spacing 12
            textbutton "回看" action ShowMenu("history") text_size 17
            textbutton "后退" action Rollback() text_size 17
            textbutton "自动" action Preference("auto-forward", "toggle") text_size 17
            textbutton "快进" action Skip() alternate Skip(fast=True, confirm=True) text_size 17
            textbutton "存档" action ShowMenu("save") text_size 17
            textbutton "读档" action ShowMenu("load") text_size 17
            textbutton "设置" action ShowMenu("preferences") text_size 17

screen scene_hud():
    zorder 5
    add WindowRain()
    add "gui/vignette.png"
    frame:
        xpos 42 ypos 32 padding (20, 12)
        background Solid("#102129da")
        hbox:
            spacing 23
            text "余 温" size 19 color "#d0b58a"
            text "/" size 18 color "#667c7d"
            text chapter_label size 19 color "#c1cfcb"
    frame:
        xpos 1390 ypos 32 xsize 165 padding (18, 12)
        background Solid("#102129da")
        hbox:
            spacing 15
            text time_label size 21 color "#d0b58a"
            text "●" size 12 color ("#a59b7b" if unease < 2 else "#a98183") yalign 0.5

screen choice(items):
    modal True
    add Solid("#081c2360")
    vbox:
        xalign 0.5 yalign 0.44 spacing 13
        text "这一刻，听从你的心意。" size 19 color "#e1caa4" xalign 0.5
        null height 6
        for i in items:
            textbutton i.caption action i.action style "choice_button" text_style "choice_button_text"

# 章节卡与视线外字幕既可点击，也会自动消失，避免打断阅读节奏。
screen chapter_card(title, subtitle):
    modal True
    zorder 150
    add Solid("#0c1d23f5")
    vbox:
        align (0.5, 0.46) spacing 26
        text "A F T E R   H O U R S" size 17 color "#79928f" xalign 0.5
        text title size 57 color "#d7bf98" xalign 0.5
        text subtitle size 24 color "#b3c3bd" xalign 0.5
    text "点击继续" align (0.5, 0.84) size 17 color "#708683"
    key "dismiss" action Return()
    timer 3.2 action Return()

screen blind_spot(caption):
    modal True
    zorder 150
    add Solid("#07171bed")
    add Solid("#a4b4aa", xsize=1, ysize=50) align (0.5, 0.34)
    text caption align (0.5, 0.48) size 31 color "#abbeb5" kerning 5
    text "你已经转过身去。" align (0.5, 0.58) size 19 color "#617c76"
    key "dismiss" action Return()
    timer 3.6 action Return()

screen ending_card(code, title, subtitle, person):
    modal True
    zorder 160
    add "bg afterhours"
    add Solid("#091c24e8")
    text "雨 停 以 后" align (0.5, 0.19) size 22 color "#819d98" kerning 8
    text title align (0.5, 0.34) size 62 color "#dfc49c"
    text subtitle align (0.5, 0.47) size 25 color "#bccac4"
    text "[code]    /    [person]" align (0.5, 0.59) size 20 color "#8faeaa"
    hbox:
        align (0.5, 0.76) spacing 40
        textbutton "再选一次" action Jump("before_final_choice")
        textbutton "回收册" action ShowMenu("collection")
        textbutton "返回标题" action MainMenu(confirm=False)
    text "本次相遇已记入回收册。" align (0.5, 0.89) size 17 color "#6d8782"

# 所有菜单共用外壳，Esc / 右键 / 返回按钮都能回到原先的阅读位置。
screen menu_shell(title, subtitle="AFTER HOURS / 余温"):
    add "bg cafe"
    add Solid("#0b1d24f5")
    text subtitle xpos 90 ypos 48 size 17 color "#829b95" kerning 2
    text title xpos 86 ypos 99 size 48 color "#ddc39b"
    add Solid("#526962", xsize=1420, ysize=1) xpos 90 ypos 188
    textbutton "← 返回" xpos 1360 ypos 94 action Return()
    key "game_menu" action Return()
    transclude

screen preferences():
    tag menu
    use menu_shell("调整今晚的节奏"):
        vbox:
            xpos 96 ypos 240 spacing 22
            text "阅读" size 25 color "#dec49d"
            text "文字速度" size 21
            bar value Preference("text speed")
            text "自动播放间隔" size 21
            bar value Preference("auto-forward time")
            null height 8
            text "声音" size 25 color "#dec49d"
            text "音乐与环境声" size 21
            bar value Preference("music volume")
            text "提示音" size 21
            bar value Preference("sound volume")
        vbox:
            xpos 785 ypos 240 spacing 25
            text "画面" size 25 color "#dec49d"
            hbox:
                spacing 25
                textbutton "窗口" action Preference("display", "window")
                textbutton "全屏" action Preference("display", "fullscreen")
            textbutton "减少动态雨丝" action ToggleField(persistent, "gentle_motion")
            textbutton "全部静音" action Preference("all mute", "toggle")
            null height 12
            text "操作" size 25 color "#dec49d"
            text "左键 / 空格   推进对话\n滚轮向上       回看上句\nEsc / 右键     打开设置\nH                    隐藏界面\nCtrl                跳过已读对话" size 21 color "#9eafaa" line_spacing 12
        hbox:
            xpos 91 ypos 799 spacing 33
            textbutton "存档" action ShowMenu("save") sensitive (not main_menu)
            textbutton "读档" action ShowMenu("load")
            textbutton "作品说明" action ShowMenu("about")
            textbutton "返回标题" action MainMenu() sensitive (not main_menu)
            textbutton "退出游戏" action Quit(confirm=True)

screen profiles_screen():
    tag menu
    default selected = 0
    $ p = profiles[selected]
    use menu_shell("相遇档案", "THREE INVITATIONS / 三封邀请"):
        add "images/" + p[0] + ".png" xpos 900 ypos 192 xysize (480, 720)
        vbox:
            xpos 93 ypos 235 spacing 18
            hbox:
                spacing 30
                for index, profile in enumerate(profiles):
                    textbutton profile[1] action SetScreenVariable("selected", index) selected (selected == index)
            null height 14
            text p[2] size 21 color "#8db2ad"
            text p[1] size 63 color "#dfc49d"
            text p[3] size 23 color "#c1cdc5"
            null height 5
            text p[4] size 25 color "#a5b9b2" line_spacing 16
            null height 12
            text "隐秘关键词 / " + p[5] size 19 color "#b49d7e"
            text "灵感原型 / " + p[6] size 18 color "#748e89"
        text "人物均为成年人的原创拟人改编。" xpos 110 ypos 825 size 17 color "#607e79"

screen collection():
    tag menu
    $ endings_list = [("K-01", "醒来以后", "珂澜"), ("Y-01", "未命名的明天", "犹夏"), ("N-01", "下班后的她", "奈亚"), ("H-01", "第四份邀请", "林予")]
    use menu_shell("雨夜回收册", "MEMORIES / 已抵达 %d / 4" % len(persistent.endings)):
        vbox:
            xpos 95 ypos 231 spacing 20
            for code, ending_name, person in endings_list:
                $ unlocked = code in persistent.endings
                frame:
                    xsize 1410 ysize 120 padding (30, 20)
                    background Solid("#1b333aa0" if unlocked else "#142a3080")
                    hbox:
                        spacing 50
                        text code size 20 color "#88a6a1" yalign 0.5 xsize 90
                        vbox:
                            spacing 8
                            text (ending_name if unlocked else "尚未抵达的雨后") size 26 color ("#ddc097" if unlocked else "#66827d")
                            text (person if unlocked else "赴一次约，让故事由你来回答。") size 18 color "#8da7a0"
                        null width 260
                        text ("已收藏" if unlocked else "未解锁") size 19 color "#829e92" yalign 0.5
        text "结局后可选择「再选一次」，快速体验其他方向。" xpos 108 ypos 825 size 18 color "#75908b"

screen save():
    tag menu
    use file_slots("保存这一刻")

screen load():
    tag menu
    use file_slots("回到那场雨")

screen file_slots(title):
    use menu_shell(title, "SAVED MOMENTS / 记忆"):
        grid 3 2:
            xpos 93 ypos 229 spacing 25
            for slot in range(1, 7):
                button:
                    xsize 454 ysize 252
                    background Solid("#18323ac0")
                    hover_background Solid("#2b4850")
                    padding (14, 12)
                    action FileAction(slot)
                    vbox:
                        spacing 6
                        add FileScreenshot(slot) xsize 424 ysize 166 fit "cover"
                        text FileTime(slot, format="%m/%d  %H:%M", empty="空白记忆") size 19 color "#d5c19f"
                        text FileSaveName(slot) size 15 color "#92aaa5"
                    key "save_delete" action FileDelete(slot)
        hbox:
            xalign 0.5 ypos 802 spacing 20
            textbutton "自动" action FilePage("auto")
            textbutton "快速" action FilePage("quick")
            for page in range(1, 5):
                textbutton str(page) action FilePage(page)

screen history():
    tag menu
    use menu_shell("我们刚才说到哪里", "CONVERSATION / 对话回看"):
        viewport:
            xpos 108 ypos 230 xsize 1390 ysize 600
            scrollbars "vertical"
            mousewheel True
            draggable True
            yinitial 1.0
            vbox:
                spacing 26
                for h in _history_list:
                    hbox:
                        spacing 30
                        text (h.who or "余温") xsize 150 size 22 color "#c1aa87"
                        text renpy.filter_text_tags(h.what, allow=[]) xsize 1130 size 24 color "#bdcbc5"
                if not _history_list:
                    text "这场雨，还没有开始。" color "#869f96"

screen about():
    tag menu
    use menu_shell("关于这场相遇", "A SHORT VISUAL NOVEL / 作品说明"):
        vbox:
            xpos 100 ypos 235 spacing 26
            text "我的相亲对象们有点怪" size 38 color "#ddc59e"
            text "雨夜试约 / 1.0.0" size 21 color "#85a79f"
            text "三封相亲邀请，一座打烊的咖啡馆，一个没有走动的时钟。\n你可以喜欢她们，也可以选择自己。" size 26 line_spacing 15
            text "现代都市 / 克系恋爱 / 轻悬疑 / 四种结局" size 22 color "#b4a081"
            null height 6
            text "引擎  Ren'Py 8.2\n字体  Source Han Sans Lite / SIL OFL\n美术  AI 辅助生成，参照用户提供的风格图\n声音  程序合成原创环境声与提示音\n剧本、界面与程序  使用 Codex 协作制作" size 21 color "#8eaaa1" line_spacing 10
            text "克苏鲁神话元素为原创拟人改编，非对原作角色的直接复述。\n无具象恐怖画面，无突然惊吓。建议佩戴耳机。" size 19 color "#738f85" line_spacing 10

# 引擎通用确认框保留标准接口，以兼容覆盖存档、返回标题与退出确认。
screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid("#041318d9")
    frame:
        align (0.5, 0.5) xsize 800 padding (48, 40)
        background Solid("#163039")
        vbox:
            spacing 34
            text message xalign 0.5 text_align 0.5 size 27 color "#e1d6bd"
            hbox:
                xalign 0.5 spacing 100
                textbutton "确定" action yes_action
                textbutton "取消" action no_action
    key "game_menu" action no_action

screen notify(message):
    zorder 190
    frame:
        xalign 0.5 ypos 110 padding (25, 14)
        background Solid("#153339ef")
        text message size 21 color "#dec59e"
    timer 3.0 action Hide("notify")
