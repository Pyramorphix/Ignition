import colorsys
import numpy as np
from preset_base import Preset

class RainbowAnimation(Preset):
    name = "Rainbow Fade"
    mode = "animation"

    params = [
        # Starting color (frame)
        {
            "name": "Start Shift",
            "key": "shift",
            "type": "int",
            "min": 0, "max": 399,
            "default": 0
        }
    ]

    def generate(self, kwargs):
    # ╭─ Parameters ────────────╮
        width, height = 400, 32
        shift = kwargs["shift"]
    # ╰─────────────────────────╯

    # ╭─ Empty array ────────────────────────────────────────────╮
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
    # ╰──────────────────────────────────────────────────────────╯
        
    # ╭─ RAINBOW!!!!! ──────────────────────────────────────────────╮
        for x in range(width):
            hue = ((x + shift) % width) / width
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            img_array[:, x] = np.array([int(c * 255) for c in rgb])
    # ╰─────────────────────────────────────────────────────────────╯
            
        return img_array
