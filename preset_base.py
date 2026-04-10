class Preset:
    """Base class for all presets."""
    name = "Base Preset"
    mode = "image"  # 'image' or 'animation'
    params = [] 

    def generate(self, kwargs):
        """Must return a NumPy array of shape (Height, Width, 3) representing RGB."""
        raise NotImplementedError
