"""Visualization utilities for insurance analytics.

Provides standardized plotting functions for risk analysis and
model interpretability.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from ..utils.logger import get_logger

logger = get_logger(__name__)

class Visualizer:
    """Creates publication-quality visualizations.
    
    Args:
        style_config: Dictionary of matplotlib/seaborn style parameters
    """
    
    def __init__(self, style_config=None):
        self.style = style_config or {
            'context': 'paper',
            'palette': 'colorblind',
            'font_scale': 1.2
        }
        self._apply_style()
        
    def _apply_style(self):
        """Apply consistent visualization style."""
        sns.set_theme(
            context=self.style['context'],
            palette=self.style['palette'],
            font_scale=self.style['font_scale']
        )
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['savefig.bbox'] = 'tight'
        plt.rcParams['font.family'] = 'DejaVu Sans'
        
    def plot_provincial_risk(self, data: pd.DataFrame, output_dir: str):
        """Create provincial risk profile visualization.
        
        Shows average loss ratio and claim frequency by province.
        
        Args:
            data: Aggregated provincial risk data
            output_dir: Directory to save plot
        """
        plt.figure(figsize=(12, 8))
        data = data.sort_values('AvgLossRatio', ascending=False)
        
        ax = sns.barplot(
            x='Province', 
            y='AvgLossRatio', 
            data=data,
            hue='ClaimFrequency',
            dodge=False
        )
        
        plt.title('Provincial Risk Profile')
        plt.xlabel('Province')
        plt.ylabel('Average Loss Ratio')
        plt.xticks(rotation=45)
        plt.legend(title='Claim Frequency')
        
        self._save_plot('provincial_risk.png', output_dir)
        
    def plot_vehicle_risk(self, data: pd.DataFrame, output_dir: str):
        """Create vehicle risk visualization.
        
        Shows top 10 riskiest vehicle makes by average claim amount.
        
        Args:
            data: Aggregated vehicle risk data
            output_dir: Directory to save plot
        """
        plt.figure(figsize=(14, 8))
        data = data.sort_values('AvgClaim', ascending=False).head(10)
        
        ax = sns.barplot(
            x='make', 
            y='AvgClaim', 
            data=data,
            palette='rocket'
        )
        
        # Add policy counts
        for i, row in enumerate(data.itertuples()):
            ax.text(i, row.AvgClaim + 500, 
                   f'Policies: {row.Policies}', 
                   ha='center')
        
        plt.title('Top 10 Risky Vehicle Makes')
        plt.xlabel('Vehicle Make')
        plt.ylabel('Average Claim Amount (ZAR)')
        plt.xticks(rotation=30)
        
        self._save_plot('vehicle_risk.png', output_dir)
        
    def _save_plot(self, filename: str, output_dir: str):
        """Save plot to specified directory.
        
        Args:
            filename: Output filename
            output_dir: Target directory
        """
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, filename)
        plt.tight_layout()
        plt.savefig(path)
        plt.close()
        logger.info(f"Saved visualization: {path}")