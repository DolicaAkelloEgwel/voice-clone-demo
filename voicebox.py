import uuid

import requests
import urllib3

VOICEBOX_API_URL = "http://127.0.0.1:17493"
PROFILES = "/profiles/"


class VoiceBox:
    def __init__(self):
        self._id = ""
        self._name = str(uuid.uuid4()).replace("-", "")[:6]

    def _success(self, response):
        return response.status_code == 200

    def create_profile(self):
        data = {"name": self._name}
        response = requests.post(VOICEBOX_API_URL + PROFILES, json=data)

        if self._success(response):
            self._id = response.json()["id"]
        else:
            # this means creating a profile failed
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
        if not self._success(response):
            pass
        return response

    def delete_profile(self):
        response = requests.delete(VOICEBOX_API_URL + PROFILES + self._id)
        return response
