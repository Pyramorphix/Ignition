import numpy as np
from preset_base import Preset

class StaticColor(Preset):
    name = "Static Color"
    mode = "image"
    params = [
        # Color (what else did you expect?)
        {
            "name": "Color",
            "key": "color",
            "type": "color",
            "default": (204, 204, 204)
        }
    ]

    def generate(self, kwargs):
    # ╭─ Empty array ────────────────────────────────────╮
        img_array = np.zeros((32, 2, 3), dtype=np.uint8)
    # ╰──────────────────────────────────────────────────╯
    # ╭─ Fill it with selected color ───────────────╮
        img_array[:, :] = np.array(kwargs["color"])
    # ╰─────────────────────────────────────────────╯
        return img_array

