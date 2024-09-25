from .pixtral_vision_node import ComfyUIPixtralVision, MultiImagesInput  # Import both classes

# Define the node mappings to register the custom nodes in ComfyUI
NODE_CLASS_MAPPINGS = {
    "ComfyUIPixtralVision": ComfyUIPixtralVision,
    "MultiImagesInput": MultiImagesInput,  # Register MultiImagesInput
}

# Optional: Define how the nodes should be displayed in the UI
NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUIPixtralVision": "Pixtral Vision Analysis",
    "MultiImagesInput": "Multi Images Input",  # Display name for MultiImagesInput
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']