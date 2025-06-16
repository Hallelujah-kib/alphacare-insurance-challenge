"""Exploratory data analysis (EDA) utilities for insurance data.

Implements data quality assessment, risk factor analysis, and visualization
generation.
"""

import pandas as pd
import numpy as np
from src.utils.visualization import Visualizer
from src.utils.logger import get_logger

logger = get_logger(__name__)

class InsuranceEDA:
    """Performs comprehensive exploratory data analysis.
    
    Args:
        visualizer: Visualization utility instance
    """
    
    def __init__(self, visualizer: Visualizer):
        self.visualizer = visualizer
        
    def generate_quality_report(self, df: pd.DataFrame) -> dict:
        """Generate comprehensive data quality report.
        
        Includes:
        - Missing value counts and percentages
        - Data type summary
        - Numeric feature statistics
        - Categorical feature cardinality
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with quality metrics
        """
        report = {
            'missing_values': self._calculate_missing(df),
            'dtype_summary': self._get_dtype_summary(df),
            'numeric_stats': self._get_numeric_stats(df),
            'categorical_summary': self._get_categorical_summary(df)
        }
        logger.info("Generated data quality report")
        return report
    
    def analyze_risk_factors(self, df: pd.DataFrame, output_dir: str):
        """Generate key risk visualizations.
        
        Produces:
        1. Provincial risk profile
        2. Vehicle risk analysis
        3. Temporal claim trends
        
        Args:
            df: Cleaned DataFrame
            output_dir: Directory to save visualizations
        """
        try:
            # Provincial risk
            provincial_risk = df.groupby('Province').agg(
                Policies=('PolicyID', 'nunique'),
                AvgLossRatio=('LossRatio', 'mean'),
                ClaimFrequency=('HasClaim', 'mean')
            ).reset_index()
            self.visualizer.plot_provincial_risk(provincial_risk, output_dir)
            
            # Vehicle risk
            vehicle_risk = df.groupby('make').agg(
                Policies=('PolicyID', 'nunique'),
                AvgClaim=('ClaimSeverity', 'mean')
            ).query('Policies > 50').reset_index()
            self.visualizer.plot_vehicle_risk(vehicle_risk, output_dir)
            
            # Temporal trends
            temporal_df = self._prepare_temporal_data(df)
            self.visualizer.plot_temporal_trends(temporal_df, output_dir)
            
            logger.info("Risk factor analysis completed")
        except Exception as e:
            logger.error(f"Risk analysis failed: {str(e)}")
            raise
    
    def _calculate_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate missing value statistics."""
        missing = df.isnull().sum()
        missing_pct = (missing / len(df)) * 100
        return pd.DataFrame({
            'missing_count': missing,
            'missing_pct': missing_pct
        }).sort_values('missing_pct', ascending=False)
    
    def _get_dtype_summary(self, df: pd.DataFrame) -> dict:
        """Summarize data types distribution."""
        return df.dtypes.value_counts().to_dict()
    
    def _get_numeric_stats(self, df: pd.DataFrame) -> dict:
        """Compute descriptive statistics for numeric features."""
        return df.describe(percentiles=[0.25, 0.5, 0.75, 0.95]).to_dict()
    
    def _get_categorical_summary(self, df: pd.DataFrame) -> dict:
        """Calculate cardinality for categorical features."""
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        return {col: df[col].nunique() for col in cat_cols}
    
    def _prepare_temporal_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare monthly aggregated data for trend analysis."""
        monthly = df.groupby(pd.Grouper(key='TransactionMonth', freq='M')).agg(
            TotalPremium=('TotalPremium', 'sum'),
            TotalClaims=('TotalClaims', 'sum'),
            ClaimCount=('HasClaim', 'sum'),
            PolicyCount=('PolicyID', 'nunique')
        )
        monthly['LossRatio'] = monthly['TotalClaims'] / monthly['TotalPremium']
        monthly['AvgClaim'] = monthly['TotalClaims'] / monthly['ClaimCount']
        return monthly.reset_index()