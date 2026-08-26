import numpy as np
from scipy import signal
from preset_base import Preset

class PulseStrobe(Preset):
    name = "Color Pulse / Strobe"
    mode = "animation"

    params = [
        # Pulsation color
        {
            "name": "Color", 
            "key": "color",
            "type": "color",
            "default": (0, 255, 0)
        },

        # Pulse mode
        {
            "name": "Pulse mode",
            "key": "mode",
            "type": "choice",
            "options": ["sine wave", "rect wave"],
            "default": "sine wave"
        },

        # Amount of pulses
        {
            "name": "Pulses per Rotation",
            "key": "pulses",
            "type": "int", 
            "min": 1,
            "max": 20,
            "default": 5
        },

        # Start from color or from black
        {
            "name": "Start from:",
            "key": "start",
            "type": "choice",
            "options": ["black", "color"],
            "default": "black"
        }
    ]

    def generate(self, kwargs):
    # ╭─ Parameters ──────────────────────╮
        width, height = 400, 32
        color = np.array(kwargs["color"])
        mode = kwargs["mode"]
        pulses = kwargs["pulses"]
        start = kwargs["start"]
    # ╰───────────────────────────────────╯
        
    # ╭─ Empty array ────────────────────────────────────────────╮
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
    # ╰──────────────────────────────────────────────────────────╯
        
    # ╭─ Chosen wave assigned to color intensity ──────────────────────────────────╮
        # Phase shift based on selected start point
        dphi = np.pi if start == "black" else 0

        if mode == "sine wave":
            for x in range(width):
                wave = (np.cos((x / width) * pulses * 2 * np.pi + dphi) + 1) / 2.0
                
                img_array[:, x] = (color * wave).astype(np.uint8)

        elif mode == "rect wave":
            for x in range(width):
                wave = (signal.square((x / width) * pulses * 2 * np.pi + dphi))

                img_array[:, x] = (color * wave).astype(np.uint8)
    # ╰────────────────────────────────────────────────────────────────────────────╯
            
        return img_array
