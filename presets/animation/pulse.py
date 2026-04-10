import numpy as np
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

        # Amount of pulses
        {
            "name": "Pulses per Rotation",
            "key": "pulses",
            "type": "int", 
            "min": 1,
            "max": 20,
            "default": 5
        }
    ]

    def generate(self, kwargs):
    # ╭─ Parameters ──────────────────────╮
        width, height = 400, 32
        color = np.array(kwargs["color"])
        pulses = kwargs["pulses"]
    # ╰───────────────────────────────────╯
        
    # ╭─ Empty array ────────────────────────────────────────────╮
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
    # ╰──────────────────────────────────────────────────────────╯
        
    # ╭─ Sine wave assigned to color intensity ─────────────────────────╮
        for x in range(width):
            wave = (np.cos((x / width) * pulses * 2 * np.pi) + 1) / 2.0
            
            img_array[:, x] = (color * wave).astype(np.uint8)
    # ╰─────────────────────────────────────────────────────────────────╯
            
        return img_array
