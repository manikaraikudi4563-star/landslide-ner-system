"""
Abstract Machine Learning Model Interface for Landslide Risk Prediction in NER-LEWS.
Provides a standard contract for swappable ML algorithms (Random Forest, XGBoost, Deep Learning, etc.).
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List

class ILandslideModel(ABC):
    @abstractmethod
    def preprocess(self, raw_features: Dict[str, Any]) -> Dict[str, float]:
        """Validates and normalizes raw environmental and sensor features."""
        pass

    @abstractmethod
    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes inference to predict landslide susceptibility.
        Returns:
            dict containing:
                - risk_score: float (0.0 - 100.0)
                - risk_tier: str (LOW, MODERATE, HIGH, CRITICAL)
                - confidence: float (0.0 - 1.0)
                - factor_contributions: Dict[str, float] (XAI feature breakdown)
        """
        pass
