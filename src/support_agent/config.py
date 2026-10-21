from pathlib import Path
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    data_dir: Path = PROJECT_ROOT/"data"

    @property
    def dense_index_path(self) -> Path:
        return self.data_dir/"index"/"dense"

    @property
    def sparse_index_path(self) -> Path:
        return self.data_dir/"index"/"sparse"

settings = Settings()