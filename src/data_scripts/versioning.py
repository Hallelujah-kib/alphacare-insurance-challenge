"""Data version control utilities for the insurance analytics project."""

import os
from pathlib import Path

# Use relative import since this is in the same package
from ..utils.logger import get_logger

logger = get_logger(__name__)

class DVCManager:
    """Manages Data Version Control operations for the project.
    
    Args:
        remote_path: Path to DVC remote storage
    """
    
    def __init__(self, remote_path: str):
        self.remote_path = Path(remote_path)
        self.initialized = False
        self._check_dvc_ready()
    
    def _check_dvc_ready(self):
        """Verify DVC setup and remote configuration."""
        if not self.remote_path.exists():
            self.remote_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created DVC remote: {self.remote_path}")
        self.initialized = True
        
    def get_versioned_path(self, file_path: str) -> Path:
        """Get path relative to data/raw directory."""
        return (Path('data/raw') / file_path).resolve()