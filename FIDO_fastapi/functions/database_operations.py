import sqlite3
from FIDO_fastapi.environment import Environment
from FIDO_fastapi.models.FIDO_models import AudioMetadata


class DatabaseOperations:

    def __init__(self):
        self.env = Environment()
        self.connection = sqlite3.connect(self.env.db_url)
        self.cursor = self.connection.cursor()

    def insert_audio_metadata(self, audio_metadata: AudioMetadata):
        try:
            parameters = (audio_metadata.session_id,
                          audio_metadata.timestamp,
                          audio_metadata.file_name,
                          audio_metadata.audio_length)

            query = """INSERT INTO AUDIO_METADATA 
            (SESSION_ID,TIMESTAMP,FILE_NAME,AUDIO_LENGTH)
            VALUES (?,?,?,?);"""
            self.cursor.execute(query, parameters)
            self.connection.commit()
        except sqlite3.Error as ex:
            self.connection.rollback()
            raise sqlite3.Error(f"ERROR: Insert audio_metadata failed. {ex}")
        except Exception as ex:
            raise (f"ERROR: Unexpected database error. {ex}")

    def close_cursor(self):
        self.cursor.close

    def close_instance(self):
        self.cursor.close
        self.connection.close()
