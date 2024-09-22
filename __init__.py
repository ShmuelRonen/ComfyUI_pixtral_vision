from .pixtral_vision_node import ComfyUIPixtralVision  # Import the node class

# Define the node mappings to register the custom node in ComfyUI
NODE_CLASS_MAPPINGS = {
    "ComfyUIPixtralVision": ComfyUIPixtralVision,
}

# Optional: Define how the node should be displayed in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUIPixtralVision": "Pixtral Vision Analysis",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
