# 引擎配置：逻辑画布固定 1600×900，Ren'Py 自动适配窗口与全屏。
init -20 python:
    gui.init(1600, 900)

define config.name = "我的相亲对象们有点怪"
define config.version = "1.0.0"
define build.name = "StrangeDates"
define config.save_directory = "StrangeDates-2026"
define config.window_title = "我的相亲对象们有点怪 · 雨夜试约"
define config.window_icon = "gui/icon.png"
define config.has_sound = True
define config.has_music = True
define config.has_voice = False
define config.main_menu_music = "audio/cafe.wav"
define config.main_menu_music_fadein = 2.0
define config.default_text_cps = 32
define config.default_afm_time = 12
define config.history_length = 250
define config.rollback_enabled = True
define config.autosave_slots = 3
define config.autosave_frequency = 40
define config.thumbnail_width = 400
define config.thumbnail_height = 225
define config.default_fullscreen = False
define config.gl2 = True
define config.developer = "auto"
define config.allow_skipping = True
define config.end_splash_transition = Dissolve(0.7)
define config.enter_transition = Dissolve(0.18)
define config.exit_transition = Dissolve(0.18)
define config.intra_transition = Dissolve(0.15)

default preferences.text_cps = 32
default preferences.afm_time = 12
default preferences.skip_unseen = False
default persistent.endings = set()
default persistent.gentle_motion = False

# 仅打包运行必须内容；避免把 SDK、测试镜像和历史构建重新装进发行包。
init python:
    build.directory_name = "StrangeDates-1.0"
    build.executable_name = "StrangeDates"
    build.include_update = False
    for pattern in [".git/**", ".gitignore", ".gitattributes", ".tools/**", ".qa/**", "tools/**", "build/**", "dist/**", "docs/**", "README.md", "*.ps1", "*.txt", "**~", "**.bak", "game/cache/**", "game/saves/**"]:
        build.classify(pattern, None)
    build.classify("licenses/**", "all")
    build.classify("game/**.rpy", "all")
    build.classify("game/**.rpyc", "all")
    build.documentation("README-HR.html")

