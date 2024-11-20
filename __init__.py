from .pixtral_vision_node import ComfyUIPixtralVision, MultiImagesInput, preview_text

NODE_CLASS_MAPPINGS = {
    "ComfyUIPixtralVision": ComfyUIPixtralVision,
    "MultiImagesInput": MultiImagesInput,
    "preview_text": preview_text,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ComfyUIPixtralVision": "Pixtral Vision Analysis",
    "MultiImagesInput": "Multi Images Input",
    "preview_text": "Preview Text",
}

WEB_DIRECTORY = "web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
