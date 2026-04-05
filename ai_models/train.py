"""
Model training script.
Generates synthetic dataset and trains risk prediction model.
Saves trained model to disk for use in prediction service.
"""

import pickle
import logging
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_synthetic_data(n_samples: int = 500) -> tuple:
    """
    Generate synthetic training data.

    Args:
        n_samples: Number of samples to generate

    Returns:
        Tuple of (X, y) where X is features and y is risk scores
    """
    np.random.seed(42)

    # Generate synthetic features
    risk_zones = np.random.uniform(0.3, 1.0, n_samples)
    rainy_hours_next_48h = np.random.randint(0, 49, n_samples)
    avg_rainfall_next_48h = np.random.uniform(0, 12, n_samples)
    rainy_hours_last_24h = np.random.randint(0, 25, n_samples)
    avg_temperature_next_48h = np.random.uniform(20, 42, n_samples)
    aqi_trend = np.random.uniform(0.05, 0.95, n_samples)
    claim_history = np.random.randint(0, 10, n_samples)
    avg_income = np.random.uniform(20000, 200000, n_samples)

    disruption_score = (
        rainy_hours_next_48h * 0.4
        + avg_rainfall_next_48h * 0.3
        + rainy_hours_last_24h * 0.2
        + risk_zones * 0.05
        + aqi_trend * 10 * 0.05
    )

    # Create feature matrix
    X = np.column_stack(
        [
            risk_zones,
            rainy_hours_next_48h,
            avg_rainfall_next_48h,
            rainy_hours_last_24h,
            avg_temperature_next_48h,
            aqi_trend,
            claim_history,
            avg_income,
            disruption_score,
        ]
    )

    feature_names = [
        "risk_zone",
        "rainy_hours_next_48h",
        "avg_rainfall_next_48h",
        "rainy_hours_last_24h",
        "avg_temperature_next_48h",
        "aqi_trend",
        "claim_history",
        "avg_income",
        "disruption_score",
    ]

    # Generate target variable (risk score between 0 and 1)
    # Future weather is weighted more than past weather.
    income_inverse = 1 - np.clip((avg_income - 20000) / (200000 - 20000), 0, 1)
    disruption_norm = np.clip(disruption_score / 26.0, 0, 1)

    y = (
        risk_zones * 0.20
        + (rainy_hours_next_48h / 48) * 0.23
        + (avg_rainfall_next_48h / 12) * 0.20
        + (rainy_hours_last_24h / 24) * 0.10
        + np.clip((avg_temperature_next_48h - 20) / 22, 0, 1) * 0.05
        + aqi_trend * 0.12
        + (claim_history / 10) * 0.16
        + income_inverse * 0.07
        + disruption_norm * 0.17
    )

    # Add some noise and clamp to [0, 1]
    y = np.clip(y + np.random.normal(0, 0.05, n_samples), 0, 1)

    return X, y, feature_names


def train_model(X: np.ndarray, y: np.ndarray) -> RandomForestRegressor:
    """
    Train Random Forest model.

    Args:
        X: Feature matrix
        y: Target variable (risk scores)

    Returns:
        Trained RandomForestRegressor model
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )

    logger.info("Training RandomForest model...")
    model.fit(X_train, y_train)

    # Evaluate
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    train_mse = mean_squared_error(y_train, y_pred_train)
    test_mse = mean_squared_error(y_test, y_pred_test)
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)

    logger.info(f"Training MSE: {train_mse:.4f}, Test MSE: {test_mse:.4f}")
    logger.info(f"Training R2: {train_r2:.4f}, Test R2: {test_r2:.4f}")

    return model


def save_model(model: RandomForestRegressor, model_path: str) -> None:
    """
    Save trained model to disk.

    Args:
        model: Trained model
        model_path: Path to save model
    """
    path = Path(model_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "wb") as f:
        pickle.dump(model, f)

    logger.info(f"Model saved to {model_path}")


def main():
    """Main training pipeline."""
    # Generate data
    X, y, feature_names = generate_synthetic_data(n_samples=500)
    logger.info(
        f"Generated {len(X)} training samples with {len(feature_names)} features"
    )

    # Train model
    model = train_model(X, y)

    # Save model relative to this file so cwd does not affect output location.
    model_path = str(Path(__file__).resolve().parent / "model" / "risk_model.pkl")
    save_model(model, model_path)

    logger.info("Training pipeline completed successfully!")


if __name__ == "__main__":
    main()
