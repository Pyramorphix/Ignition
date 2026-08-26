import numpy as np
from preset_base import Preset

class MultiGradient(Preset):
    name = "Multi Gradient"
    mode = "image"

    params = [
        # Number of colors to use
        {
            "name": "Number of Colors",
            "key": "num_colors",
            "type": "choice",
            "options": ["3", "4", "5"],
            "default": "3"
        },
        
        # Color pickers (All 5 are listed, but only the selected amount are used)
        { "name": "Color 1 (Top)", "key": "c1", "type": "color", "default": (255, 0, 0) },
        { "name": "Color 2",       "key": "c2", "type": "color", "default": (255, 255, 0) },
        { "name": "Color 3",       "key": "c3", "type": "color", "default": (0, 255, 0) },
        { "name": "Color 4",       "key": "c4", "type": "color", "default": (0, 255, 255) },
        { "name": "Color 5 (Bottom)", "key": "c5", "type": "color", "default": (0, 0, 255) }
    ]

    def generate(self, kwargs):
    # ╭─ Parameters ──────────────────────╮
        width, height = 2, 32
        # Convert string choice to integer
        num_colors = int(kwargs["num_colors"]) 
    # ╰───────────────────────────────────╯
        
    # ╭─ Gather Active Colors ─────────────────────────────────────╮
        color_keys = ["c1", "c2", "c3", "c4", "c5"]
        
        # Slice the list to only grab the colors we actually need
        active_colors = [kwargs[k] for k in color_keys[:num_colors]]
    # ╰────────────────────────────────────────────────────────────╯
        
    # ╭─ Interpolation Setup ───────────────────────────────────────────────╮
        # Map out the exact Y coordinates where our pure colors will sit.
        # e.g., for 3 colors on 32px: [0.0, 15.5, 31.0]
        y_anchor_positions = np.linspace(0, height - 1, num_colors)
        
        # The indices of all 32 pixels
        pixel_indices = np.arange(height)
    # ╰─────────────────────────────────────────────────────────────────────╯

    # ╭─ Calculate Gradient ───────────────────────────────────────────────────╮
        # We must interpolate R, G, and B channels independently
        r_anchors = [c[0] for c in active_colors]
        g_anchors = [c[1] for c in active_colors]
        b_anchors = [c[2] for c in active_colors]

        # Use numpy's 1D linear interpolation mapped over the 32 pixels
        r_interp = np.interp(pixel_indices, y_anchor_positions, r_anchors)
        g_interp = np.interp(pixel_indices, y_anchor_positions, g_anchors)
        b_interp = np.interp(pixel_indices, y_anchor_positions, b_anchors)
    # ╰────────────────────────────────────────────────────────────────────────╯

    # ╭─ Assemble the Image Array ─────────────────────────────────────────────╮
        # Stack the 3 separated color channels into a single (32, 3) column
        gradient_column = np.column_stack((r_interp, g_interp, b_interp)).astype(np.uint8)

        # Tile the column horizontally to stretch it across our 2px width 
        # Shape goes from (32, 3) -> (32, 2, 3)
        img_array = np.tile(gradient_column[:, np.newaxis, :], (1, width, 1))
    # ╰────────────────────────────────────────────────────────────────────────╯
                    
        return img_array
