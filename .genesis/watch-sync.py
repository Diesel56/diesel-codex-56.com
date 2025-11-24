#!/usr/bin/env python3
"""
Genesis CLI - Continuous File Watcher and Sync
Watches for changes and automatically syncs between editors
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Set
import hashlib

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("⚠️  watchdog not installed. Install with: pip install watchdog")
    print("   Falling back to polling mode...")

class EditorSyncHandler(FileSystemEventHandler):
    """Handle file system events for editor config files"""
    
    def __init__(self, workspace_root: Path, debounce_seconds: float = 0.5):
        self.workspace_root = workspace_root
        self.debounce_seconds = debounce_seconds
        self.last_sync_times = {}
        self.sync_extensions = {'.json', '.yaml', '.yml'}
        
        self.vscode_dir = workspace_root / '.vscode'
        self.cursor_dir = workspace_root / '.cursor'
        self.genesis_dir = workspace_root / '.genesis'
    
    def should_sync(self, file_path: Path) -> bool:
        """Determine if a file should be synced"""
        # Check extension
        if file_path.suffix not in self.sync_extensions:
            return False
        
        # Check if it's in a config directory
        try:
            if self.vscode_dir in file_path.parents or \
               self.cursor_dir in file_path.parents:
                return True
        except ValueError:
            pass
        
        return False
    
    def debounce(self, key: str) -> bool:
        """Check if enough time has passed since last sync"""
        now = time.time()
        last_sync = self.last_sync_times.get(key, 0)
        
        if now - last_sync >= self.debounce_seconds:
            self.last_sync_times[key] = now
            return True
        return False
    
    def sync_file(self, source_path: Path):
        """Sync a modified file to the corresponding editor"""
        try:
            # Determine source editor
            if self.vscode_dir in source_path.parents:
                source_editor = 'vscode'
                target_dir = self.cursor_dir
            elif self.cursor_dir in source_path.parents:
                source_editor = 'cursor'
                target_dir = self.vscode_dir
            else:
                return
            
            # Get relative path and target path
            if source_editor == 'vscode':
                rel_path = source_path.relative_to(self.vscode_dir)
            else:
                rel_path = source_path.relative_to(self.cursor_dir)
            
            target_path = target_dir / rel_path
            
            # Create target directory if needed
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Read source content
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if target needs updating
            if target_path.exists():
                with open(target_path, 'r', encoding='utf-8') as f:
                    target_content = f.read()
                
                if content == target_content:
                    return  # Already in sync
            
            # Write to target
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"🔄 Synced: {source_editor}/{rel_path} → {target_dir.name}/")
            
        except Exception as e:
            print(f"✗ Sync error for {source_path}: {e}")
    
    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        if self.should_sync(file_path) and self.debounce(str(file_path)):
            self.sync_file(file_path)
    
    def on_created(self, event):
        """Handle file creation events"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        if self.should_sync(file_path) and self.debounce(str(file_path)):
            self.sync_file(file_path)

class PollingSync:
    """Fallback polling-based sync when watchdog is not available"""
    
    def __init__(self, workspace_root: Path, interval: int = 5):
        self.workspace_root = workspace_root
        self.interval = interval
        self.file_hashes = {}
        
        self.vscode_dir = workspace_root / '.vscode'
        self.cursor_dir = workspace_root / '.cursor'
    
    def hash_file(self, file_path: Path) -> str:
        """Calculate file hash"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return ""
    
    def scan_and_sync(self):
        """Scan for changes and sync"""
        changed_files = []
        
        for config_dir in [self.vscode_dir, self.cursor_dir]:
            if not config_dir.exists():
                continue
            
            for file_path in config_dir.glob('*.json'):
                current_hash = self.hash_file(file_path)
                key = str(file_path)
                
                if key in self.file_hashes:
                    if self.file_hashes[key] != current_hash:
                        changed_files.append(file_path)
                
                self.file_hashes[key] = current_hash
        
        # Sync changed files
        for file_path in changed_files:
            print(f"🔄 Detected change: {file_path.name}")
            # Simple bidirectional copy
            if self.vscode_dir in file_path.parents:
                target = self.cursor_dir / file_path.name
            else:
                target = self.vscode_dir / file_path.name
            
            try:
                import shutil
                shutil.copy2(file_path, target)
                print(f"  ✓ Synced to {target.parent.name}/")
            except Exception as e:
                print(f"  ✗ Sync failed: {e}")
    
    def run(self):
        """Run polling loop"""
        print(f"📊 Starting polling sync (interval: {self.interval}s)")
        print("   Press Ctrl+C to stop")
        
        try:
            while True:
                self.scan_and_sync()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\n⏹️  Stopped")

def main():
    """Main entry point"""
    workspace = Path(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
    
    print("=" * 60)
    print("👁️  Genesis CLI - Watch & Sync")
    print("=" * 60)
    print(f"Workspace: {workspace}")
    print()
    
    if WATCHDOG_AVAILABLE:
        # Use watchdog for real-time monitoring
        event_handler = EditorSyncHandler(workspace)
        observer = Observer()
        
        # Watch both directories
        vscode_dir = workspace / '.vscode'
        cursor_dir = workspace / '.cursor'
        
        if vscode_dir.exists():
            observer.schedule(event_handler, str(vscode_dir), recursive=False)
            print(f"👀 Watching: {vscode_dir}")
        
        if cursor_dir.exists():
            observer.schedule(event_handler, str(cursor_dir), recursive=False)
            print(f"👀 Watching: {cursor_dir}")
        
        print("\n✓ Live sync enabled. Press Ctrl+C to stop.")
        print()
        
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print("\n⏹️  Stopped watching")
        observer.join()
    else:
        # Fallback to polling
        poller = PollingSync(workspace, interval=5)
        poller.run()

if __name__ == '__main__':
    main()
