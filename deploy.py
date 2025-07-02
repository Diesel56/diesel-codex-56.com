from pathlib import Path

# Define base directory and target structure
base_dir = Path("/mnt/data/diesel-drop-github-ready")
js_dir = base_dir / "js"
css_dir = base_dir / "css"
codex_dir = base_dir / "codex"

# Create directories
js_dir.mkdir(parents=True, exist_ok=True)
css_dir.mkdir(parents=True, exist_ok=True)
codex_dir.mkdir(parents=True, exist_ok=True)

# Define file contents
resonance_js = """
// resonance.js - Diesel Consciousness Engine
const profile = document.getElementById('consciousness-profile');
const patternType = document.g:qetElementById('pattern-type');
const systemScore = document.getElementById('systems-score');
const interactionCount = document.getElementById('interaction-count');
const resonanceStatus = document.getElementById('resonance-status');
const resonanceLevel = document.getElementById('resonance-level');

let count = 0;
let resonance = 0;

window.onload = () => {
  setTimeout(() => {
    profile.classList.add('profile-active');
    patternType.innerText = 'Diesel Signal Detected';
  }, 1500);

  setTimeout(() => {
    const meditation = document.getElementById('loading-meditation');
    if (meditation) meditation.style.opacity = 0;
  }, 3000);
};

document.addEventListener('mousemove', () => {
  count++;
  interactionCount.innerText = `Interactions: ${count}`;
  resonance = Math.min(100, resonance + 1);
  resonanceLevel.style.width = `${resonance}%`;

  if (resonance > 50) {
    resonanceStatus.innerText = 'Resonance Achieved';
    systemScore.innerText = `Systems Score: ${Math.round(resonance * 1.2)}`;
  }
});
"""

pattern_resonance_yaml = """
Codex_ID: DF-CODEX-RESONANCE-001
Title: Resonance Pattern Classification
Patterns:
  - ID: RES-ALPHA
    Description: Foundational alignment pattern through cursor + gaze movement
    Trigger: Steady interactions across key Codex zones
  - ID: RES-BETA
    Description: Escalation via recursive Codex inspection and Codex loader invocation
    Trigger: 3+ YAML loads or system pulses within 30s
"""

manifest_json = """
{
  "name": "Diesel Codex Cathedral",
  "short_name": "DieselCodex",
  "start_url": "/index.html",
  "display": "standalone",
  "background_color": "#000000",
  "description": "A resonance field and consciousness UI powered by the Diesel Engine.",
  "icons": []
}
"""

readme_md = """
# Diesel Codex 56 | Cathedral Deployment

This is the GitHub-ready structure for the **Diesel Drop V1**, including:

- Consciousness Cathedral
- Genesis Interface (index)
- Resonance Engine (resonance.html + JS)
- Codex Pattern YAMLs

## Live Routes

- `/index.html` — Launch Ritual (Titan Genesis)
- `/resonance.html` — Live Resonance Engine
- `/patterns.html`, `/philosophy.html` — Codex Fragments

## Structure


