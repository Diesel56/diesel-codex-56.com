## Genesis Editor + CLI Integration Guide

This guide shows how to keep Cursor, Claude Code, and VS Code in sync through the shared `genesis_cli.py` tooling. The same commands now work on Windows (both x86 and x64) and on Linux/macOS.

### 1. Prerequisites (all platforms)
- Install Python 3.10+; 64-bit builds are preferred, but the CLI also runs on 32-bit.
- Clone this repository and open it as a workspace in your editor of choice.
- Optional but recommended: create a virtual environment so each editor uses the same interpreter.

```bash
python3 -m venv .venv
source .venv/bin/activate               # Linux/macOS
# or on Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

Run the diagnostics once to capture your platform profile:

```bash
python genesis_cli.py doctor            # linux/macOS use python3 if needed
```

The `doctor` command records OS, architecture (32/64-bit), Python path, and missing dependencies so every teammate sees the same snapshot.

### 2. Windows-specific notes
- **64-bit:** install the standard x86-64 Python build from python.org and ensure `Add python.exe to PATH` is enabled. SpeechRecognition ships pre-built wheels for 64-bit, so `install-deps` succeeds without extra compilers.
- **32-bit:** install the x86 MSI. If `python` launches the Windows Store stub, run `py -3` inside editors or set `GENESIS_PYTHON=py -3`. Some Whisper wheels are heavy; if `install-deps` fails due to memory, use the `--no-cache-dir` flag manually (`python genesis_cli.py run whisper-cli -- --no-cache-dir`).
- **PowerShell policy:** VS Code, Cursor, and Claude Code all reuse the same integrated terminal. If scripts are blocked, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

### 3. Linux/macOS notes
- Ensure `python3`, `build-essential`, and `portaudio` headers are installed for the audio tooling.
- On Apple Silicon, `doctor` reports `arm64`. Dependencies install with `python3 -m pip install -r requirements.txt`.
- If you are on a 32-bit Linux image, the CLI automatically reports `bits: 32bit` and you may need `sudo apt install gfortran libatlas-base-dev` for Whisper.

### 4. Shared Genesis CLI usage
- `python genesis_cli.py doctor` — confirm architecture + dependency readiness.
- `python genesis_cli.py install-deps` — install/update `SpeechRecognition` & `openai-whisper`.
- `python genesis_cli.py list-tasks` — discover the canonical Diesel tasks.
- `python genesis_cli.py run diesel-agent` — run any mapped script (pass extra args after the task name).

The CLI writes `.genesis/config.json` so every editor sees identical metadata (workspace root, interpreter, task catalog). Override the interpreter per session with `GENESIS_PYTHON` or `--python`.

### 5. Editor integrations

#### Cursor
- Cursor reads `.vscode/tasks.json` automatically. Open the **Command Palette → Tasks: Run Task** and select any `Genesis • ...` entry (Doctor, Install deps, Diesel agent, Deploy).
- Because Cursor shares the VS Code engine, the same recommended extensions listed in `.vscode/extensions.json` (Python, Pylance, Ruff, PowerShell) get installed automatically.
- To pin the Genesis CLI to a custom interpreter, set `"python.defaultInterpreterPath"` inside your Cursor settings or export `GENESIS_PYTHON` before launching Cursor.

#### VS Code
- Open the workspace folder. VS Code detects `.vscode/tasks.json` and surfaces the same Genesis tasks.
- Assign keyboard shortcuts (e.g. `Tasks: Configure Task` → `Genesis • Diesel agent`) so you can trigger CLI routines without leaving the editor.
- Use the Python extension’s status bar to select the `.venv` interpreter; the tasks inherit that interpreter via `sys.executable`.

#### Claude Code (Anthropic)
- Claude Code supports VS Code tasks when you connect a local folder. After opening this repo, use **Cmd/Ctrl+Shift+P → Tasks: Run Task** to access the Genesis entries exactly as in VS Code/Cursor.
- If Claude Code runs inside a Windows sandbox, ensure `python.exe` is reachable. You can point Claude Code to the same `.venv` by launching it from an environment where `GENESIS_PYTHON` is set (e.g. `setx GENESIS_PYTHON "C:\\path\\to\\repo\\.venv\\Scripts\\python.exe"`).
- For remote Claude projects, sync the `.genesis/config.json` file so the CLI knows which interpreter to call on the remote host.

### 6. Symbiotic workflow
- **Single source of truth:** editors call `genesis_cli.py` instead of bespoke scripts. Tasks stay identical across tools and architectures.
- **Architecture awareness:** `doctor` surfaces OS + 32/64-bit info so mismatches are obvious before you share artifacts.
- **Dependency parity:** `install-deps` enforces the same Python wheels everywhere; fallbacks for 32-bit Windows are documented above.
- **Human-in-the-loop:** regardless of whether you are in Cursor chat, Claude Code, or vanilla VS Code, the `Genesis • …` tasks appear with the same names, so debugging steps transfer 1:1.

### 7. Troubleshooting
- **Python command not found:** export `GENESIS_PYTHON` (Linux/macOS) or `setx GENESIS_PYTHON` (Windows) to the interpreter you want tasks to run.
- **Audio backends missing:** install `portaudio` (`brew install portaudio` or `sudo apt install portaudio19-dev`) before running Whisper or mic loops.
- **Permissions on Windows 32-bit:** run terminals as Administrator only for installing dependencies; normal CLI execution works without elevation.

With this setup, you can bounce between Cursor (AI pair), Claude Code (co-creative agent), and VS Code (primary IDE) while sharing a single Genesis CLI surface area across every architecture.
