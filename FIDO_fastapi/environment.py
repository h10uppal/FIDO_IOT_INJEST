from dotenv import load_dotenv
import os


class Environment:

    def __init__(self) -> None:
        load_dotenv()
        # SQLite
        self.db_url = os.getenv("SQLITE_DB")
        self.sample_rate = 4000
