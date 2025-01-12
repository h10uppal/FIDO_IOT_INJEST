from typing import List, Dict
from pydantic import BaseModel, field_validator
from datetime import datetime
import base64
import binascii


class AudioMetadata(BaseModel):
    session_id: str
    timestamp: str
    file_name: str
    audio_length: float


class __AudioFiles(BaseModel):
    file_name: str
    encoded_audio: str

    @field_validator('encoded_audio', mode='plain')
    def encoded_audio_validator(cls, value: str) -> str:
        try:
            validation = base64.b64decode(value, validate=True)
            return value
        except binascii.Error:
            raise ValueError("ERROR: String is not Base64 encoded")


class AudioPayload(BaseModel):
    session_id: str
    timestamp: str
    audio_files: List[Dict[str, str]]

    @field_validator('timestamp', mode='after')
    def timestamp_format_validate(cls, value: str) -> str:
        try:
            if isinstance(value, str):
                datetime.fromisoformat(value)
                return value
            else:
                raise ValueError("ERROR: Timestamp must be of type string")
        except Exception as ex:
            raise ValueError(
                f"ERROR: Timestamp ISO8601 validation error: {ex}")

    @field_validator('audio_files', mode='after')
    def encoded_audio_validator(cls, value: str) -> str:
        try:
            for file in value:
                encoded_audio = file['encoded_audio']
                file_name = file['file_name']
                try:
                    validation = base64.b64decode(encoded_audio, validate=True)
                except binascii.Error as ex:
                    raise ValueError(
                        f"ERROR: String is not Base64 encoded: {ex}")
            return value
        except Exception as ex:
            raise ValueError(f"Dictonairy attributes error: {ex}")
