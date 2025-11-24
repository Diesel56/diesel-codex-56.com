#!/usr/bin/env python3
"""
Genesis CLI Cross-Editor Synchronization Script
Ensures Cursor, VS Code, and Claude Code stay in sync across platforms
"""

import os
import sys
import json
import shutil
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import time
import hashlib

class EditorSync:
    """Synchronizes settings across VS Code, Cursor, and Claude Code"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.platform = platform.system()
        self.arch = platform.machine()
        
        # Detect architecture type
        if self.arch in ['AMD64', 'x86_64']:
            self.arch_type = 'x64'
        elif self.arch in ['x86', 'i386', 'i686']:
            self.arch_type = 'x86'
        elif self.arch in ['aarch64', 'arm64']:
            self.arch_type = 'arm64'
        else:
            self.arch_type = 'unknown'
            
        print(f"🖥️  Platform: {self.platform} ({self.arch_type})")
        
        # Define editor paths
        self.editors = {
            'vscode': self.workspace_root / '.vscode',
            'cursor': self.workspace_root / '.cursor',
            'genesis': self.workspace_root / '.genesis'
        }
        
        # User config paths (platform-specific)
        if self.platform == 'Windows':
            appdata = Path(os.environ.get('APPDATA', ''))
            self.user_configs = {
                'vscode': appdata / 'Code' / 'User',
                'cursor': appdata / 'Cursor' / 'User',
            }
        else:  # Linux/Mac
            config = Path.home() / '.config'
            self.user_configs = {
                'vscode': config / 'Code' / 'User',
                'cursor': config / 'Cursor' / 'User',
            }
    
    def ensure_directories(self):
        """Create editor config directories if they don't exist"""
        for name, path in self.editors.items():
            path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Ensured {name} directory: {path}")
    
    def hash_file(self, file_path: Path) -> str:
        """Calculate MD5 hash of a file"""
        if not file_path.exists():
            return ""
        
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()
    
    def sync_file(self, source: Path, targets: List[Path], file_name: str):
        """Sync a file from source to multiple targets"""
        source_file = source / file_name
        
        if not source_file.exists():
            print(f"⚠️  Source file not found: {source_file}")
            return
        
        source_hash = self.hash_file(source_file)
        
        for target_dir in targets:
            target_file = target_dir / file_name
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Check if target needs updating
            if target_file.exists():
                target_hash = self.hash_file(target_file)
                if source_hash == target_hash:
                    print(f"  ↔ {file_name} already in sync with {target_dir.name}")
                    continue
            
            # Copy file
            try:
                shutil.copy2(source_file, target_file)
                print(f"  ✓ Synced {file_name} → {target_dir.name}/")
            except Exception as e:
                print(f"  ✗ Failed to sync {file_name} to {target_dir.name}: {e}")
    
    def sync_workspace_settings(self):
        """Sync workspace settings between editors"""
        print("\n📋 Syncing workspace settings...")
        
        # Sync VS Code settings to Cursor
        vscode_dir = self.editors['vscode']
        cursor_dir = self.editors['cursor']
        
        files_to_sync = [
            'settings.json',
            'extensions.json',
            'tasks.json',
            'launch.json'
        ]
        
        for file_name in files_to_sync:
            # Bidirectional sync - use most recent
            vscode_file = vscode_dir / file_name
            cursor_file = cursor_dir / file_name
            
            vscode_exists = vscode_file.exists()
            cursor_exists = cursor_file.exists()
            
            if vscode_exists and cursor_exists:
                vscode_time = vscode_file.stat().st_mtime
                cursor_time = cursor_file.stat().st_mtime
                
                if vscode_time > cursor_time:
                    self.sync_file(vscode_dir, [cursor_dir], file_name)
                elif cursor_time > vscode_time:
                    self.sync_file(cursor_dir, [vscode_dir], file_name)
                else:
                    print(f"  ↔ {file_name} in sync")
            elif vscode_exists:
                self.sync_file(vscode_dir, [cursor_dir], file_name)
            elif cursor_exists:
                self.sync_file(cursor_dir, [vscode_dir], file_name)
    
    def merge_settings(self, base_settings: dict, overlay_settings: dict) -> dict:
        """Merge two settings dictionaries intelligently"""
        result = base_settings.copy()
        
        for key, value in overlay_settings.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge_settings(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def sync_user_settings(self):
        """Sync user-level settings (if accessible)"""
        print("\n👤 Checking user settings...")
        
        for editor, config_path in self.user_configs.items():
            if config_path.exists():
                print(f"  ✓ {editor.capitalize()} user config found: {config_path}")
            else:
                print(f"  ⚠️  {editor.capitalize()} user config not found: {config_path}")
    
    def validate_architecture_config(self):
        """Validate architecture-specific configurations"""
        print(f"\n🔧 Validating architecture configuration ({self.arch_type})...")
        
        genesis_config = self.editors['genesis'] / 'config.yaml'
        
        if genesis_config.exists():
            print(f"  ✓ Genesis config found")
            # Could parse YAML here to validate arch-specific paths
        else:
            print(f"  ✗ Genesis config missing")
    
    def create_sync_manifest(self):
        """Create a manifest of synchronized files"""
        manifest = {
            'timestamp': time.time(),
            'platform': self.platform,
            'architecture': self.arch_type,
            'workspace': str(self.workspace_root),
            'files': {}
        }
        
        for editor_name, editor_path in self.editors.items():
            manifest['files'][editor_name] = []
            
            if editor_path.exists():
                for file_path in editor_path.glob('*.json'):
                    manifest['files'][editor_name].append({
                        'name': file_path.name,
                        'hash': self.hash_file(file_path),
                        'size': file_path.stat().st_size
                    })
        
        manifest_path = self.editors['genesis'] / 'sync-manifest.json'
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"\n📝 Created sync manifest: {manifest_path}")
    
    def run_sync(self):
        """Execute full synchronization"""
        print("=" * 60)
        print("🔄 Genesis CLI - Cross-Editor Synchronization")
        print("=" * 60)
        
        self.ensure_directories()
        self.sync_workspace_settings()
        self.sync_user_settings()
        self.validate_architecture_config()
        self.create_sync_manifest()
        
        print("\n" + "=" * 60)
        print("✅ Synchronization complete!")
        print("=" * 60)

def main():
    """Main entry point"""
    # Determine workspace root
    if len(sys.argv) > 1:
        workspace = sys.argv[1]
    else:
        workspace = os.getcwd()
    
    # Run synchronization
    syncer = EditorSync(workspace)
    syncer.run_sync()

if __name__ == '__main__':
    main()
