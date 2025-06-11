"""
This module will simulate the creation of labeled neural thought data.
"""
import numpy as np
import base64
import json
from datetime import datetime

def serialize_numpy_array(array: np.ndarray) -> str:
    """Serialize numpy array to base64 string"""
    return base64.b64encode(array.tobytes()).decode('utf-8')

def create_message(array: np.ndarray, label: str = None) -> str:
    """Combing metadata and array into a single JSON message"""
    return json.dumps({
        "content": {
            "label": label,
            "dtype": str(array.dtype), 
            "shape": array.shape,
            "data": serialize_numpy_array(array)
        }
    })

