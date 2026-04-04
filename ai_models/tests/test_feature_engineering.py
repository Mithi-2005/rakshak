import unittest

from utils.feature_engineering import create_features


class FeatureEngineeringTests(unittest.TestCase):
    def test_create_features_includes_aqi_and_temperature(self):
        features = create_features(
            location_info={"risk_zone": 0.7},
            weather_features={
                "rainy_hours_next_48h": 10,
                "avg_rainfall_next_48h": 4.5,
                "rainy_hours_last_24h": 6,
                "avg_temperature_next_48h": 31.2,
            },
            aqi_features={"aqi_trend": 0.64},
            claim_history=2,
            avg_income=850,
        )

        self.assertIn("avg_temperature_next_48h", features)
        self.assertIn("aqi_trend", features)
        self.assertGreater(features["disruption_score"], 0)


if __name__ == "__main__":
    unittest.main()
