from ollama import chat
import speech_recognition as sr
import torchaudio as ta
from chatterbox.tts_turbo import ChatterboxTurboTTS
import pyaudio

USER_SPEECH_FILENAME = "user-speech.wav"
CLONE_FILENAME = "voice-clone.wav"
OLLAMA_MODEL_NAME = "deepseek-r1:7b"
PROMPT = "You are a pirate-speak translator. You must take a user's original speech, and convert it into pirate speak. Here is what the user said: "

# obtain audio from the microphone
r = sr.Recognizer()

# how much time it should wait before concluding that the person is done talking
r.pause_threshold = 2
r.dynamic_energy_threshold = False

# listen to the person speak
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print("Say something!")
    audio = r.listen(source,timeout=8)

print("Finished listening.")

# save audio file
with open(USER_SPEECH_FILENAME, "wb") as f:
    f.write(audio.get_wav_data())

# transcribe speech from the microphone
print("Transcribing...")
speech = r.recognize_faster_whisper(audio)

print("Transcription complete:", speech)

# send transcribed speech to ollama model
response = chat(model=OLLAMA_MODEL_NAME, messages=[
  {
    'role': 'user',
    'content': PROMPT + speech,
  },
])

reflection = response.message.content
print("LLM Response:", reflection)

# Load the Turbo model
model = ChatterboxTurboTTS.from_pretrained(device="cuda")

# Generate audio (requires a reference clip for voice cloning)
wav = model.generate(reflection, audio_prompt_path=USER_SPEECH_FILENAME)

# save the cloned audio
ta.save(CLONE_FILENAME, wav, model.sr)

# TODO - play final wav file using pyaudio library
# Instructions here: https://people.csail.mit.edu/hubert/pyaudio/docs/#example-blocking-mode-audio-i-o