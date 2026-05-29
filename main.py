import os
import uuid

import playsound3 as playsound
import requests
import speech_recognition as sr
from ollama import chat

from voicebox import VoiceBox

USER_SPEECH_FILENAME = "user-speech.wav"
CLONE_FILENAME = "voice-clone.wav"
PROJECT_DIR = os.path.abspath(__file__)
GLOBAL_INPUT_AUDIO_PATH = os.path.join(PROJECT_DIR, USER_SPEECH_FILENAME)
print(GLOBAL_INPUT_AUDIO_PATH)

test = True

# language model - must be something that has been installed with Ollama
OLLAMA_MODEL_NAME = "deepseek-r1:7b"

# Prompt for the LLM
PROMPT = "You are a pirate-speak translator. You must take a user's original speech, and convert it into pirate speak. Here is what the user said: "

# obtain audio from the microphone
r = sr.Recognizer()

# how much time it should wait before concluding that the person is done talking
r.pause_threshold = 2

# suggested by a stackoverflow commenter to help combat when the recording stops and starts at unusual times
r.dynamic_energy_threshold = False

# this is a value that I think needs to be played around with depending on your laptop's microphone
# r.energy_threshold = 400

vb = VoiceBox()
vb.create_profile()

# listen to the person speak

if not test:
    with sr.Microphone() as source:
        # tell the SpeechRecognition library to adjust for background noise
        r.adjust_for_ambient_noise(source)

        print("Say something!")
        audio = r.listen(source, timeout=8)

    print("Finished listening.")

    # save microphone audio file
    with open(USER_SPEECH_FILENAME, "wb") as f:
        f.write(audio.get_wav_data())
else:
    USER_SPEECH_FILENAME = "test-audio.wav"

res = vb.add_voice_sample(
    open(USER_SPEECH_FILENAME, "rb").read(),
    USER_SPEECH_FILENAME,
    "the subject speaking about a personal dilemma",
)


exit()

# transcribe speech from the recording
print("Transcribing...")
speech = r.recognize_faster_whisper(audio)
print("Transcription complete:", speech)

# send transcribed speech to the ollama model
response = chat(
    model=OLLAMA_MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": PROMPT + speech,
        },
    ],
)

# store the reply in a variable
reflection = response.message.content
print("LLM Response:", reflection)

# # Load the voice-cloning model
# model = ChatterboxTurboTTS.from_pretrained(device="cuda")

# # Generate audio in the style of the speech
# wav = model.generate(reflection, audio_prompt_path=USER_SPEECH_FILENAME)

# # save the cloned audio
# ta.save(CLONE_FILENAME, wav, model.sr)

# # play the cloned voice file
# playsound.playsound(CLONE_FILENAME, block=True)
