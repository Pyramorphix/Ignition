# Ignition

A PyQt6-based GUI application for designing LED matrix presets. Create static images or animations and export them as BMP files.


## Included Presets

### Static Images
- Dashes
- Glowing Ends / Center
- 2-color Gradient
- Static Color

### Animations
- Bouncing Dot
- Pulse
- Rainbow
- Smooth Transition
- Wipe


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Pyramorphix/Ignition
   cd ignition
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```bash
python Ignition.py
```

### How to Use

1. **Select Mode**: Choose between "Image" or "Animation" mode
2. **Choose a Preset**: Select from the dropdown list of available presets
3. **Configure Parameters**: Use the dynamically generated controls for customization.
4. **Preview**: View your design in real-time in the preview panel
   - For animations, check "Play Animation" to see the sequence
   - Adjust playback speed using the slider
5. **Export**: Click "Export as .BMP" to save your creation

## Project Structure

```
ignition/
├── Ignition.py          # Application entry point
├── main_window.py       # Main GUI window and logic
├── preset_base.py       # Base class for preset definitions
├── preset_manager.py    # Preset loading and management
├── requirements.txt     # Python dependencies
├── presets/
│   ├── static/          # Static image presets
│   │   ├── dashes.py
│   │   ├── glowing_ends_center.py
│   │   ├── gradient2.py
│   │   └── static_color.py
│   └── animation/       # Animation presets
│       ├── bouncing_dot.py
│       ├── pulse.py
│       ├── rainbow.py
│       ├── smooth_transition.py
│       └── wipe.py
└── README.md
```

## Creating Custom Presets

To create a new preset:

1. Create a new Python file in either `presets/static/` or `presets/animation/`
2. Import and subclass `Preset` from `preset_base`
3. Define the `name`, `mode`, and `params` attributes
4. Implement the `generate()` method to return a NumPy array of shape `(Height, Width, 3)` representing RGB values

Example (static color preset):
```python
import numpy as np
from preset_base import Preset

class StaticColor(Preset):
    name = "Static Color"
    mode = "image"  # or "animation"
    params = [
        # Color (user input)
        {
            "name": "Color",  # Displayed field name
            "key": "color", # Attribute name in kwargs
            "type": "color", # Input field type
            "default": (204, 204, 204)  # default value
        }
    ]

    def generate(self, kwargs):
        # Create an empty array 
        img_array = np.zeros((32, 2, 3), dtype=np.uint8)

        # Fill it with selected color
        img_array[:, :] = np.array(kwargs["color"])
        
        return img_array
```

## Contribution

Feel free to fork the project, add your improvements and make new presets.
I'll be happy to review pull requests!


## License

This project is provided as-is.
