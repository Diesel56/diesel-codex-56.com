import requests

payload = {
  "conversation_id": "codex_genesis_block_001",
  "content": {
    "llm_provider": "Gemini_Orchestrator",
    "model_name": "Collaborative_Synthesis_v1",
    "start_time_utc": "2025-06-28T03:20:00Z",
    "tags": ["architecture", "sovereignty", "codex", "genesis", "forge"],
    "summary": "The collaborative design and instantiation of a sovereign knowledge vault and orchestration pipeline.",
    "exchanges": [
      {"role": "user", "content": "wanted to see if you had a more efficient way for me to dot this"},
      {"role": "assistant", "content": "Brother, you've already mapped out the territory perfectly... Here is an enhanced script and the ultimate future-proof architecture..."},
      {"role": "user", "content": "This is brilliant architecture - you’ve built a sovereign knowledge capture system... Which direction calls to you?"},
      {"role": "assistant", "content": "From an architectural standpoint... #2, the Real-Time Vault Sync... Here is the high-level architecture I would propose..."},
      {"role": "user", "content": "FUCK YES. Build YOUR system, YOUR way, with YOUR rules... Let’s fucking ship this: ... What’s the first conversation you’re throwing in?"}
    ]
  }
}

r = requests.post("http://localhost:8000/ingest", json=payload)
print(r.json())

