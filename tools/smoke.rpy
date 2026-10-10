# 仅由 smoke.py 注入 .qa 临时项目，发行包不包含此文件。
# 所有交互均通过 Ren'Py 官方 testcase / Action 执行，不模拟桌面操作。
default qa_saved_marker = 0

init 999 python:
    class QAScreen(Action):
        """让 testcase 在目标屏幕实际出现时停止推进。"""
        def __init__(self, name):
            self.name = name
        def get_sensitive(self):
            return renpy.get_screen(self.name) is not None
        def __call__(self):
            pass

    def qa_shot(name):
        assert renpy.screenshot("__QA_OUTPUT__/" + name + ".png")

# 独立演出段落用于稳定比较字号、立绘裁切、对话框与静默空镜。
label qa_portraits:
    # 状态位必须在剧情语句内设置，存档按剧情 checkpoint 恢复，不能在测试事件中造状态。
    $ qa_saved_marker = 41
    $ chapter_label = "雨夜试约"
    $ time_label = "21:17"
    scene bg cafe
    show screen scene_hud
    show kelan at portrait_center
    k "如果你今晚梦见海，不用往前走。"
    hide kelan
    show youxia at portrait_center
    y "不知道也没关系。今晚，我们走一条没准备过的路。"
    hide youxia
    show naiya at portrait_center
    n "下一次，如果我又开始猜你想听什么，你提醒我。"
    hide naiya
    scene bg afterhours
    call screen blind_spot("当你转过身")
    "空无一人的咖啡馆里，另一只杯子还留着余温。"
    return

testcase portfolio_ui:
    $ _test.timeout = 20.0
    $ preferences.text_cps = 0
    pause 1.2
    $ qa_shot("01-title")
    "人物档案"
    pause 0.7
    assert renpy.get_screen("profiles_screen")
    $ qa_shot("02-profile-kelan")
    "犹夏"
    pause 0.3
    $ qa_shot("02-profile-youxia")
    "奈亚"
    pause 0.3
    $ qa_shot("02-profile-naiya")
    "返回"
    pause 0.4
    "设置"
    pause 0.6
    assert renpy.get_screen("preferences")
    $ qa_shot("03-preferences")
    "减少动态雨丝"
    assert persistent.gentle_motion
    "减少动态雨丝"
    assert not persistent.gentle_motion
    "作品说明"
    pause 0.4
    $ qa_shot("04-about")
    "返回"
    pause 0.4
    run Start("qa_portraits")
    pause 1.0
    $ qa_shot("05-kelan-dialogue")
    "存档"
    pause 0.5
    assert renpy.get_screen("save")
    run FileSave(1, confirm=False)
    pause 0.5
    assert FileLoadable(1)
    $ qa_shot("06-save")
    "返回"
    pause 0.3
    $ qa_saved_marker = 99
    run FileLoad(1, confirm=False)
    pause 0.7
    assert qa_saved_marker == 41
    assert renpy.get_screen("say")
    type SPACE
    pause 0.9
    $ qa_shot("07-youxia-dialogue")
    type SPACE
    pause 0.9
    $ qa_shot("08-naiya-dialogue")
    type SPACE
    pause 0.8
    $ qa_shot("09-blind-spot")
    $ renpy.quit()

testcase complete_story:
    $ _test.timeout = 20.0
    $ preferences.text_cps = 0
    run Start()
    type SPACE until "先不管系统"
    type SPACE until "先告诉我"
    type SPACE until run QAScreen("choice")
    pause 0.5
    $ qa_shot("10-final-choice")
    "珂澜，明天下午"
    type SPACE until run QAScreen("ending_card")
    assert "K-01" in persistent.endings
    pause 0.4
    $ qa_shot("11-ending-kelan")
    "再选一次"
    "犹夏，我们走一条"
    type SPACE until run QAScreen("ending_card")
    assert "Y-01" in persistent.endings
    pause 0.4
    $ qa_shot("12-ending-youxia")
    "再选一次"
    "奈亚，吃火锅"
    type SPACE until run QAScreen("ending_card")
    assert "N-01" in persistent.endings
    pause 0.4
    $ qa_shot("13-ending-naiya")
    "再选一次"
    "谢谢今晚"
    type SPACE until run QAScreen("ending_card")
    assert "H-01" in persistent.endings
    pause 0.4
    $ qa_shot("14-ending-alone")
    "回收册"
    pause 0.5
    assert persistent.endings == {"K-01", "Y-01", "N-01", "H-01"}
    $ qa_shot("15-collection-complete")
    $ renpy.quit()
