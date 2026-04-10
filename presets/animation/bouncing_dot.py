import numpy as np
from preset_base import Preset

class BouncingDot(Preset):
    name = "Bouncing Glowing Dot"
    mode = "animation"
    params = [
        # Dot color
        {
            "name": "Dot Color",
            "key": "dot_color",
            "type": "color",
            "default": (255, 100, 0)
        },

        # Amount of bounces
        {
            "name": "Bounces",
            "key": "bounces",
            "type": "int",
            "min": 1,
            "max": 10,
            "default": 3
        },

        # Point size
        {
            "name": "Glow Size",
            "key": "glow",
            "type": "int",
            "min": 1,
            "max": 10,
            "default": 4
        },

        # Bounce amplitude
        {
            "name": "Amplitude",
            "key": "amplitude",
            "type": "int",
            "min": 10,
            "max": 100,
            "default": 100
        }
    ]

    def generate(self, kwargs):
    # ╭─ Parameters ────────────────────────────╮
        width, height = 400, 32
        color = np.array(kwargs["dot_color"])
        bounces = kwargs["bounces"]
        glow = kwargs["glow"]
        # Map 0-100 to 0.0-1.0
        amplitude = kwargs["amplitude"] / 100.0

        center_y = height / 2
        max_swing = center_y * amplitude
    # ╰─────────────────────────────────────────╯
        
    # ╭─ Empty array ────────────────────────────────────────────╮
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
    # ╰──────────────────────────────────────────────────────────╯
        
    # ╭─ Cosine wave ──────────────────────────────────────────────────────╮
        for x in range(width):
            wave = np.cos((x / width) * bounces * 2 * np.pi)
            dot_y = center_y + (wave * max_swing)
            
            # Glow
            for y in range(height):
                distance = abs(y - dot_y)
                if distance < glow:
                    intensity = 1.0 - (distance / glow)
                    img_array[y, x] = (color * intensity).astype(np.uint8)
    # ╰────────────────────────────────────────────────────────────────────╯
                    
        return img_array

