"""生成原创氛围声音与几何 UI 素材；不读取、不修改角色或背景原画。

依赖：numpy、Pillow。执行本文件即可确定性重建所有输出。
声音为原创程序合成，无外部采样；循环声采用周期噪声和跨边界音符。
"""

from pathlib import Path
import wave

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
AUDIO = ROOT / "game" / "audio"
GUI = ROOT / "game" / "gui"
RATE = 44100
LOOP_SECONDS = 24


def noise(seconds, seed, low, high):
    """用频域滤波生成完整周期的柔和噪声，不在文件边界截断随机片段。"""
    count = int(seconds * RATE)
    rng = np.random.default_rng(seed)
    freq = np.fft.rfftfreq(count, 1 / RATE)
    response = (1 - np.exp(-((freq / low) ** 2))) * np.exp(-((freq / high) ** 2))
    spectrum = np.fft.rfft(rng.standard_normal(count)) * response
    spectrum[0] = 0
    signal = np.fft.irfft(spectrum, n=count)
    return signal / max(np.std(signal), 1e-9)


def stereo_noise(seconds, seed, low, high, width=0.2):
    """共享主体加轻微独立分量，保留稳定的中央声像。"""
    middle = noise(seconds, seed, low, high)
    left = middle + width * noise(seconds, seed + 1, low, high)
    right = middle + width * noise(seconds, seed + 2, low, high)
    return np.column_stack((left, right))


def close_loop(signal):
    """用 25ms 平滑校正令首末电平完全相同，消除播放器接缝点击。"""
    signal = signal.copy()
    count = int(0.025 * RATE)
    taper = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, count))
    middle = (signal[0] + signal[-1]) * 0.5
    signal[:count] += (middle - signal[0])[None, :] * taper[:, None]
    signal[-count:] += (middle - signal[-1])[None, :] * taper[::-1, None]
    return signal


def write_wav(name, signal, rms, loop=False):
    """输出克制音量的 44.1kHz、双声道、16位 PCM，并报告有效电平。"""
    signal = signal - signal.mean(axis=0)
    if loop:
        signal = close_loop(signal)
    signal *= rms / max(np.sqrt(np.mean(signal * signal)), 1e-9)
    peak = float(np.max(np.abs(signal)))
    if peak > 0.55:
        signal *= 0.55 / peak
    pcm = np.round(signal * 32767).astype("<i2")
    with wave.open(str(AUDIO / f"{name}.wav"), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(RATE)
        handle.writeframes(pcm.tobytes())
    print(f"{name}: {len(pcm) / RATE:.1f}s, RMS={np.sqrt(np.mean(signal**2)):.4f}, "
          f"peak={np.max(np.abs(signal)):.4f}, seam={np.max(np.abs(pcm[0].astype(int)-pcm[-1].astype(int)))}")


def electric_piano(t, offset, frequency, pan=0.0):
    """柔和电钢琴音色，带有限长衰减；取模时间让音符尾音自然跨循环。"""
    age = np.mod(t - offset, LOOP_SECONDS)
    attack = 1 - np.exp(-age / 0.025)
    release = np.clip((7.5 - age) / 1.5, 0, 1)
    envelope = attack * np.exp(-age / 2.5) * release * release
    tone = (np.sin(2 * np.pi * frequency * age)
            + 0.19 * np.exp(-age / 0.8) * np.sin(2 * np.pi * frequency * 2 * age)
            + 0.045 * np.exp(-age / 0.6) * np.sin(2 * np.pi * frequency * 3 * age))
    mono = envelope * tone
    return np.column_stack((mono * (1 - pan), mono * (1 + pan)))


def make_audio():
    t = np.arange(LOOP_SECONDS * RATE) / RATE

    # 窗外细雨：不含雷击、尖锐水滴或突然的动态变化。
    rain = stereo_noise(LOOP_SECONDS, 104, 250, 4600, 0.28)
    rain *= (0.91 + 0.055 * np.sin(2 * np.pi * t / 12)
             + 0.035 * np.sin(2 * np.pi * t / 8))[:, None]
    write_wav("rain", rain, rms=0.032, loop=True)

    # 三组稀疏的柔和和弦，演奏留出大量空白给阅读。
    cafe = stereo_noise(LOOP_SECONDS, 208, 350, 2800, 0.15) * 0.0014
    chords = [(1.3, [174.614, 220.0, 261.626, 329.628]),
              (9.3, [164.814, 220.0, 293.665, 349.228]),
              (17.3, [146.832, 196.0, 246.942, 329.628])]
    for offset, notes in chords:
        for index, frequency in enumerate(notes):
            cafe += 0.034 * electric_piano(t, offset + index * 0.13, frequency,
                                          pan=(index - 1.5) * 0.08)
    write_wav("cafe", cafe, rms=0.022, loop=True)

    # 没有具象怪物叫声：仅使用远处低频和漂浮的泛音制造空旷感。
    undertow = stereo_noise(LOOP_SECONDS, 312, 24, 110, 0.12) * 0.014
    for frequency, gain, phase in [(41.0, 0.038, 0.0), (61.5, 0.014, 0.3),
                                    (123.0, 0.006, 1.1), (246.0, 0.0025, 2.0)]:
        amplitude = 0.88 + 0.12 * np.sin(2 * np.pi * t / 12 + phase)
        left = gain * amplitude * np.sin(2 * np.pi * frequency * t + phase)
        right = gain * amplitude * np.sin(2 * np.pi * frequency * t + phase + 0.07)
        undertow += np.column_stack((left, right))
    write_wav("undertow", undertow, rms=0.029, loop=True)

    # 轻铃：圆润的起音、自然的衰减和结束淡出。
    t = np.arange(int(1.8 * RATE)) / RATE
    chime = np.zeros_like(t)
    for multiplier, gain, decay in [(1, 1, 0.65), (2.71, 0.12, 0.31), (4.13, 0.035, 0.2)]:
        chime += gain * np.sin(2 * np.pi * 659.255 * multiplier * t) * np.exp(-t / decay)
    chime *= (1 - np.exp(-t / 0.012)) * np.clip((1.8 - t) / 0.4, 0, 1) ** 2
    write_wav("chime", np.column_stack((chime, chime * 0.94)), rms=0.036)

    # 单次低沉心跳（双搏组成一次心动），避免突发峰值。
    t = np.arange(int(1.5 * RATE)) / RATE
    pulse = np.zeros_like(t)
    for start, gain, frequency in [(0.14, 1.0, 53), (0.40, 0.55, 47)]:
        age = np.maximum(t - start, 0)
        envelope = (age / 0.025) ** 2 * np.exp(-age / 0.028)
        envelope[t < start] = 0
        pulse += gain * envelope * np.sin(2 * np.pi * frequency * age)
    pulse *= np.clip((1.5 - t) / 0.3, 0, 1) ** 2
    write_wav("pulse", np.column_stack((pulse, pulse)), rms=0.034)


def rgba_field(width, height, rgb, alpha):
    canvas = np.zeros((height, width, 4), dtype=np.uint8)
    canvas[:, :, :3] = rgb
    canvas[:, :, 3] = np.clip(alpha, 0, 255).astype(np.uint8)
    return Image.fromarray(canvas)


def make_gui():
    # 菜单左边稳定承载标题和按钮，右边渐隐，底部稍加暗色。
    x = np.arange(1600)[None, :]
    y = np.arange(900)[:, None]
    gradient = np.clip((x - 580) / 900, 0, 1)
    gradient = gradient * gradient * (3 - 2 * gradient)
    left = 249 * (1 - gradient)
    bottom = 60 * np.clip((y - 720) / 180, 0, 1) ** 1.5
    combined = 255 - (255 - left) * (255 - bottom) / 255
    rgba_field(1600, 900, (16, 29, 34), combined).save(GUI / "menu_veil.png")

    dialogue = Image.new("RGBA", (1600, 260), (16, 27, 34, 245))
    ImageDraw.Draw(dialogue).line([(0, 0), (1599, 0)], fill=(204, 177, 124, 145), width=1)
    dialogue.save(GUI / "dialogue.png")

    # 轻微暗角，只在边缘出现，避免压暗人物面部。
    horizontal = np.clip((np.abs(x - 799.5) - 590) / 210, 0, 1) ** 2
    vertical = np.clip((np.abs(y - 449.5) - 340) / 110, 0, 1) ** 2
    rgba_field(1600, 900, (0, 0, 0), 28 * horizontal + 28 * vertical).save(GUI / "vignette.png")

    # 原创几何图标：细金环中的简约咖啡杯，以 4 倍采样获得干净边缘。
    scale = 4
    icon = Image.new("RGBA", (256 * scale, 256 * scale), (16, 29, 34, 255))
    draw = ImageDraw.Draw(icon)
    gold = (201, 175, 121, 255)
    white = (239, 236, 222, 255)
    draw.ellipse((24 * scale, 24 * scale, 232 * scale, 232 * scale), outline=gold, width=2 * scale)
    draw.ellipse((162 * scale, 103 * scale, 197 * scale, 146 * scale), outline=white, width=6 * scale)
    draw.rounded_rectangle((74 * scale, 100 * scale, 169 * scale, 162 * scale),
                           radius=15 * scale, fill=white)
    draw.rectangle((74 * scale, 98 * scale, 169 * scale, 117 * scale), fill=white)
    draw.line((67 * scale, 177 * scale, 185 * scale, 177 * scale), fill=white, width=5 * scale)
    for start in (103, 133):
        draw.arc((start * scale, 65 * scale, (start + 16) * scale, 91 * scale),
                 start=85, end=270, fill=gold, width=3 * scale)
    small_icon = icon.resize((256, 256), Image.Resampling.LANCZOS)
    small_icon.save(GUI / "icon.png")
    # 同源导出 Windows 程序图标，供 Ren'Py 打包时自动嵌入可执行文件。
    small_icon.save(ROOT / "icon.ico", format="ICO",
                    sizes=[(size, size) for size in (16, 32, 48, 64, 128, 256)])
    for name in ("menu_veil", "dialogue", "vignette", "icon"):
        with Image.open(GUI / f"{name}.png") as image:
            print(f"{name}: {image.size}, {image.mode}")


if __name__ == "__main__":
    AUDIO.mkdir(parents=True, exist_ok=True)
    GUI.mkdir(parents=True, exist_ok=True)
    make_audio()
    make_gui()
