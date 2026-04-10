import numpy as np
from preset_base import Preset

class GlowingEndsCenter(Preset):
    name = "Glowing Ends/Center"
    mode = "image"

    params = [
        # Glow color
        {
            "name": "Color",
            "key": "color",
            "type": "color",
            "default": (0, 255, 255)
        },

        # Type (Glowing ends / Glowing center)
        {
            "name": "Position",
            "key": "position",
            "type": "choice",
            "options": ["Ends", "Center"],
            "default": "Ends"
        },

        # Glow size (how many pixels to include)
        {
            "name": "Glow Size",
            "key": "glow_size",
            "type": "int",
            "min": 1,
            "max": 16,
            "default": 4
        }
    ]

    def generate(self, kwargs):
    # ╭─ Parameters ──────────────────────╮
        width, height = 2, 32
        color = np.array(kwargs["color"])
        position = kwargs["position"]
        glow_size = kwargs["glow_size"]
    # ╰───────────────────────────────────╯
        
    # ╭─ Empty array ────────────────────────────────────────────╮
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
    # ╰──────────────────────────────────────────────────────────╯
        
    # ╭─ Loop through all pixels ──────────────────────────────────────╮
        for y in range(height):
            if position == "Ends":
                # Calculate distance to the closest edge
                # y=0 or y=31
                dist = min(y, 31 - y)
            elif position == "Center":
                # Calculate distance to the center
                # between y=15 and y=16
                dist = min(abs(y - 15), abs(y - 16))
            
            if dist < glow_size:
                # Linear intensity fade
                intensity = 1.0 - (dist / glow_size)
                img_array[y, :] = (color * intensity).astype(np.uint8)
    # ╰────────────────────────────────────────────────────────────────╯
                
        return img_array

