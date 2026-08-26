import numpy as np
from PIL import Image
from preset_base import Preset

class Wipe(Preset):
    name = "Wipe"
    mode = "animation"

    params = [
        # Source Choice
        {
            "name": "Source",
            "key": "source_type",
            "type": "choice",
            "options": ["Color", "Image"],
            "default": "Color"
        },
        
        # Image File
        {
            "name": "Image File",
            "key": "image_path",
            "type": "file",
            "default": ""
        },

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
            "options": ["Wipe In", "Wipe Out"],
            "default": "Wipe In"
        },

        # Fade starting position (Top / Bottom)
        {
            "name": "Wipe Start",
            "key": "wipe_start",
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
    # ╭─ Parameters ─────────────────────────────────────╮
        width, height = 400, 32
        source_type = kwargs.get("source_type", "Color")
        image_path = kwargs.get("image_path", "")
        base_color = np.array(kwargs["color"])
        in_out = kwargs["in_out"]
        wipe_start = kwargs["wipe_start"]
        easing = kwargs["easing"]
        smoothness = kwargs["smoothness"]
    # ╰──────────────────────────────────────────────────╯
        
    # ╭─ Empty array ────────────────────────────────────────────╮
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
    # ╰──────────────────────────────────────────────────────────╯
        
    # ╭─ Determine target colors for the 32 pixels ──────────────────╮
        if source_type == "Image" and image_path:
            try:
                img = Image.open(image_path).convert("RGB")
                # Force resize in case user uploads something else
                img = img.resize((2, height)) 
                img_np = np.array(img)
                # Take the first column of the image
                # Shape becomes (32, 3)
                target_colors = img_np[:, 0, :] 

            except Exception as e:
                print(f"Failed to load image: {e}")
                # Fall back to solid color
                target_colors = np.tile(base_color, (height, 1)) 
        else:
            # Tile the base color to create a (32, 3) array
            target_colors = np.tile(base_color, (height, 1))
    # ╰─────────────────────────────────────────────────────────────╯

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
            
        # ╭─ Adjust direction ───────╮
            if in_out == "Wipe Out":
                edge = height - edge
        # ╰──────────────────────────╯

        # ╭─ Calculate alpha for each pixel ────────────────────────
            if ((in_out == "Wipe In" and wipe_start == "Top") or
                (in_out == "Wipe Out" and wipe_start == "Bottom")):
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

        # ╭─ Assemble frame ────────────────────────────────────────╮
            # Reshape alpha : (height,) -> (height, 1)
            alpha = alpha.reshape(-1, 1)
            frame_colors = (target_colors * alpha).astype(np.uint8)
            img_array[:, frame] = frame_colors
        # ╰─────────────────────────────────────────────────────────╯
                    
        return img_array

