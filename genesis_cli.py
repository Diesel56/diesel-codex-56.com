#!/usr/bin/env python3
"""Shared Genesis CLI for Diesel Codex tooling.

This CLI provides a single entry-point that every editor (Cursor, Claude Code,
VS Code) can call to run the same workflows regardless of host OS/architecture.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Sequence

REPO_ROOT = Path(__file__).resolve().parent
CONFIG_DIR = REPO_ROOT / ".genesis"
CONFIG_FILE = CONFIG_DIR / "config.json"
REQUIREMENTS_FILE = REPO_ROOT / "requirements.txt"


def _python_command(override: str | None = None) -> str:
    if override:
        return override
    env_override = os.environ.get("GENESIS_PYTHON")
    if env_override:
        return env_override
    return sys.executable


def _task_command(entry: Dict[str, str], py_cmd: str) -> List[str]:
    kind = entry.get("type", "python")
    target = entry["target"]
    if kind == "python":
        script = REPO_ROOT / target
        return [py_cmd, str(script)]
    if kind == "module":
        return [py_cmd, "-m", target]
    if kind == "shell":
        return [target]
    raise ValueError(f"Unsupported task type: {kind}")


TASKS: Dict[str, Dict[str, str]] = {
    "diesel-agent": {
        "description": "Scan the vault and refresh manifest data",
        "type": "python",
        "target": "diesel-agent.py",
    },
    "vault-viewer": {
        "description": "Inspect Codex manifest entries in the terminal",
        "type": "python",
        "target": "vault_viewer.py",
    },
    "get-codex": {
        "description": "Fetch a Codex pattern into the local vault",
        "type": "python",
        "target": "get_codex.py",
    },
    "whisper-cli": {
        "description": "Simulate Whisper transcription for Codex input",
        "type": "python",
        "target": "whisper-cli.py",
    },
    "voice-loop": {
        "description": "Run the voice loop interface",
        "type": "python",
        "target": "voice-loop.py",
    },
    "deploy": {
        "description": "Generate the Diesel drop deployment bundle",
        "type": "python",
        "target": "deploy.py",
    },
}


DEFAULT_CONFIG = {
    "workspace_root": str(REPO_ROOT),
    "python": sys.executable,
    "tasks": TASKS,
}


REQ_IMPORT_MAP = {
    "SpeechRecognition": "speech_recognition",
    "openai-whisper": "whisper",
}


def ensure_config() -> Dict[str, object]:
    CONFIG_DIR.mkdir(exist_ok=True)
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
    else:
        data = DEFAULT_CONFIG
    data["workspace_root"] = str(REPO_ROOT)
    data["python"] = data.get("python") or sys.executable
    data["tasks"] = TASKS
    with CONFIG_FILE.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, indent=2)
    return data


def detect_platform_profile() -> Dict[str, str]:
    bits, linkage = platform.architecture()
    return {
        "os": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor() or "unknown",
        "bits": bits,
        "linkage": linkage,
        "is_64bit": "yes" if bits == "64bit" else "no",
    }


def read_requirements() -> List[str]:
    if not REQUIREMENTS_FILE.exists():
        return []
    requirements: List[str] = []
    for raw_line in REQUIREMENTS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        requirements.append(line)
    return requirements


def find_missing_dependencies() -> List[str]:
    missing: List[str] = []
    for requirement in read_requirements():
        pkg_name = requirement.split("==")[0]
        module_name = REQ_IMPORT_MAP.get(pkg_name, pkg_name.replace("-", "_"))
        if importlib.util.find_spec(module_name) is None:
            missing.append(pkg_name)
    return missing


def cmd_doctor(_: argparse.Namespace) -> int:
    ensure_config()
    profile = detect_platform_profile()
    print("Genesis CLI Diagnostics")
    print("-----------------------")
    print(f"OS           : {profile['os']} {profile['release']} ({profile['version']})")
    print(f"Machine      : {profile['machine']}")
    print(f"Processor    : {profile['processor']}")
    print(f"Architecture : {profile['bits']} (64-bit? {profile['is_64bit']})")
    print(f"Python       : {sys.version.split()[0]} @ {sys.executable}")
    missing = find_missing_dependencies()
    if missing:
        print("\nMissing Python dependencies detected:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("Run `genesis_cli.py install-deps` to install them.")
    else:
        print("\nPython dependencies: OK")
    return 0


def cmd_install_deps(args: argparse.Namespace) -> int:
    ensure_config()
    if not REQUIREMENTS_FILE.exists():
        print("requirements.txt not found; nothing to install.")
        return 0
    pip_args: List[str] = [
        _python_command(args.python_override),
        "-m",
        "pip",
        "install",
    ]
    if args.upgrade:
        pip_args.append("--upgrade")
    pip_args.extend(["-r", str(REQUIREMENTS_FILE)])
    print("Executing:", " ".join(pip_args))
    result = subprocess.run(pip_args, cwd=REPO_ROOT, check=False)
    return result.returncode


def cmd_list_tasks(_: argparse.Namespace) -> int:
    ensure_config()
    print("Available Genesis tasks:")
    for name, meta in TASKS.items():
        print(f"  - {name:<14} {meta['description']}")
    return 0


def cmd_run_task(args: argparse.Namespace) -> int:
    ensure_config()
    task_name = args.task
    if task_name not in TASKS:
        print(f"Unknown task '{task_name}'. Run `list-tasks` to see options.")
        return 1
    py_cmd = _python_command(args.python_override)
    base_command = _task_command(TASKS[task_name], py_cmd)
    command = base_command + list(args.extra)
    print("Executing:", " ".join(command))
    result = subprocess.run(command, cwd=REPO_ROOT, check=False)
    return result.returncode


def cmd_show_config(_: argparse.Namespace) -> int:
    config = ensure_config()
    print(json.dumps(config, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Genesis CLI bridge for editor + architecture parity."
    )
    parser.add_argument(
        "--python",
        dest="python_override",
        help="Explicit python interpreter to use when spawning tasks",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Run environment diagnostics")
    doctor.set_defaults(func=cmd_doctor)

    install = subparsers.add_parser(
        "install-deps", help="Install Python dependencies from requirements.txt"
    )
    install.add_argument(
        "--upgrade", action="store_true", help="Upgrade packages to latest versions"
    )
    install.set_defaults(func=cmd_install_deps)

    subparsers.add_parser("list-tasks", help="List known Genesis tasks").set_defaults(
        func=cmd_list_tasks
    )

    run = subparsers.add_parser("run", help="Execute a specific Genesis task")
    run.add_argument("task", choices=sorted(TASKS.keys()), help="Task name to execute")
    run.add_argument(
        "extra",
        nargs=argparse.REMAINDER,
        help="Additional arguments passed to the underlying task",
    )
    run.set_defaults(func=cmd_run_task)

    subparsers.add_parser(
        "show-config", help="Print the resolved Genesis config"
    ).set_defaults(func=cmd_show_config)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
