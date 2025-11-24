# Genesis CLI + Editor Symbiosis Guide

This guide describes how to keep the Genesis CLI, Cursor, Claude Code, and vanilla VS Code in lockstep on Windows across both 32-bit (x86) and 64-bit (x64) systems. The objective is to ensure that every tool invokes the exact same CLI bits, virtual environments, and automation so that decisions made in one editor are immediately reproducible in the others.

---

## 1. Pre-flight Checklist

| Step | Why it matters | Command / Action |
| --- | --- | --- |
| Verify architecture | Determines which Genesis CLI binary & Python wheels to install | `powershell -c "$Env:PROCESSOR_ARCHITECTURE"` or `python - <<<'import platform; print(platform.architecture())'` |
| Install Python ≥ 3.10 (x86 or x64) | Needed because the repo ships Python entry points (`deploy.py`, `voice-loop.py`, etc.) | Use the Microsoft Store build (x64 only) or grab the appropriate installer from python.org (`Windows installer (32-bit)` if you truly need x86) |
| Install Git + OpenSSL | Required by Cursor/VS Code terminals and Genesis CLI auth flows | `winget install --id Git.Git` (x64) or `choco install git --x86` |
| Ensure PowerShell RemoteSigned | Allows helper bootstrap scripts to run without being blocked | `powershell -c "Set-ExecutionPolicy -Scope CurrentUser RemoteSigned"` |

---

## 2. Acquire & Register the Genesis CLI

1. **Grab the right binary**
   - x64: `genesis-cli-<version>-win-x64.zip`
   - x86: `genesis-cli-<version>-win-x86.zip`
   - Place the extracted `genesis.exe` inside `C:\Tools\genesis\<version>\{x64|x86}`.

2. **Package-manager alternatives**

| Architecture | Package manager command | Notes |
| --- | --- | --- |
| x64 | `winget install --id Genesis.CLI --architecture x64` | Installs to `C:\Program Files\GenesisCLI` by default |
| x86 | `choco install genesis-cli --x86 --version=<version>` | Forces Chocolatey to pick the 32-bit MSI |

3. **PATH harmonisation**
   - System PATH: `C:\Tools\genesis\<version>\bin`
   - User PATH fallback for non-admin installs: `%USERPROFILE%\AppData\Local\GenesisCLI\bin`
   - Confirm with `genesis --version` from a new PowerShell window.

4. **Python shim (optional but recommended)**

Create `scripts/genesis.ps1` (or `.cmd`) so every editor launches the CLI through a single entry point:

```powershell
param([Parameter(Position=0)] [string]$GenesisCommand = "help")
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$envFile = Join-Path $root "..\.env"
if (Test-Path $envFile) {
  Get-Content $envFile | Where-Object {$_ -match "="} | foreach-object {
    $name,$value = $_.Split("=",2)
    [System.Environment]::SetEnvironmentVariable($name,$value)
  }
}
& "C:\Tools\genesis\current\genesis.exe" $GenesisCommand @args
exit $LASTEXITCODE
```

Symlink `C:\Tools\genesis\current` to the actual version to make upgrades atomic.

---

## 3. Shared Workspace Baseline

1. **Clone once for all editors**
   ```powershell
   git clone https://github.com/<org>/<repo>.git C:\work\genesis
   ```
2. **Create a universal virtual environment (per architecture)**
   ```powershell
   cd C:\work\genesis
   py -3.11 -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Bootstrap the CLI linkage**
   ```powershell
   scripts\genesis.ps1 doctor
   ```
4. **Record machine-specific overrides in `.env.local` (ignored) and keep `.env.example` checked in so the same variables flow into all editors.**

---

## 4. Editor-Specific Integration

### 4.1 Cursor (Windows x64 & x86)

Cursor inherits the VS Code task system, so we reuse `.vscode/tasks.json` and `.vscode/settings.json`:

- **Tasks** – expose Genesis CLI workflows:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "genesis:plan",
      "type": "shell",
      "command": "${workspaceFolder}\\\\scripts\\\\genesis.ps1",
      "args": ["plan", "--workspace", "${workspaceFolder}"],
      "problemMatcher": [],
      "options": { "shell": { "executable": "powershell.exe" } }
    },
    {
      "label": "genesis:deploy",
      "dependsOn": "genesis:plan",
      "type": "shell",
      "command": "${workspaceFolder}\\\\scripts\\\\genesis.ps1",
      "args": ["deploy"]
    }
  ]
}
```

- **Settings** – enforce the shared PowerShell profile and virtual environment:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}\\\\.venv\\\\Scripts\\\\python.exe",
  "terminal.integrated.profiles.windows": {
    "PowerShell (Genesis)": {
      "path": "C:\\\\Windows\\\\System32\\\\WindowsPowerShell\\\\v1.0\\\\powershell.exe",
      "args": ["-NoLogo", "-ExecutionPolicy", "Bypass", "-File", "${workspaceFolder}\\\\scripts\\\\enter-shell.ps1"]
    }
  },
  "terminal.integrated.defaultProfile.windows": "PowerShell (Genesis)"
}
```

- **Cursor Rules** – add `cursor/rules/genesis.md` reminding the AI agent to run the `genesis:*` tasks when automation is needed.

### 4.2 Claude Code (Claude Desktop ≥ 0.6.0)

1. Enable **Local Workspaces** inside Claude Desktop → Settings → Labs.
2. Add `C:\work\genesis` as a workspace; Claude will mirror the repo but leaves files in place.
3. Open the **Terminal** panel → choose the same PowerShell profile used above so `scripts\genesis.ps1` is on the PATH.
4. Define reusable commands through `Claude Workspace Settings → Commands` (Beta) pointing to the wrapper script, e.g.:
   - *Genesis Plan*: `scripts\genesis.ps1 plan --workspace %cd%`
   - *Genesis Deploy*: `scripts\genesis.ps1 deploy --env %GENESIS_ENV%`
5. Because Claude Code sandboxes each terminal instance, explicitly run `.venv\Scripts\activate` (or call the wrapper script, which in turn activates the env) at the start of every session.
6. Claude’s AI pair-programmer can execute shell commands; pin a system prompt reminding it to rely on the `genesis:*` commands rather than ad-hoc scripts to avoid configuration drift.

> **Note:** Claude Code currently ships only as a 64-bit desktop app. On 32-bit hardware, use Claude in the browser and point it to a Codespace/remote Windows VM that exposes the same wrapper scripts.

### 4.3 VS Code (Stable/Insiders)

VS Code will consume the exact same `.vscode` folder as Cursor, so most configuration is already covered. Add the following to complete the loop:

1. **Extensions** – install `ms-python.python`, `GitHub.vscode-pull-request-github`, and any Genesis-specific extension pack if provided.
2. **Launch configs** – if you debug CLI-powered scripts (`deploy.py`, `voice-loop.py`), add entries to `.vscode/launch.json` pointing to `${workspaceFolder}/.venv/Scripts/python.exe`.
3. **Dev Containers (optional)** – if you need a portable 64-bit Linux environment on a 32-bit Windows host, create `.devcontainer/devcontainer.json` that boots a container with the same Genesis CLI plus Python stack. Both Cursor and VS Code can open the repo inside that container, keeping parity with Claude’s remote shell.

---

## 5. Cross-Editor Handshake Patterns

- **Single Source of Truth** – the `scripts/genesis.ps1` wrapper plus `.env` file is the canonical way to choose config, secrets, and architecture-specific switches.
- **Task Labels** – always use the `genesis:<action>` naming scheme so any editor (or AI agent) can discover available workflows via `Tasks: Run Task`.
- **Process Isolation** – prefer `--workspace ${workspaceFolder}` (Cursor/VS Code) and `%cd%` (Claude) so commands operate inside whichever repository root each editor has opened.
- **Pre-flight validation** – schedule `genesis doctor` (or equivalent) inside CI to match the local workflow, ensuring that editor macros do not mask missing dependencies on x86 hardware.

---

## 6. Verification Matrix

| Scenario | Validation command | Expected result |
| --- | --- | --- |
| Cursor on Win x64 | `Tasks: Run Task → genesis:plan` | CLI prints resolved architecture `windows-x64`, exits 0 |
| Cursor on Win x86 | Same as above | CLI prints `windows-x86`; wrapper points to x86 binary |
| Claude Code on remote VM | `scripts/genesis.ps1 doctor` | Passes env + credential checks |
| VS Code Debug Session | F5 on `deploy.py` with `PYTHONPATH` from `.env` | Breakpoints hit with CLI-supplied config |

If any entry fails, rerun `scripts/genesis.ps1 doctor --verbose` and compare PATH plus binary hashes between machines.

---

## 7. Troubleshooting

- **`genesis.exe` refuses to run on x86:** confirm a 32-bit binary exists; if not, install the CLI into a lightweight 64-bit Windows VM (Hyper-V or WSLg) and expose it through `remote` extensions.
- **Cursor AI tool attempts to run `python` instead of `scripts/genesis.ps1`:** add a rule in `cursor/rules/genesis.md` instructing Cursor to call the wrapper and run `Tasks: Run Task` when automation is needed.
- **Claude Code terminal cannot find `.venv`:** its shell launches outside the repo; run `cd /path/to/workspace` first or define a startup command under Settings → Developer → Shell Init.
- **VS Code tasks pick the wrong shell:** set `"terminal.integrated.shellIntegration.enabled": true` and explicitly choose the `PowerShell (Genesis)` profile in `settings.json`.

---

## 8. Next Steps

1. Check `.vscode/tasks.json` and `scripts/genesis.ps1` into version control so the automation is discoverable.
2. Add CI that runs `scripts/genesis.ps1 doctor` on every push, ensuring that any editor-specific regression is caught quickly.
3. Document environment variables in `docs/genesis-env-reference.md` so new machines can be provisioned without digging through shell history.

Following this guide keeps Cursor, Claude Code, and VS Code executing the same Genesis CLI flows, regardless of whether you are on a modern 64-bit workstation or a constrained 32-bit fallback box.
