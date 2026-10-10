# 《我的相亲对象们有点怪》
# 一周目约 5—8 分钟。所有可攻略角色及主角均为成年人。
# 流程：三人共通序章 → 三次短约会 → 自由选择 → 三条恋爱结局 / 离席结局。
# 人物、立绘、界面和 persistent.endings 由主工程定义，本文件负责剧情状态。

# HUD 只呈现玩家已知的章节 / 时刻；unease 取 0—3，用于气氛提示。
default chapter_label = "雨夜来信"
default time_label = "21:17"
default unease = 0
# noticed 影响主角对异常的措辞，绝不让主角得知「视线之外」镜头的内容。
default noticed = False
# 共鸣不限制攻略权，只改变结局中的亲密对白，便于短 Demo 完整展示所有路线。
default resonance_k = 0
default resonance_y = 0
default resonance_n = 0

label start:
    $ chapter_label = "雨夜来信"
    $ time_label = "21:17"
    $ unease = 0
    $ noticed = False
    $ resonance_k = 0
    $ resonance_y = 0
    $ resonance_n = 0

    stop music fadeout 1.0
    scene bg cafe with fade
    play music "audio/rain.wav" fadein 2.0 volume 0.45
    call screen chapter_card("雨夜来信", "一张桌子，三封邀请。")
    show screen scene_hud

    "我叫林予，二十七岁，在一家杂志社做编辑。"
    "今天校完的最后一篇稿子叫《如何辨别不靠谱的相亲对象》。"
    "现在，我正拿着三份时间、地点完全相同的相亲邀请，站在一家即将打烊的咖啡馆里。"
    me "……很好。理论终于要接受实践检验了。"
    "窗外的雨把招牌晕成一小团金色：余温。"
    "店员已经收走了其他桌上的杯子。靠窗的位置，却恰好留着四把椅子。"

    show kelan at portrait_center with dissolve
    k "林予？这里。"
    "穿深青色外套的姑娘朝我招手。她看起来有些困，捧着热杯子的样子倒十分认真。"
    k "我是珂澜。你比我梦到的……比我想的，来得早一点。"
    me "地铁没晚点。算是今晚的第一个好兆头。"
    hide kelan with dissolve
    show youxia at portrait_center with dissolve
    y "也可能是最后一个。"
    "旁边的银发姑娘合上手里的笔记本。她的语气很平静，像是在报天气。"
    y "犹夏。做建筑设计。抱歉，我刚才那句话不适合初次见面。"
    me "没事。我写过更不适合的开场白。"
    hide youxia with dissolve
    show naiya at portrait_center with dissolve
    n "比如一晚上约三个？"
    "第三位姑娘把手机翻过来。屏幕上，是和我一模一样的邀请函。"
    n "奈亚。品牌顾问。放心，至少有一个人今晚确实没打算来谈合作。"
    me "我现在解释是系统的问题，还有可信度吗？"
    n "有。我今天恰好喜欢诚实得很狼狈的人。"
    hide naiya with dissolve

    "三份邀请的末尾，都写着同一句话。"
    "『请在二十一点十七分之前，选一个能陪你等雨停的人。』"
    "墙上的时钟，正好停在二十一点十七分。"

    # 第一个共通选择：对待突发事件的方式，给予对应角色一次共鸣。
    menu:
        "我把邀请函放在桌上。"
        "「先不管系统。你们喝点什么？」":
            $ resonance_k += 1
            show kelan at portrait_center with dissolve
            k "热可可。要很热的那种。"
            me "你面前这杯呢？"
            k "拿来暖手的。……原来真的可以先点自己喜欢的东西。"
            hide kelan with dissolve
        "「这句『选一个』，是谁写的？」":
            $ resonance_y += 1
            $ noticed = True
            $ unease += 1
            show youxia at portrait_center with dissolve
            y "不是我。如果是我，会把『也可以不选』写清楚。"
            "她拿起笔，认真地在那一行下面补了六个字。"
            me "现在好多了。"
            hide youxia with dissolve
        "「我们至少可以给这场事故一个好评。」":
            $ resonance_n += 1
            show naiya at portrait_center with dissolve
            n "理由呢？"
            me "匹配效率很高。责任归属很差。"
            "她笑出声，又很快捂住嘴，像没料到自己会笑。"
            n "这个评价我想偷走。"
            hide naiya with dissolve

    "我们决定轮流聊一会儿。其他人去吧台坐，免得这场相亲彻底变成面试。"
    "店员从头到尾没有问，我们为什么有三份预约。"

    $ chapter_label = "01 / 珂澜"
    call screen chapter_card("珂澜", "海会记得每一个失眠的人。")
    show kelan at portrait_center with dissolve
    k "你最近睡得好吗？"
    me "这是相亲问题，还是健康调查？"
    k "相亲。我想知道，约你吃早餐会不会很残忍。"
    me "很残忍。尤其是周六。"
    k "那就午餐。午餐睡过了，就下午茶。"
    "她说得很自然，仿佛错过一次约会，也不会错过这个人。"
    me "你做什么工作？"
    k "研究海洋里的声音。偶尔给睡眠电台选音乐，会先把自己听睡着。"
    me "这算工伤吗？"
    k "算效果验收。"
    "她认真回答完，才慢半拍地笑起来。"
    k "我听过你投稿的那个故事。主角一直等一艘不会回来的船。"
    me "那篇没发表。"
    "她的手指停在杯沿。雨声忽然近了一点。"
    k "……那也许是我记错了。"
    k "不过，如果有个人一直等着，你觉得船该回来吗？"
    me "先看那个人，还想不想等。"
    "珂澜看了我很久。不是失落，更像是第一次听见另一种答案。"
    k "好。那我以后先问。"
    "我低头，替她捡起滑到桌下的餐巾。"

    # 视线之外：先隐藏立绘，再切空镜。异象仅向读者展示，主角没有看到。
    hide kelan with dissolve
    scene bg afterhours with dissolve
    $ unease = min(3, unease + 1)
    stop music fadeout 0.7
    play sound "audio/undertow.wav" volume 0.45
    call screen blind_spot("当你低下头")
    "玻璃上的雨水，在同一瞬间停止下落。"
    "倒影里的海平面，比这座城市高出一点。没有浪，也没有岸。"
    k "还不行。"
    "她用手心捂住杯口。那句很轻的话，不是说给林予听的。"
    scene bg cafe with dissolve
    play music "audio/rain.wav" fadein 1.0 volume 0.45
    show kelan at portrait_center with dissolve
    me "你的餐巾。"
    k "谢谢。"
    "她接过去时，指尖终于有了温度。"
    hide kelan with dissolve

    $ chapter_label = "02 / 犹夏"
    call screen chapter_card("犹夏", "每一扇门，都通向一个如果。")
    show youxia at portrait_center with dissolve
    "犹夏坐下来，把糖包往我面前推了一点。"
    y "你下一句会问，我有什么爱好。"
    me "其实我想问，这家店的洗手间在哪。"
    y "……左边第二扇门。"
    "她把笔记本翻到新的一页。我瞥见上一页写满了箭头。"
    me "在做项目方案？"
    y "在准备聊天。"
    me "我有这么难聊吗？"
    y "不是。是可能性太多了。"
    "她说她记路很快，几乎不会迷路；看电影却总在结局前离场。"
    me "怕烂尾？"
    y "怕又猜对。"
    "我把菜单转了一百八十度，闭着眼点了一项。"
    me "那你猜猜，我会点什么。"
    y "焦糖布丁。"
    "我睁开眼。手指下面，写着『禁止吸烟』。"
    "她愣了两秒，笑得肩膀轻轻发抖。"
    y "这一种，我真的没有准备。"
    me "职业编辑，偶尔也会指错行。"
    y "如果我们再见面……你希望知道结果吗？"
    me "约会还是体检？"
    y "约会。包括最好的结果，和最坏的。"

    # 第二个共通选择：自由意志 / 耐心 / 真实，各自回应一条路线的情感主题。
    menu:
        "她没有看笔记本，只看着我。"
        "「先告诉我，你自己想不想来。」":
            $ resonance_y += 1
            y "想。"
            "这次，她回答得比任何一次预测都快。"
            me "那这一项就够了。"
        "「不知道也没关系。我们慢慢试。」":
            $ resonance_k += 1
            y "你不怕浪费时间？"
            me "咖啡都快凉了。可我没觉得今晚浪费了。"
            "她把笔记本合起来，第一次没有夹好书签。"
        "「我比较想知道，没写进方案的你。」":
            $ resonance_n += 1
            $ noticed = True
            $ unease = min(3, unease + 1)
            y "那可能不太像你期待的相亲对象。"
            me "我来的时候，期待的是一位。今晚已经超额完成了。"
            "吧台那边，有人轻轻笑了一声。"

    "店员送来布丁。我转过身，向他道谢。"
    hide youxia with dissolve
    scene bg afterhours with dissolve
    stop music fadeout 0.7
    play sound "audio/chime.wav" volume 0.3
    call screen blind_spot("当你转过身")
    "走廊尽头的门，门缝里透着白昼。"
    "有人在门的另一边，叫了一声林予。声音苍老而熟悉。"
    y "这一晚，请不要替我回答。"
    "她按住笔记本。所有箭头，都安静地停在纸上。"
    scene bg cafe with dissolve
    play music "audio/rain.wav" fadein 1.0 volume 0.45
    show youxia at portrait_center with dissolve
    me "要分一半吗？"
    y "要。"
    "犹夏把自己的勺子递过来。她没有问布丁是什么味道。"
    hide youxia with dissolve

    $ chapter_label = "03 / 奈亚"
    call screen chapter_card("奈亚", "最难学会的表情，是自己的。")
    show naiya at portrait_center with dissolve
    n "到我了。你喜欢安静的，还是话多的？"
    me "你现在这样就挺好。"
    n "这个回答很危险。我现在可能是特意这样的。"
    "她托着下巴，笑得无懈可击。连停顿都恰到好处。"
    n "会做饭，不查手机，不介意你加班。你的每一个冷笑话，我都能笑。"
    me "听起来不像相亲，像购买售后服务。"
    n "大家不都希望，被人喜欢得刚刚好吗？"
    me "那你呢？"
    "她眨了眨眼。"
    me "你喜欢吃什么？不许回答『看你』。"
    n "……很辣的东西。"
    me "我不太能吃辣。"
    "她脸上的笑意短暂地空了一拍。"
    me "所以可以点鸳鸯锅。这个技术已经很成熟了。"
    "奈亚低下头，笑了很久。笑完以后，坐姿也没有刚才那么端正了。"
    n "林予，你这样很影响我的工作。"
    me "品牌顾问？"
    n "让每个人都看见，他最想看见的东西。"
    me "今天下班吧。"
    "她没有马上接话，只把手机按灭了。"
    n "那我能说一句不讨喜的吗？"
    me "能。"
    n "我不想今晚结束得这么快。"
    "我看了一眼窗外。雨似乎小了些。"

    hide naiya with dissolve
    scene bg afterhours with dissolve
    $ unease = min(3, unease + 1)
    stop music fadeout 0.7
    play sound "audio/pulse.wav" volume 0.28
    call screen blind_spot("当你望向窗外")
    "熄灭的手机，在桌面上亮起。"
    "没有号码。只有一条消息：『请确认本次使用的姓名。』"
    "输入框里的光标闪了很久。"
    n "奈亚。"
    "她删掉自动填入的其余名字。一个接着一个。"
    scene bg cafe with dissolve
    play music "audio/rain.wav" fadein 1.0 volume 0.45
    show naiya at portrait_center with dissolve
    me "你刚才说什么？"
    n "说下次想吃火锅。"
    me "鸳鸯锅。"
    n "嗯。你的那一半，可以不放辣。"
    hide naiya with dissolve

    $ chapter_label = "雨停之前"
    "店员终于把门口的营业牌翻了过去。"
    "三位姑娘回到桌边。没有人催我，但那三封邀请还放在那里。"
    "奇怪的是，聊了这么久，墙上的时钟仍然指着二十一点十七分。"
    if noticed:
        "我想起三封同一时间的邀请，还有没发表过的故事。"
        "今晚一定有什么事，不在我所知道的范围里。"
    else:
        "可能只是电池没电。"
        "我决定暂时保留这个，非常普通的解释。"
    "手机震了一下。邀请函最下面，多了一行小字。"
    "『雨将停止。请选择同行者。』"
    me "这次我自己选。"
    "我把手机扣在桌上。"

# 结局页可直接 Jump 到这里重选。重新建立场景与 HUD，不重置本周目共鸣。
label before_final_choice:
    $ chapter_label = "雨停之前"
    $ time_label = "21:17"
    scene bg cafe with dissolve
    play music "audio/rain.wav" fadein 1.0 volume 0.45
    show screen scene_hud

    menu:
        "雨停以后——"
        "「珂澜，明天下午，一起晒太阳吧。」":
            jump ending_kelan
        "「犹夏，我们走一条没准备过的路。」":
            jump ending_youxia
        "「奈亚，吃火锅的时候，你不用上班。」":
            jump ending_naiya
        "「谢谢今晚。我想一个人走回去。」":
            jump ending_alone


# 珂澜：以「主动醒来」回应沉睡 / 深海意象，不以实体化神祇表现恐怖。
label ending_kelan:
    $ chapter_label = "终章 / 醒来以后"
    show kelan at portrait_center with dissolve
    k "太阳……我可能起不来。"
    me "下午三点。再起不来，就四点。"
    k "你会等我？"
    me "会。但睡过头要发消息。"
    "她把手机拿出来，像是终于学会了某种比做梦更困难的联系方式。"
    if resonance_k > 0:
        k "还喝热可可吗？"
        me "喝。给你点一杯真的可以喝的。"
        "她笑着把自己的杯子抱得更紧了一点。"
    else:
        k "我不太擅长，醒着和别人见面。"
        me "我也不太擅长。我们可以都表现得差一点。"
    "临走前，她替我理好被雨打湿的衣领。动作很轻，像怕惊醒什么。"
    k "如果你今晚梦见海，不用往前走。"
    me "你会在岸上？"
    k "我会试着到岸上来。"
    hide kelan with dissolve
    $ time_label = "21:18"
    "我们推开门。时钟轻轻响了一下。"
    stop music fadeout 1.0
    play music "audio/cafe.wav" fadein 1.5 volume 0.3
    "第二天下午三点，我收到一张阳光照进窗台的照片。"
    "『醒了。今天没有让任何人替我做梦。』"
    "我回复：『楼下等你。』"
    scene bg afterhours with dissolve
    call screen blind_spot("而在你看不见的地方")
    "空无一人的咖啡馆里，一只杯子留下浅浅的水印。"
    "水印之外，所有潮汐都安静地等待着。"
    "这一次，她没有回应。"
    $ persistent.endings.add("K-01")
    $ renpy.save_persistent()
    hide screen scene_hud
    call screen ending_card("K-01", "醒来以后", "她第一次，把明天留给了一个具体的人。", "珂澜")
    return


# 犹夏：把知晓所有可能性的能力，收束为愿意接受未知的亲密关系。
label ending_youxia:
    $ chapter_label = "终章 / 未命名的明天"
    show youxia at portrait_center with dissolve
    y "往左走，我们会聊得很投机。往右走——"
    "她停下来，把笔记本收进包里。"
    y "抱歉。职业习惯。"
    me "那就先出门。到了路口再说。"
    if resonance_y > 0:
        y "你确定不想看看方案？最坏的那个也许很糟。"
        me "吵架的时候，允许我当场组织语言就行。"
        y "好。我也当场组织。"
    else:
        y "我可能还是会忍不住猜。"
        me "那猜到了也先别告诉我。惊喜要留一点。"
    "她把一枚小小的钥匙扣递给我。上面是一扇没有编号的门。"
    y "普通纪念品。没有别的用途。"
    me "你特意强调这个，有点可疑。"
    "她笑了。这次没有预先想好怎样笑才最合适。"
    hide youxia with dissolve
    $ time_label = "21:18"
    "出门以后，我们同时往不同的方向迈了一步。"
    "然后停在原地，看着对方笑起来。"
    stop music fadeout 1.0
    play music "audio/cafe.wav" fadein 1.5 volume 0.3
    "我们最后去了街对面，只因为便利店的灯还亮着。"
    "她第一次花了五分钟，挑选一支不知道味道的冰淇淋。"
    scene bg afterhours with dissolve
    call screen blind_spot("而在你看不见的地方")
    "咖啡馆的走廊里，每扇门后都有脚步声渐渐远去。"
    "留下的笔记纸上，所有已写好的结局消失了。"
    "最后一页，只有她新添的一句话：『今天，走错路也算数。』"
    $ persistent.endings.add("Y-01")
    $ renpy.save_persistent()
    hide screen scene_hud
    call screen ending_card("Y-01", "未命名的明天", "她知道所有答案，却愿意等你说出自己的。", "犹夏")
    return


# 奈亚：面具意象只通过职业化表情、姓名和来电呈现，不展示变形画面。
label ending_naiya:
    $ chapter_label = "终章 / 下班后的她"
    show naiya at portrait_center with dissolve
    n "我下班以后，可能会很难伺候。"
    me "举个例子？"
    n "会抢最后一块毛肚。"
    me "这问题很严重。得多点一份。"
    "她没再给出一个恰到好处的微笑，而是向我伸出手。"
    n "重新认识一下。奈亚。喜欢辣，不喜欢被催回复。"
    me "林予。怕辣，偶尔也会晚回消息。"
    if resonance_n > 0:
        n "还有，我刚才有两次觉得你的笑话不好笑。"
        me "只两次？那今晚发挥得不错。"
        "她这次笑得一点也不礼貌。"
    else:
        n "还有，我其实没有那么会做饭。"
        me "我其实没有那么会相亲。"
        n "这个我已经发现了。"
    "她握住我的手。掌心暖得很普通。"
    n "下一次，如果我又开始猜你想听什么，你提醒我。"
    me "好。暗号是『下班了』。"
    hide naiya with dissolve
    $ time_label = "21:18"
    "推门时，她抢先撑开伞。"
    me "雨已经停了。"
    n "我知道。但我现在就想和你共一把。"
    stop music fadeout 1.0
    play music "audio/cafe.wav" fadein 1.5 volume 0.3
    "回家的路上，她发来九家火锅店，让我负责删掉八家。"
    "消息的最后，是一个拍糊了的表情包。很不专业。我保存了。"
    scene bg afterhours with dissolve
    call screen blind_spot("而在你看不见的地方")
    "吧台上的座机响了。一次。又一次。"
    "来电显示不断变换着名字。没有一个叫奈亚。"
    "今晚，无人接听。"
    $ persistent.endings.add("N-01")
    $ renpy.save_persistent()
    hide screen scene_hud
    call screen ending_card("N-01", "下班后的她", "在无数个名字之中，她开始偏爱你叫的那一个。", "奈亚")
    return


# 离席同样是完整且被尊重的选择；第四份邀请保留续作入口。
label ending_alone:
    $ chapter_label = "终章 / 第四份邀请"
    "说完这句话，桌边反而轻松了下来。"
    show youxia at portrait_center with dissolve
    y "这也是一个有效的选择。"
    hide youxia with dissolve
    show kelan at portrait_center with dissolve
    k "回去早点睡。没有梦也很好。"
    hide kelan with dissolve
    show naiya at portrait_center with dissolve
    n "下次如果再见，不许装作不认识。"
    me "不会。今晚已经很难忘了。"
    hide naiya with dissolve
    "我拿起外套。没有人阻拦，也没有人要求一个更漂亮的理由。"
    $ time_label = "21:18"
    "门外的空气很凉。城市重新有了车流声。"
    stop music fadeout 1.0
    play music "audio/cafe.wav" fadein 1.5 volume 0.3
    "我走过两条街，手机又震了一下。"
    "第四份邀请。"
    "『明晚，二十一点十七分。余温咖啡馆。』"
    "邀请人的名字，是林予。"
    me "……这系统真的该修了。"
    "我没有点开，把手机放回口袋，继续往家走。"
    scene bg afterhours with dissolve
    call screen blind_spot("而在你看不见的地方")
    "咖啡馆里，三个人望着那把空椅子。"
    y "他没有选我们。"
    k "他选了自己。"
    n "那下一次——"
    "她把桌上的第四只杯子，也翻了过来。"
    n "就由他邀请吧。"
    $ persistent.endings.add("H-01")
    $ renpy.save_persistent()
    hide screen scene_hud
    call screen ending_card("H-01", "第四份邀请", "今晚，他平安到家。故事还没有替他作答。", "林予")
    return
