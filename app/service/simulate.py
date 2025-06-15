"""
This module will simulate the creation of labeled neural thought data.
"""
import numpy as np
import base64
import json
from datetime import datetime
import random
import torch

_eeg_simulated_data = None
_eeg_simulated_data_labels = None
_data_loaded = False

def serialize_numpy_array(array: np.ndarray) -> str:
    """Serialize numpy array to base64 string"""
    return base64.b64encode(array.tobytes()).decode('utf-8')

def create_message(array: np.ndarray, label: str = None) -> str:
    """Combine metadata and array into a single JSON message"""
    return json.dumps({
        "content": {
            "label": label,
            "dtype": str(array.dtype), 
            "shape": array.shape,
            "data": serialize_numpy_array(array)
        }
    })


def load_simulated_eeg_data():
    # load mock data
    global _eeg_simulated_data, _eeg_simulated_data_labels    
    if _data_loaded:
        return
    # filepath definitions
    mock_eeg_data_file_path = "../model/data/mock/Simulation_data/X_all.pth"
    mock_eeg_data_label_file_path = "../model/data/mock/Simulation_data/y_all.pth"

    _eeg_simulated_data = torch.load(mock_eeg_data_file_path)
    _eeg_simulated_data_labels = torch.load(mock_eeg_data_label_file_path)

    _data_loaded = True
    return _data_loaded


def get_random_eeg_sample_json() -> str:
    """Return one randomly selected EEG sample with label as JSON message"""
    if not _data_loaded:
        load_simulated_eeg_data()

    total_samples = len(_eeg_simulated_data)
    index = random.randint(0, total_samples - 1)

    sample = _eeg_simulated_data[index].numpy()  # shape: [128, 1152]
    label = _eeg_simulated_data_labels[index]

    return create_message(sample, label)
