# Diesel Codex Vault

This is the GitOps-connected Diesel Vault system for local Codex pattern management.

## Included Scripts
- `diesel-agent.py`: Scans the vault for files and updates the manifest
- `whisper-cli.py`: Simulates voice transcription to YAML
- `get_codex.py`: Fetches a known Codex pattern into your vault
- `vault_viewer.py`: CLI-based manifest reader

## Setup
1. Install Python requirements:
```bash
pip install -r requirements.txt
```

2. Run any tool, for example:
```bash
python3 diesel-agent.py
python3 whisper-cli.py
python3 get_codex.py --pattern "child crisis"
python3 vault_viewer.py
```

3. Store all your Codex YAMLs, notes, transcripts in `vault/context/`.

## Codex Sovereignty
This repo is your private vault. It can be extended with real Whisper integration, voice daemon triggers, or AI pattern mirrors.

All Codex data lives locally unless you choose to share it.
