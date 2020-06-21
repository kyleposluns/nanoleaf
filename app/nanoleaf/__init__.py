from dotenv import load_dotenv
from pathlib import Path
from app.nanoleaf.aurora import Aurora

load_dotenv(dotenv_path=Path("../../") / ".env")