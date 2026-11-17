import pandas as pd

from backend.ai.anomaly_engine import AnomalyEngine


def test_anomaly_engine_detects_extreme_value():
    df = pd.DataFrame({
        "Revenue": [100] * 20 + [1000],
    })

    anomalies = AnomalyEngine().detect_anomalies(df)

    assert any(item["metric"] == "Revenue" for item in anomalies)
