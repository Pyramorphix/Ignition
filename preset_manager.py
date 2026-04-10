import importlib
import pkgutil

from preset_base import Preset
import presets  # Imports the folder

def load_presets():
    """Loads all the presets from 'presets/' directory and returns them as list"""
    # Look through 'presets/' and all its subdirectories
    for _, module_name, is_package in pkgutil.walk_packages(path=presets.__path__,
                                                            prefix=presets.__name__ + "."):
        if not is_package:
            # Import preset (Preset subclass)
            importlib.import_module(module_name)

    # Grab all loaded subclasses
    loaded_presets = [cls() for cls in Preset.__subclasses__()]

    # Sort them alphabetically by name
    loaded_presets.sort(key=lambda x: x.name)

    return loaded_presets

