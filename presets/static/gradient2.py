import numpy as np
from preset_base import Preset

class TwoColorGradient(Preset):
    name = "2-Color Gradient"
    mode = "image"
    
    params = [
        # First color
        {
            "name": "Color 1 (Top/Center)",
            "key": "c1",
            "type": "color",
            "default": (255, 0, 0)
        },

        # Second color
        {
            "name": "Color 2 (Bottom/Edge)",
            "key": "c2",
            "type": "color",
            "default": (0, 0, 255)
        },

        # Gradient type (Linear / Radial)
        {
            "name": "Gradient Style",
            "key": "style",
            "type": "choice",
            "options": ["Linear", "Radial"],
            "default": "Linear"
        }
    ]

    def generate(self, kwargs):
    # ╭─ Parameters ────────────────╮
        width, height = 2, 32
        c1 = np.array(kwargs["c1"])
        c2 = np.array(kwargs["c2"])
        style = kwargs["style"]
    # ╰─────────────────────────────╯
        
    # ╭─ Empty array ────────────────────────────────────────────╮
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
    # ╰──────────────────────────────────────────────────────────╯
            
        if style == "Linear":
        # ╭─ Linear math ──────────────────────────────────────────────────────────────────────╮
            # Create a straight 1D gradient from c1 to c2
            gradient_1d = np.linspace(c1, c2, height)
            
            # Tile it across the width
            img_array = np.tile(gradient_1d[:, np.newaxis, :], (1, width, 1)).astype(np.uint8)
        # ╰────────────────────────────────────────────────────────────────────────────────────╯
            
        elif style == "Radial":
        # ╭─ Radial math ─────────────────────────────────────────╮
            # Calculate center position
            center_pixel = (height - 1) / 2.0 
            
            for y in range(height):
                # Map distance from the center to [0, 1]
                distance = abs(y - center_pixel) / center_pixel
                
                # Create gradient
                blended = (c1 * (1 - distance)) + (c2 * distance)
                img_array[y, :] = blended.astype(np.uint8)
        # ╰───────────────────────────────────────────────────────╯
                
        return img_array

