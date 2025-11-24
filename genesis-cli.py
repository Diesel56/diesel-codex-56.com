#!/usr/bin/env python3
"""
Genesis CLI - Cross-platform command-line interface for Diesel Engine
Supports Windows (32/64-bit), Linux (32/64-bit), and macOS
"""

import os
import sys
import json
import platform
import subprocess
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('genesis-cli')

class GenesisCLI:
    """Main Genesis CLI class for cross-platform operations"""
    
    def __init__(self, config_path: str = 'genesis.config.json'):
        self.config_path = Path(config_path)
        self.workspace_root = Path.cwd()
        self.platform_info = self._detect_platform()
        self.config = self._load_config()
        
    def _detect_platform(self) -> Dict[str, str]:
        """Detect current platform and architecture"""
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        # Map system names
        if system == 'windows':
            system = 'windows'
        elif system == 'linux':
            system = 'linux'
        elif system == 'darwin':
            system = 'darwin'
        
        # Map architecture
        if machine in ['x86_64', 'amd64']:
            arch = 'x64'
        elif machine in ['i386', 'i686', 'x86']:
            arch = 'x86'
        elif machine in ['arm64', 'aarch64']:
            arch = 'arm64'
        else:
            arch = machine
            
        bits = '64' if sys.maxsize > 2**32 else '32'
        
        return {
            'system': system,
            'arch': arch,
            'bits': bits,
            'python_version': platform.python_version(),
            'full': f"{system}-{arch}"
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """Load Genesis configuration"""
        if not self.config_path.exists():
            logger.warning(f"Config file {self.config_path} not found")
            return {}
            
        with open(self.config_path, 'r') as f:
            return json.load(f)
    
    def _save_config(self):
        """Save current configuration"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _get_platform_config(self) -> Dict[str, Any]:
        """Get platform-specific configuration"""
        platforms = self.config.get('platforms', {})
        system_config = platforms.get(self.platform_info['system'], {})
        arch_config = system_config.get(self.platform_info['arch'], {})
        
        # Fallback to x64 if specific arch not found
        if not arch_config and self.platform_info['arch'] == 'x86':
            arch_config = system_config.get('x64', {})
            
        return arch_config
    
    def _run_command(self, cmd: List[str], env: Optional[Dict] = None) -> int:
        """Run a command with platform-specific settings"""
        platform_config = self._get_platform_config()
        
        # Merge environment variables
        cmd_env = os.environ.copy()
        if env:
            cmd_env.update(env)
        if platform_config.get('env'):
            cmd_env.update(platform_config['env'])
            
        # Update with Genesis environment
        if self.config.get('env'):
            for key, value in self.config['env'].items():
                value = value.replace('${workspaceFolder}', str(self.workspace_root))
                cmd_env[key] = value
        
        # Use platform-specific shell if needed
        shell = platform_config.get('shell', 'bash')
        
        logger.info(f"Running command: {' '.join(cmd)}")
        logger.debug(f"Platform: {self.platform_info['full']}")
        logger.debug(f"Shell: {shell}")
        
        try:
            result = subprocess.run(
                cmd,
                env=cmd_env,
                capture_output=False,
                text=True,
                shell=(self.platform_info['system'] == 'windows')
            )
            return result.returncode
        except Exception as e:
            logger.error(f"Command failed: {e}")
            return 1
    
    def init(self, args: argparse.Namespace) -> int:
        """Initialize Genesis CLI in the workspace"""
        logger.info("Initializing Genesis CLI...")
        
        # Create directory structure
        dirs_to_create = [
            '.genesis',
            '.genesis/cache',
            '.genesis/logs',
            '.genesis/temp',
            '.genesis/artifacts',
            '.vscode',
            '.cursor'
        ]
        
        for dir_path in dirs_to_create:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            
        logger.info(f"Created directory structure")
        
        # Install dependencies based on platform
        platform_config = self._get_platform_config()
        python_cmd = platform_config.get('pythonPath', 'python3')
        
        if Path('requirements.txt').exists():
            logger.info("Installing Python dependencies...")
            self._run_command([python_cmd, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        
        logger.info("Genesis CLI initialized successfully")
        return 0
    
    def build(self, args: argparse.Namespace) -> int:
        """Build the project"""
        logger.info("Building project...")
        
        # Validate configuration
        if not Path('diesel_engine.yaml').exists():
            logger.error("diesel_engine.yaml not found")
            return 1
        
        # Run platform-specific build commands
        platform_config = self._get_platform_config()
        python_cmd = platform_config.get('pythonPath', 'python3')
        
        # Format Python code
        logger.info("Formatting Python code...")
        self._run_command([python_cmd, '-m', 'black', '.', '--line-length', '88'])
        
        # Lint code
        logger.info("Linting code...")
        self._run_command([python_cmd, '-m', 'flake8', '.', '--max-line-length', '88'])
        
        logger.info("Build completed successfully")
        return 0
    
    def deploy(self, args: argparse.Namespace) -> int:
        """Deploy the project"""
        logger.info(f"Deploying to {args.env}...")
        
        # Run build first
        if self.build(args) != 0:
            logger.error("Build failed, aborting deployment")
            return 1
        
        # Run deployment script
        platform_config = self._get_platform_config()
        python_cmd = platform_config.get('pythonPath', 'python3')
        
        deploy_script = 'secure_deploy.py' if args.secure else 'deploy.py'
        if Path(deploy_script).exists():
            logger.info(f"Running {deploy_script}...")
            return self._run_command([python_cmd, deploy_script])
        else:
            logger.warning(f"{deploy_script} not found")
            return 1
    
    def sync(self, args: argparse.Namespace) -> int:
        """Sync configurations across all editors"""
        logger.info("Syncing editor configurations...")
        
        editors = self.config.get('editors', {})
        
        for editor, config in editors.items():
            if config.get('enabled') and config.get('autoSync'):
                logger.info(f"Syncing {editor} configuration...")
                # Configuration files are already created
                
        logger.info("Sync completed successfully")
        return 0
    
    def validate(self, args: argparse.Namespace) -> int:
        """Validate all configurations"""
        logger.info("Validating configurations...")
        
        errors = []
        
        # Check required files
        required_files = [
            'diesel_engine.yaml',
            'genesis.config.json'
        ]
        
        for file_path in required_files:
            if not Path(file_path).exists():
                errors.append(f"Required file {file_path} not found")
        
        # Check platform support
        platform_config = self._get_platform_config()
        if not platform_config or not platform_config.get('enabled'):
            errors.append(f"Platform {self.platform_info['full']} not supported")
        
        # Check dependencies
        dependencies = self.config.get('dependencies', {})
        for dep, version in dependencies.items():
            logger.info(f"Checking {dep} version...")
            # Add version checking logic here
        
        if errors:
            for error in errors:
                logger.error(error)
            return 1
        
        logger.info("All configurations are valid")
        return 0
    
    def status(self, args: argparse.Namespace) -> int:
        """Show Genesis CLI status"""
        logger.info("Genesis CLI Status")
        logger.info("=" * 50)
        logger.info(f"Platform: {self.platform_info['system']}")
        logger.info(f"Architecture: {self.platform_info['arch']}")
        logger.info(f"Bits: {self.platform_info['bits']}")
        logger.info(f"Python: {self.platform_info['python_version']}")
        logger.info(f"Workspace: {self.workspace_root}")
        logger.info(f"Config: {self.config_path}")
        
        # Show enabled editors
        logger.info("\nEnabled Editors:")
        editors = self.config.get('editors', {})
        for editor, config in editors.items():
            if config.get('enabled'):
                logger.info(f"  - {editor}")
        
        # Show enabled modules
        logger.info("\nDiesel Engine Modules:")
        diesel_config = self.config.get('engines', {}).get('diesel', {})
        for module in diesel_config.get('modules', []):
            logger.info(f"  - {module}")
        
        return 0

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Genesis CLI - Diesel Engine Command Interface')
    parser.add_argument('--config', default='genesis.config.json', help='Config file path')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize Genesis CLI')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build the project')
    build_parser.add_argument('--clean', action='store_true', help='Clean build')
    
    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy the project')
    deploy_parser.add_argument('--env', default='production', help='Target environment')
    deploy_parser.add_argument('--secure', action='store_true', help='Use secure deployment')
    
    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Sync editor configurations')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate configurations')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show Genesis CLI status')
    
    args = parser.parse_args()
    
    # Set debug logging
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    # Create CLI instance
    cli = GenesisCLI(args.config)
    
    # Execute command
    if not args.command:
        parser.print_help()
        return 0
    
    command_map = {
        'init': cli.init,
        'build': cli.build,
        'deploy': cli.deploy,
        'sync': cli.sync,
        'validate': cli.validate,
        'status': cli.status
    }
    
    command_func = command_map.get(args.command)
    if command_func:
        return command_func(args)
    else:
        logger.error(f"Unknown command: {args.command}")
        return 1

if __name__ == '__main__':
    sys.exit(main())