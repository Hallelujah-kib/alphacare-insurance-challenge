"""Data cleaning utilities for insurance risk analytics.

Implements data cleaning pipelines including missing value imputation,
outlier handling, and categorical encoding.
"""

import numpy as np
import pandas as pd
from ..utils.logger import get_logger

logger = get_logger(__name__)

class DataCleaner:
    """Implements configurable data cleaning pipeline.
    
    Args:
        strategy_config: Dictionary of cleaning strategies
    """
    
    def __init__(self, strategy_config: dict):
        self.strategies = strategy_config
        
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply complete cleaning pipeline.
        
        Pipeline includes:
        1. Missing value handling
        2. Numeric column correction
        3. Outlier treatment
        4. Categorical encoding
        
        Args:
            df: DataFrame to clean
            
        Returns:
            Cleaned DataFrame
        """
        try:
            df = self._handle_missing_values(df)
            df = self._fix_numeric_columns(df)
            df = self._winsorize_outliers(df)
            df = self._encode_categoricals(df)
            logger.info("Data cleaning completed")
            return df
        except Exception as e:
            logger.error(f"Cleaning failed: {str(e)}")
            raise
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values with exact column name matching."""
        for col, strategy in self.strategies['missing_values'].items():
            # Use exact column name from config
            if col not in df.columns:
                available_cols = [c for c in df.columns if c.lower() == col.lower()]
                if available_cols:
                    logger.warning(f"Using {available_cols[0]} instead of {col}")
                    col = available_cols[0]  # Use case-insensitive match if found
                else:
                    logger.warning(f"Column {col} not found in DataFrame. Available columns: {list(df.columns)}")
                    continue
                    
            if strategy == 'fill_mode':
                df[col] = df[col].fillna(df[col].mode()[0])
            elif strategy == 'fill_median':
                df[col] = df[col].fillna(df[col].median())
            elif strategy == 'fill_unknown':
                df[col] = df[col].fillna('Unknown')
        
        return df
    
    def _fix_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle zero/invalid values in numeric columns."""
        for col in self.strategies['numeric_columns']:
            df[col] = df[col].replace(0, np.nan).fillna(df[col].median())
        return df
    
    def _winsorize_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Winsorize numeric columns while preserving NaN values."""
        from scipy.stats import mstats
        
        for col in self.strategies['outlier_columns']:
            if col not in df.columns:
                continue
                
            # Preserve original index and NA values
            mask = df[col].notna()
            if mask.any():  # Only process if non-NA values exist
                winsorized = mstats.winsorize(
                    df.loc[mask, col].values,
                    limits=self.strategies['winsorize_limits']
                )
                df.loc[mask, col] = winsorized
                
        return df
    
    def _encode_categoricals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Reduce cardinality of high-dimension categoricals."""
        high_cardinality = self.strategies.get('high_cardinality_cols', [])
        for col in high_cardinality:
            if col in df.columns:
                top_categories = df[col].value_counts().head(10).index
                df[col] = df[col].where(df[col].isin(top_categories), 'Other')
        return df