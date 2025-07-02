import os
import json

def scan_vault_and_tag():
    path = os.path.expanduser("~/jimmy.recourse/vault/context")
    manifest_path = os.path.expanduser("~/jimmy.recourse/vault/manifest.json")

    tagged_files = {}

    for file in os.listdir(path):
        if file.endswith(".yaml") or file.endswith(".md") or file.endswith(".txt"):
            full_path = os.path.join(path, file)
            with open(full_path, "r") as f:
                content = f.read()

            tag = "Codex Pattern Detected" if "Codex" in content else "Unclassified"
            tagged_files[file] = {"path": full_path, "tag": tag}

    with open(manifest_path, "w") as mf:
        json.dump(tagged_files, mf, indent=2)

    print(f"🧠 Manifest updated with {len(tagged_files)} files")

if __name__ == "__main__":
    scan_vault_and_tag()

