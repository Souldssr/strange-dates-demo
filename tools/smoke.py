"""用 Ren'Py 自带 testcase 验证实际渲染、菜单与剧情，不控制用户桌面。

测试脚本只注入 .qa 临时工程，永不随正式游戏分发。
运行：python tools/smoke.py [--sdk PATH] [--case portfolio_ui]
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    default_sdk = root / ".tools" / "renpy-8.2.0-sdk"
    # 外部 SDK 通过环境变量或 --sdk 指定，避免公开本机安装路径。
    if not default_sdk.exists() and os.environ.get("RENPY_SDK"):
        default_sdk = Path(os.environ["RENPY_SDK"])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk", type=Path, default=default_sdk)
    parser.add_argument("--distribution", type=Path, help="改用已解压发行包自带的 Python 和引擎验证，不依赖 SDK。")
    parser.add_argument("--case", action="append", dest="cases")
    args = parser.parse_args()
    cases = args.cases or ["portfolio_ui", "complete_story"]
    runtime_root = args.distribution or args.sdk
    runtime = runtime_root / "lib/py3-windows-x86_64/python.exe"
    engine = runtime_root / ("StrangeDates.py" if args.distribution else "renpy.py")
    if not runtime.exists() or not engine.exists():
        parser.error("Ren'Py SDK 未找到，请用 --sdk 指定路径。")

    # 每次新建测试镜像，避免旧脚本 / 旧存档干扰，也不删除开发者文件。
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    scratch = root / ".qa" / run_id
    output = root / "build" / "screenshots"
    output.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        (args.distribution or root) / "game", scratch / "game",
        ignore=shutil.ignore_patterns("*.rpyc", "cache", "saves"),
    )
    test_source = (root / "tools" / "smoke.rpy").read_text(encoding="utf-8")
    test_source = test_source.replace("__QA_OUTPUT__", output.as_posix())
    (scratch / "game" / "zz_smoke.rpy").write_text(test_source, encoding="utf-8")

    env = os.environ.copy()
    env.update({
        # 8.2 的 test 子命令默认 dummy video；显式使用 Windows 才能实际渲染。
        "SDL_VIDEODRIVER": "windows",
        "SDL_AUDIODRIVER": "dummy",
        "RENPY_RENDERER": "angle2",
        "RENPY_PATH_TO_SAVES": str(scratch / "saves"),
        "RENPY_LOG_BASE": str(scratch),
    })
    results = []
    for case in cases:
        print(f"Ren'Py testcase: {case}", flush=True)
        try:
            result = subprocess.run(
                [str(runtime), str(engine), str(scratch), "test", case],
                cwd=str(root), env=env, capture_output=True, timeout=180,
            )
            log = result.stdout + result.stderr
            (root / "build" / f"qa-{case}.log").write_bytes(log)
            results.append({"case": case, "exit_code": result.returncode})
            print(log.decode("utf-8", errors="replace"), flush=True)
            if result.returncode:
                print(f"失败日志：build/qa-{case}.log", flush=True)
                break
        except subprocess.TimeoutExpired as exc:
            (root / "build" / f"qa-{case}.log").write_bytes((exc.stdout or b"") + (exc.stderr or b""))
            results.append({"case": case, "exit_code": "timeout"})
            break
    report = {"run_id": run_id, "runtime": str(runtime_root), "distribution": bool(args.distribution), "results": results}
    (root / "build" / "qa-results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    # 分别保留每个用例的最新结果，便于在 UI 与剧情分开运行时追溯。
    for item in results:
        detail = dict(report, results=[item])
        suffix = "-release" if args.distribution else ""
        (root / "build" / ("qa-result-" + item["case"] + suffix + ".json")).write_text(json.dumps(detail, indent=2), encoding="utf-8")
    return 0 if all(r["exit_code"] == 0 for r in results) and len(results) == len(cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
