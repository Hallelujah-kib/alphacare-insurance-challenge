"""Data loading utilities for insurance risk analytics.

Includes functionality for loading raw data, creating derived features,
and integrating with data version control systems.
"""

import pandas as pd
from pathlib import Path
from .versioning import DVCManager
from ..utils.logger import get_logger

logger = get_logger(__name__)

class InsuranceDataLoader:
    """Handles loading and preprocessing of insurance data.
    
    Args:
        config_manager: Configuration manager instance
    """
    
    def __init__(self, config_manager):
        self.config = config_manager
        self.dvc = DVCManager(
            remote_path=self.config.get('dvc.remote_path')
        )
        
    def load_raw_data(self) -> pd.DataFrame:
        """Load and version raw data using DVC.
        
        Returns:
            Raw DataFrame with insurance data
            
        Raises:
            FileNotFoundError: If data file doesn't exist
            pd.errors.EmptyDataError: For empty files
        """
        try:
            raw_dir = Path(self.config.get('data.raw_dir', 'data/raw'))
            raw_file = self.config.get('data.raw_file')
            
            if not raw_file:
                raise ValueError("No raw_file specified in config")
            
            # Construct full path
            data_path = raw_dir / raw_file
            
            # Verify file exists
            if not data_path.exists():
                available_files = list(raw_dir.glob('*'))
                raise FileNotFoundError(
                    f"Data file {data_path} not found. "
                    f"Available files: {available_files}")
                
            logger.info(f"Loading data from: {data_path}")
            
            df = pd.read_csv(
                data_path,
                sep='|',
                parse_dates=['TransactionMonth'],
                na_values=[' ', '.000000000000'],
                low_memory=False
            )
            logger.info(f"Loaded data with shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Data loading failed: {str(e)}")
            raise
            
    def create_derived_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create business-specific derived features.
        
        Args:
            df: Raw DataFrame to enhance
            
        Returns:
            DataFrame with additional derived features
            
        Raises:
            KeyError: If required columns are missing
        """
        try:
            # Essential features
            df['LossRatio'] = df['TotalClaims'] / df['TotalPremium']
            df['VehicleAge'] = df['TransactionMonth'].dt.year - df['RegistrationYear']
            
            # Claim indicators
            df['HasClaim'] = (df['TotalClaims'] > 0).astype(int)
            df['ClaimSeverity'] = df['TotalClaims'].where(df['TotalClaims'] > 0, 0)
            
            # Risk categories
            df['RiskCategory'] = pd.cut(
                df['LossRatio'],
                bins=[0, 0.3, 0.6, 1, float('inf')],
                labels=['Low', 'Medium', 'High', 'Extreme'],
                right=False
            )
            logger.info("Derived features created successfully")
            return df
        except KeyError as e:
            logger.error(f"Missing column for feature engineering: {str(e)}")
            raise