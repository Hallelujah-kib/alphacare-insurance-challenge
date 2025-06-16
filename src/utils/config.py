"""Configuration management utilities for loading and accessing settings.

Provides a ConfigManager class to handle YAML configuration files with
hierarchical key access and update capabilities.
"""

import yaml
from pathlib import Path


class ConfigManager:
    """Manages application configuration through YAML files.
    
    Provides hierarchical key access using dot notation and supports
    runtime configuration updates.
    
    Args:
        config_path: Path to YAML configuration file (default: 'config/settings.yml')
    
    Attributes:
        config (dict): Parsed configuration dictionary
        config_path (Path): Path to configuration file
    """
    
    def __init__(self, config_path: str = "config/settings.yml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        """Load configuration from YAML file.
        
        Returns:
            Parsed configuration dictionary
            
        Raises:
            FileNotFoundError: If configuration file doesn't exist
            yaml.YAMLError: For malformed YAML files
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default=None):
        """Retrieve configuration value using dot notation.
        
        Args:
            key: Dot-separated key path (e.g., 'data.raw_file')
            default: Default value if key not found
            
        Returns:
            Value from configuration or default if not found
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def update(self, updates: dict):
        """Update configuration with new values and persist to file.
        
        Args:
            updates: Dictionary of updates to merge into configuration
        """
        self.config.update(updates)
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f)