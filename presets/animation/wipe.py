import numpy as np
from preset_base import Preset

class Wipe(Preset):
    name = "Wipe"
    mode = "animation"

    params = [
        # Color
        {
            "name": "Color",
            "key": "color",
            "type": "color",
            "default": (255, 0, 255)
        },

        # Mode (Fade in / Fade out)
        {
            "name": "Mode",
            "key": "in_out",
            "type": "choice",
            "options": ["Fade In", "Fade Out"],
            "default": "Fade In"
        },

        # Fade starting position (Top / Bottom)
        {
            "name": "Fade Start",
            "key": "fade_start",
            "type": "choice",
            "options": ["Top", "Bottom"],
            "default": "Bottom"
        },

        # Easing mode
        {
            "name": "Easing",
            "key": "easing",
            "type": "choice",
            "options": [
                "Linear",
                "Ease In",
                "Ease Out",
                "Ease In Out"
                ],
            "default": "Linear"
        },

        # Smoothness
        {
            "name": "Smoothness",
            "key": "smoothness",
            "type": "int",
            "min": 0,
            "max": 5,
            "default": 1
        }
    ]

    def generate(self, kwargs):
    # ╭─ Parameters ──────────────────────╮
        width, height = 400, 32
        color = np.array(kwargs["color"])
        in_out = kwargs["in_out"]
        fade_start = kwargs["fade_start"]
        easing = kwargs["easing"]
        smoothness = kwargs["smoothness"]
    # ╰───────────────────────────────────╯
        
    # ╭─ Empty array ────────────────────────────────────────────╮
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
    # ╰──────────────────────────────────────────────────────────╯
        
    # ╭─ Precompute pixel indices ───────────────────────────╮
        pixel_indices = np.arange(height, dtype=np.float32)
    # ╰──────────────────────────────────────────────────────╯

        for frame in range(width):
        # ╭─ Map time to [0, 1] ────╮
            t = frame / (width - 1)
        # ╰─────────────────────────╯
            
        # ╭─ Apply easing ──────────────────────────╮
            if easing == "Ease In":
                t = t * t
            elif easing == "Ease Out":
                t = 1 - (1 - t) * (1 - t)
            elif easing == "Ease In Out":
                if t < 0.5:
                    t = 2 * t * t
                else:
                    t = 1 - ((-2 * t + 2) ** 2) / 2
        # ╰─────────────────────────────────────────╯
                    
        # ╭─ Current edge position ───────╮
            edge = t * height
        # ╰───────────────────────────────╯
            
        # ╭─ Adjust fade direction ──╮
            if in_out == "Fade Out":
                edge = height - edge
        # ╰──────────────────────────╯

        # ╭─ Calculate alpha for each pixel ────────────────────────
            if ((in_out == "Fade In" and fade_start == "Top") or
                (in_out == "Fade Out" and fade_start == "Bottom")):
                # Edge moves from the top downwards
                # Pixels near top should be filled first
                dist_from_edge = edge - pixel_indices
            else:
                # Edge moves from the bottom upwards
                # Pixels near bottom should be filled first
                dist_from_edge = pixel_indices - (height - edge)
        # ╰─────────────────────────────────────────────────────────╯

        # ╭─ Calculate smoothness ───────────────────────────────────────╮
            if smoothness > 0:
                alpha = np.clip(dist_from_edge / smoothness + 0.5, 0, 1)
            else:
                alpha = (dist_from_edge >= 0).astype(np.float32)
        # ╰──────────────────────────────────────────────────────────────╯

        # ╭─ Assemble frame ────────────────────────────────╮
            # Reshape alpha : (height,) -> (height, 1)
            alpha = alpha.reshape(-1, 1)
            frame_colors = (color * alpha).astype(np.uint8)
            img_array[:, frame] = frame_colors
        # ╰─────────────────────────────────────────────────╯
                    
        return img_array

