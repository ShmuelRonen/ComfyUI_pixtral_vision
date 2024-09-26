from .pixtral_vision_node import ComfyUIPixtralVision, MultiImagesInput

NODE_CLASS_MAPPINGS = {
    "ComfyUIPixtralVision": ComfyUIPixtralVision,
    "MultiImagesInput": MultiImagesInput,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUIPixtralVision": "Pixtral Vision Analysis",
    "MultiImagesInput": "Multi Images Input",
}

WEB_DIRECTORY = "web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']