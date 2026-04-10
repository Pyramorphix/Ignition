import numpy as np
from preset_base import Preset

class SmoothTransition(Preset):
    name = "2-Color Seamless Transition"
    mode = "animation"

    params = [
        # Initial color
        {
            "name": "Color 1",
            "key": "c1",
            "type": "color",
            "default": (0, 255, 255)
        },

        # Final color
        {
            "name": "Color 2",
            "key": "c2",
            "type": "color",
            "default": (255, 0, 255)
         }
    ]

    def generate(self, kwargs):
    # ╭─ Parameters ────────────────╮
        width, height = 400, 32
        c1 = np.array(kwargs["c1"])
        c2 = np.array(kwargs["c2"])
    # ╰─────────────────────────────╯
        
    # ╭─ Empty array ────────────────────────────────────────────╮
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
    # ╰──────────────────────────────────────────────────────────╯
        
        for x in range(width):
        # ╭─ Sine wave mapped from -1..1 to 0..1 ───────────╮
            wave = (np.cos((x / width) *  np.pi) + 1) / 2.0
            
            blended = (c1 * wave) + (c2 * (1 - wave))
            img_array[:, x] = blended.astype(np.uint8)
        # ╰─────────────────────────────────────────────────╯
            
        return img_array
