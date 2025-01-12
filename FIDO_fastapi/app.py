from fastapi import FastAPI
from pydantic import ValidationError
from FIDO_fastapi.models.FIDO_models import AudioPayload, AudioMetadata
from FIDO_fastapi.functions.database_operations import DatabaseOperations
import sqlite3
from fastapi.responses import JSONResponse
import base64
from FIDO_fastapi.environment import Environment
import numpy as np
app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


@app.get("/test_db")
async def test_db():
    database_conn_instance = DatabaseOperations()
    database_conn_instance.close_instance()


@app.post("/process-audio")
async def process_audio(audio_payload: AudioPayload):

    try:
        env = Environment()
        database_conn_instance = DatabaseOperations()
        content_list = []

        for file in audio_payload.audio_files:
            decoded = base64.b64decode(file['encoded_audio'])
            raw_audio = np.frombuffer(decoded, dtype="int16")
            file_name = file['file_name']
            audio_file_length = len(raw_audio)/env.sample_rate

            audio_metadata = AudioMetadata(
                session_id=audio_payload.session_id,
                timestamp=str(audio_payload.timestamp),
                file_name=file_name,
                audio_length=audio_file_length
            )

            database_conn_instance.insert_audio_metadata(audio_metadata)

            content = {"status": "success",
                       "file_name": file_name,
                       "length_seconds": audio_file_length}
            content_list.append(content)

        return JSONResponse(status_code=201, content=content_list)

    except sqlite3.DatabaseError as ex:

        return JSONResponse(status_code=500,
                            content={
                                "status": "error",
                                "message": f"Database Insert Error: {ex}",
                            })
    except ValidationError as ex:
        return JSONResponse(status_code=400,
                            content={
                                "status": "error",
                                "message": f"Input Data Error: {ex}",
                            })
    except Exception as ex:
        return JSONResponse(status_code=500,
                            content={
                                "status": "error",
                                "message": f"Unexpected Error: {ex}",
                            })
    finally:
        database_conn_instance.close_instance()
