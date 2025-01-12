import sys
import os
import uuid
import base64
import numpy as np
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
client = TestClient(app)
from FIDO_fastapi.app import app
from fastapi.testclient import TestClient




def test_read_app():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def generate_random_audio_inp(audio_files_number, total_data_points, audio_duration, encoded_audio=None, file_name=None):
    audio_files = []
    low = -32768
    high = 32767
    content_list = []
    for i in range(0, audio_files_number):

        raw_audio = np.random.randint(
            low, high, total_data_points, dtype="int16")
        byte_audio = raw_audio.tobytes()
        if (encoded_audio == None):
            encoded_audio_inp = base64.b64encode(byte_audio).decode("utf-8")
        else:
            encoded_audio_inp = encoded_audio[i]
        if (file_name == None):
            file_name_inp = str(uuid.uuid4()) + ".mp3"
        else:
            file_name_inp = file_name[i]

        audio_files.append({"file_name": file_name_inp,
                            "encoded_audio": encoded_audio_inp})

        content = {"status": "success",
                   "file_name": file_name_inp,
                   "length_seconds": float(audio_duration)}
        content_list.append(content)

    return [audio_files, content_list]


def test_process_audio():

    audio_files_number = 2
    audio_duration = 5
    sample_rate = 4000
    total_data_points = sample_rate*audio_duration
    result = generate_random_audio_inp(
        audio_files_number, total_data_points, audio_duration)
    audio_files_inp = result[0]
    content_list = result[1]

    test_audio_payload = {"session_id": str(uuid.uuid4()),
                          "timestamp": str(datetime.now()),
                          "audio_files": audio_files_inp
                          }

    response = client.post("/process-audio", json=test_audio_payload)
    assert response.status_code == 201
    assert response.json() == content_list


# SessionId type error
# Datetime type error
# encoded_audio type error
# file_name type error
def test_process_audio_type_error():
    audio_files_number = 2
    audio_duration = 5
    sample_rate = 4000
    total_data_points = sample_rate*audio_duration
    result = generate_random_audio_inp(
        audio_files_number, total_data_points, audio_duration)
    audio_files_inp = result[0]

    test_audio_payload = {"session_id": int(uuid.uuid4()),
                          "timestamp": str(datetime.now()),
                          "audio_files": audio_files_inp
                          }

    response = client.post("/process-audio", json=test_audio_payload)
    assert response.status_code == 422

    test_audio_payload2 = {"session_id": str(uuid.uuid4()),
                           "timestamp": str("12-12-23"),
                           "audio_files": audio_files_inp
                           }
    response2 = client.post("/process-audio", json=test_audio_payload2)

    assert response2.status_code == 422

    encoded_audio = ["101010100101010101001010010010101001010", "MDAwMDAwMTAwMDEwMTAwMDEwMDEwMTAwMDEwMDAwMDAwMDEwMTAwMTAwMTAxMDAxMDAwMDEwMTAwMTAwMDEwMDAxMDAxMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDEwMTEwMTAxMTAwMDAwMDAwMDAwMDEwMTAxMDExMTEwMDAwMDAwMDAwMDAwMDAwMTAxMTExMTExMTAwMDAwMDAwMDAwMDAwMDAwMTAxMTEwMTAxMDExMTExMTExMTEwMTAwMTEwMTAwMTAxMDEwMTAxMDEwMDAxMDAxMDEwMTEwMDAxMTEwMDE="]
    result2 = generate_random_audio_inp(
        audio_files_number, total_data_points, audio_duration, encoded_audio, ["RANDOM_NAME", "RANDOM_NAME2"])
    test_audio_payload3 = {"session_id": str(uuid.uuid4()),
                           "timestamp": str(datetime.now()),
                           "audio_files": result2[0]
                           }
    response3 = client.post("/process-audio", json=test_audio_payload3)
    assert response3.status_code == 422

    result3 = generate_random_audio_inp(
        audio_files_number, total_data_points, audio_duration, file_name=[1234, 1228227])
    test_audio_payload4 = {"session_id": str(uuid.uuid4()),
                           "timestamp": str(datetime.now()),
                           "audio_files": result3[0]
                           }
    response4 = client.post("/process-audio", json=test_audio_payload4)
    assert response4.status_code == 422


def test_bulk_audio_process():
    audio_files_number = 1000
    audio_duration = 100
    sample_rate = 4000
    total_data_points = sample_rate*audio_duration
    result = generate_random_audio_inp(
        audio_files_number, total_data_points, audio_duration)
    audio_files_inp = result[0]
    content_list = result[1]

    test_audio_payload = {"session_id": str(uuid.uuid4()),
                          "timestamp": str(datetime.now()),
                          "audio_files": audio_files_inp
                          }

    response = client.post("/process-audio", json=test_audio_payload)
    assert response.status_code == 201
    assert response.json() == content_list
