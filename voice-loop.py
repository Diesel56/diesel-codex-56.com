
import speech_recognition as sr
import os
import subprocess

WAKE_PHRASE = "diesel"

COMMAND_MAP = {
    "run agent": "python3 diesel-agent.py",
    "create codex": "python3 whisper-cli.py",
    "read manifest": "python3 vault_viewer.py",
    "fetch child crisis": "python3 get_codex.py --pattern \"child crisis\"",
}

def match_command(spoken_text):
    for phrase, command in COMMAND_MAP.items():
        if phrase in spoken_text:
            return command
    return None

def listen_and_execute():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("🎤 Voice Commando Activated. Speak clearly after the wake word: 'Diesel'.")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

        while True:
            print("👂 Listening...")
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio).lower()
                print(f"🗣 You said: {text}")

                if WAKE_PHRASE in text:
                    command = match_command(text)
                    if command:
                        print(f"⚙️ Executing: {command}")
                        subprocess.run(command, shell=True)
                    else:
                        print("⚠️ Command not recognized after wake phrase.")
                else:
                    print("💤 Wake phrase not detected.")
            except sr.UnknownValueError:
                print("🤷 Could not understand audio.")
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    listen_and_execute()
