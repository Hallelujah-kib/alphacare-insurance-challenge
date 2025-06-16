"""Main execution pipeline for insurance risk analytics.

Orchestrates the end-to-end workflow including:
- Data loading and cleaning
- Exploratory data analysis
- Hypothesis testing
- Model training and evaluation
"""

from src.data.loader import InsuranceDataLoader
from src.data.cleaner import DataCleaner
from src.analysis.eda import InsuranceEDA
from src.analysis.hypothesis import HypothesisTester
from src.modeling.trainer import RiskModelTrainer
from src.utils.visualization import Visualizer
from src.utils.config import ConfigManager
from src.utils.logger import setup_logging
import joblib

def main():
    """Execute the end-to-end analytics pipeline."""
    # Initialize system
    setup_logging()
    config = ConfigManager("config/settings.yml")
    
    # === DATA PIPELINE ===
    loader = InsuranceDataLoader(config)
    cleaner = DataCleaner(config.get('cleaning_strategies'))
    
    # Load and preprocess data
    df = loader.load_raw_data()
    df = loader.create_derived_features(df)
    df = cleaner.clean(df)
    
    # Save cleaned data
    processed_path = config.get('data.processed_path')
    df.to_parquet(processed_path)
    print(f"Saved cleaned data to {processed_path}")
    
    # === ANALYSIS PIPELINE ===
    visualizer = Visualizer()
    eda = InsuranceEDA(visualizer)
    
    # Generate reports
    eda_report = eda.generate_quality_report(df)
    eda.analyze_risk_factors(df, config.get('reports.figures_path'))
    
    # Hypothesis testing
    tester = HypothesisTester(alpha=0.05)
    provincial_result = tester.test_provincial_risk(df)
    gender_result = tester.test_gender_risk(df)
    
    # Save hypothesis results
    joblib.dump(
        {'provincial': provincial_result, 'gender': gender_result},
        config.get('reports.hypothesis_results_path')
    )
    
    # === MODELING PIPELINE ===
    trainer = RiskModelTrainer(config)
    model_results = trainer.train_models(df)
    
    # Save final results
    joblib.dump(
        {'eda': eda_report, 'models': model_results},
        config.get('reports.final_results_path')
    )
    print("Pipeline executed successfully!")

if __name__ == '__main__':
    main()