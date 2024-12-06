import torch
from TTS.api import TTS
from typing import Dict

class ModelManager:
    """A class to manage multiple TTS models."""
    
    def __init__(self):
        self.models: Dict[str, TTS] = {}

    def load_model(self, model_name: str) -> TTS:
        """
        Load and cache a TTS model by name.

        Args:
            model_name (str): Name of the TTS model to load.

        Returns:
            TTS: Loaded TTS model.
        """
        if model_name in self.models:
            return self.models[model_name]
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = TTS(model_name).to(device)
        self.models[model_name] = model
        return model

    def get_model(self, model_name: str) -> TTS:
        """
        Retrieve a pre-loaded TTS model.

        Args:
            model_name (str): Name of the TTS model to retrieve.

        Returns:
            TTS: TTS model instance.
        """
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' is not loaded. Use 'load_model' first.")
        return self.models[model_name]

model_manager = ModelManager()
