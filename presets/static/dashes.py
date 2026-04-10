import numpy as np
from preset_base import Preset

class Dashes(Preset):
    name = "Dashes"
    mode = "image"

    params = [
        # Dash color 1
        {
            "name": "Color 1",
            "key": "c1",
            "type": "color",
            "default": (255, 0, 255)
        },

        # Dash color 2
        {
            "name": "Color 2",
            "key": "c2",
            "type": "color",
            "default": (0, 0, 0)
        },

        # Dash size
        {
            "name": "Dash Size (Pixels)",
            "key": "size",
            "type": "int",
            "min": 1,
            "max": 16,
            "default": 2
        }
    ]

    def generate(self, kwargs):
    # ╭─ Parameters ────────────────╮
        width, height = 2, 32
        c1 = np.array(kwargs["c1"])
        c2 = np.array(kwargs["c2"])
        size = kwargs["size"]
    # ╰─────────────────────────────╯
        
    # ╭─ Empty array ────────────────────────────────────────────╮
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
    # ╰──────────────────────────────────────────────────────────╯
        
    # ╭─ Generate dashes ────────────╮
        for y in range(height):
            if (y // size) % 2 == 0:
                img_array[y, :] = c1
            else:
                img_array[y, :] = c2
    # ╰──────────────────────────────╯
                
        return img_array

