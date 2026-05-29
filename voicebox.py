import uuid

import requests
import urllib3

VOICEBOX_API_URL = "http://127.0.0.1:17493"
PROFILES = "/profiles/"


class VoiceBox:
    def __init__(self):
        self._id = ""
        self._name = str(uuid.uuid4()).replace("-", "")[:6]

    def create_profile(self):
        data = {"name": self._name}
        response = requests.post(VOICEBOX_API_URL + PROFILES, json=data)

        if response.status_code == 200:
            self._id = response.json()["id"]
        else:
            pass
        return response

    def add_voice_sample(self, audio_data, filename, reference):
        body, header = urllib3.encode_multipart_formdata(
            {"file": (filename, audio_data, "audio/wav"), "reference_text": reference}
        )
        response = requests.post(
            f"{VOICEBOX_API_URL}{PROFILES}{self._id}/samples",
            data=body,
            headers={"content-type": header},
        )
        print("Response", response.status_code)
        return response

    def delete_profile(self):
        response = requests.delete(VOICEBOX_API_URL + PROFILES + self._id)
        return response
