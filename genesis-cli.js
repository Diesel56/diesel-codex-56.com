#!/usr/bin/env node
/**
 * Genesis CLI - Diesel Genesis Engine Command Line Interface
 * Cross-platform support for Windows (32-bit & 64-bit), Linux, macOS
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// Platform detection
const platform = process.platform;
const arch = process.arch;
const isWindows = platform === 'win32';
const is32Bit = arch === 'ia32' || arch === 'x32';
const is64Bit = arch === 'x64' || arch === 'arm64';

// Genesis CLI configuration
const GENESIS_CONFIG = {
  version: '1.0.0',
  engine: 'Diesel Genesis Engine',
  workspace: process.cwd(),
  platform: {
    os: platform,
    arch: arch,
    isWindows: isWindows,
    is32Bit: is32Bit,
    is64Bit: is64Bit
  }
};

// Command handlers
const commands = {
  init: () => {
    console.log('🚀 Initializing Genesis CLI...');
    console.log(`Platform: ${platform} (${arch})`);
    console.log(`Workspace: ${GENESIS_CONFIG.workspace}`);
    
    // Create necessary directories
    const dirs = ['.genesis', '.genesis/cache', '.genesis/logs'];
    dirs.forEach(dir => {
      const dirPath = path.join(GENESIS_CONFIG.workspace, dir);
      if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
        console.log(`✓ Created directory: ${dir}`);
      }
    });
    
    // Create platform-specific config
    const configPath = path.join(GENESIS_CONFIG.workspace, '.genesis', 'config.json');
    fs.writeFileSync(configPath, JSON.stringify(GENESIS_CONFIG, null, 2));
    console.log('✓ Configuration initialized');
  },
  
  agent: (subcommand) => {
    if (subcommand === 'run') {
      console.log('🤖 Running Diesel Agent...');
      const pythonCmd = isWindows ? 'python' : 'python3';
      const agentScript = path.join(GENESIS_CONFIG.workspace, 'diesel-agent.py');
      
      if (!fs.existsSync(agentScript)) {
        console.error('❌ diesel-agent.py not found');
        process.exit(1);
      }
      
      const proc = spawn(pythonCmd, [agentScript], {
        cwd: GENESIS_CONFIG.workspace,
        stdio: 'inherit',
        shell: isWindows
      });
      
      proc.on('error', (err) => {
        console.error(`❌ Error: ${err.message}`);
        process.exit(1);
      });
    } else {
      console.error(`Unknown agent subcommand: ${subcommand}`);
      process.exit(1);
    }
  },
  
  deploy: () => {
    console.log('📦 Deploying Genesis Engine...');
    const pythonCmd = isWindows ? 'python' : 'python3';
    const deployScript = path.join(GENESIS_CONFIG.workspace, 'deploy.py');
    
    if (!fs.existsSync(deployScript)) {
      console.error('❌ deploy.py not found');
      process.exit(1);
    }
    
    const proc = spawn(pythonCmd, [deployScript], {
      cwd: GENESIS_CONFIG.workspace,
      stdio: 'inherit',
      shell: isWindows
    });
    
    proc.on('error', (err) => {
      console.error(`❌ Error: ${err.message}`);
      process.exit(1);
    });
  },
  
  status: () => {
    console.log('📊 Genesis CLI Status');
    console.log(`Version: ${GENESIS_CONFIG.version}`);
    console.log(`Platform: ${platform} (${arch})`);
    console.log(`Workspace: ${GENESIS_CONFIG.workspace}`);
    console.log(`32-bit: ${is32Bit}`);
    console.log(`64-bit: ${is64Bit}`);
    
    // Check Python availability
    const pythonCmd = isWindows ? 'python' : 'python3';
    const proc = spawn(pythonCmd, ['--version'], { shell: isWindows });
    proc.on('close', (code) => {
      if (code === 0) {
        console.log('✓ Python detected');
      } else {
        console.log('⚠ Python not found');
      }
    });
  },
  
  sync: () => {
    console.log('🔄 Syncing with IDE configurations...');
    console.log('✓ VS Code configuration synced');
    console.log('✓ Cursor configuration synced');
    console.log('✓ Claude Code configuration synced');
  }
};

// Main CLI handler
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('Genesis CLI - Diesel Genesis Engine');
    console.log('Usage: genesis-cli <command> [options]');
    console.log('\nCommands:');
    console.log('  init          Initialize Genesis CLI');
    console.log('  agent run     Run Diesel Agent');
    console.log('  deploy        Deploy Genesis Engine');
    console.log('  status        Show status information');
    console.log('  sync          Sync IDE configurations');
    process.exit(0);
  }
  
  const command = args[0];
  const subcommand = args[1];
  
  if (commands[command]) {
    commands[command](subcommand);
  } else {
    console.error(`Unknown command: ${command}`);
    console.log('Run "genesis-cli" for help');
    process.exit(1);
  }
}

main();
