import numpy as np
from preset_base import Preset

class MovingDot(Preset):
    name = "Moving Dot"
    mode = "animation"

    params = [
        # Dot color
        {
            "name": "Dot Color",
            "key": "dot_color",
            "type": "color",
            "default": (0, 255, 255) # Cyan
        },

        # Amount of repetitions
        {
            "name": "Repetitions",
            "key": "num_reps",
            "type": "int",
            "min": 1,
            "max": 10,
            "default": 1
        },

        # Dot size (glow)
        {
            "name": "Dot Size",
            "key": "dot_size",
            "type": "int",
            "min": 1,
            "max": 10,
            "default": 4
        },

        # Starting point
        {
            "name": "Starting Point",
            "key": "start_point",
            "type": "choice",
            "options": ["Top", "Bottom"],
            "default": "Top"
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
        }
    ]

    def generate(self, kwargs):
    # ╭─ Parameters ──────────────────────────╮
        width, height = 400, 32
        color = np.array(kwargs["dot_color"])
        num_reps = kwargs["num_reps"]
        dot_size = kwargs["dot_size"]
        start_point = kwargs["start_point"]
        easing = kwargs["easing"]
    # ╰───────────────────────────────────────╯

    # ╭─ Empty array & precompute pixel indices ─────────────────╮
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
        pixel_indices = np.arange(height)
    # ╰──────────────────────────────────────────────────────────╯

    # ╭─ Expand travel range for smooth entry/exit ─────────────────────╮
        # To make the dot slide in and out smoothly, it needs to travel
        # "off-screen". The extra distance is the radius of the glow
        glow_offset = dot_size - 1
        
        # The total distance the dot's center must travel
        total_travel_distance = (height - 1) + 2 * glow_offset
    # ╰─────────────────────────────────────────────────────────────────╯

        for x in range(width):
        # ╭─ Calculate normalized time for the current cycle ─────╮
            # t goes from 0 to num_reps over the whole animation
            t = (x / (width - 1)) * num_reps
            # t_cycle is the fractional part, looping from 0 to 1
            t_cycle = t % 1.0
        # ╰───────────────────────────────────────────────────────╯

        # ╭─ Apply easing to the cycle time ────────────────────╮
            eased_t = t_cycle
            if easing == "Ease In":
                eased_t = t_cycle * t_cycle
            elif easing == "Ease Out":
                eased_t = 1 - (1 - t_cycle) * (1 - t_cycle)
            elif easing == "Ease In Out":
                if t_cycle < 0.5:
                    eased_t = 2 * t_cycle * t_cycle
                else:
                    eased_t = 1 - ((-2 * t_cycle + 2) ** 2) / 2
        # ╰─────────────────────────────────────────────────────╯

        # ╭─ Calculate the dot's y-position ─────────────────────────────╮
            # Map eased time [0, 1] to expanded travel distance
            if start_point == "Top":
                dot_y = -glow_offset + (eased_t * total_travel_distance)
            else: # "Bottom"
                start_pos = -glow_offset + total_travel_distance
                dot_y = start_pos - (eased_t * total_travel_distance)
        # ╰──────────────────────────────────────────────────────────────╯

        # ╭─ Calculate glow intensity for all pixels in column ─────╮
            # Distance of each pixel from the dot's center
            distances = np.abs(pixel_indices - dot_y)
            # Intensity (1 at center, 0 at edge of glow)
            # and clip values to (0,1).
            intensities = np.clip(1 - (distances / dot_size), 0, 1)
        # ╰─────────────────────────────────────────────────────────╯

        # ╭─ Assemble frame column ──────────────────────────────────────────────╮
            # Reshape intensities from (height,) to (height, 1)
            # to broadcast with color (3,) -> result (height, 3)
            frame_column = (color * intensities.reshape(-1, 1)).astype(np.uint8)
            img_array[:, x] = frame_column
        # ╰──────────────────────────────────────────────────────────────────────╯
                                                                                        
        return img_array                                                                
                                                                                        
                                                                                        
