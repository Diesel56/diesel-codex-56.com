#!/usr/bin/env node
/**
 * Symbiotic Dynamic Sync - Synchronizes configurations across IDEs
 * Ensures VS Code, Cursor, and Claude Code stay in sync
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE_ROOT = process.cwd();
const CONFIG_DIRS = [
  '.vscode',
  '.cursor',
  '.claude-code'
];

// Shared settings that should be synchronized
const SHARED_SETTINGS = [
  'python.defaultInterpreterPath',
  'python.analysis.typeCheckingMode',
  'python.formatting.provider',
  'editor.tabSize',
  'editor.insertSpaces',
  'files.associations',
  'yaml.schemas',
  'terminal.integrated.defaultProfile.windows',
  'terminal.integrated.profiles.windows'
];

function stripJsonComments(content) {
  // Remove single-line comments (// ...)
  content = content.replace(/\/\/.*$/gm, '');
  // Remove multi-line comments (/* ... */)
  content = content.replace(/\/\*[\s\S]*?\*\//g, '');
  return content;
}

function loadConfig(configPath) {
  try {
    if (fs.existsSync(configPath)) {
      let content = fs.readFileSync(configPath, 'utf8');
      // Strip comments for JSON parsing (VS Code settings.json supports comments)
      content = stripJsonComments(content);
      return JSON.parse(content);
    }
    return {};
  } catch (error) {
    console.error(`Error loading ${configPath}:`, error.message);
    return {};
  }
}

function saveConfig(configPath, config) {
  try {
    const dir = path.dirname(configPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n');
    return true;
  } catch (error) {
    console.error(`Error saving ${configPath}:`, error.message);
    return false;
  }
}

function syncConfigurations() {
  console.log('🔄 Syncing IDE configurations...');
  
  const configs = {};
  
  // Load all configurations
  CONFIG_DIRS.forEach(dir => {
    const configPath = path.join(WORKSPACE_ROOT, dir, 'settings.json');
    configs[dir] = loadConfig(configPath);
  });
  
  // Find the most complete configuration (VS Code as source of truth)
  const sourceConfig = configs['.vscode'] || {};
  
  // Sync shared settings to all configurations
  CONFIG_DIRS.forEach(dir => {
    if (!configs[dir]) {
      configs[dir] = {};
    }
    
    // Copy shared settings from source
    SHARED_SETTINGS.forEach(setting => {
      if (sourceConfig[setting] !== undefined) {
        configs[dir][setting] = sourceConfig[setting];
      }
    });
    
    // Add IDE-specific settings
    if (dir === '.cursor') {
      configs[dir]['cursor.genesis.cli.enabled'] = true;
      configs[dir]['cursor.genesis.cli.symbioticMode'] = true;
    } else if (dir === '.claude-code') {
      configs[dir]['claude.genesis.cli.enabled'] = true;
      configs[dir]['claude.genesis.cli.symbioticMode'] = true;
    }
    
    // Save configuration
    const configPath = path.join(WORKSPACE_ROOT, dir, 'settings.json');
    if (saveConfig(configPath, configs[dir])) {
      console.log(`✓ Synced ${dir}/settings.json`);
    }
  });
  
  console.log('✅ Configuration sync complete');
}

// Run sync
syncConfigurations();
