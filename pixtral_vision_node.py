import requests
import base64
import io
from PIL import Image
import torch
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComfyUIPixtralVision:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Describe the image"}),
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": "Enter your Mistral API key here"}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.5, "step": 0.1})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "ComfyUI/Pixtral Vision"

    def process(self, prompt, image, api_key, temperature):
        try:
            logger.info(f"Processing image. Type: {type(image)}, Shape: {getattr(image, 'shape', 'No shape')}")
            
            # Convert PyTorch tensor to a NumPy array
            if isinstance(image, torch.Tensor):
                image = image.squeeze().cpu().numpy()
            
            # Ensure the image is in the correct format (HWC)
            if len(image.shape) == 3 and image.shape[0] in [1, 3, 4]:  # CHW format
                image = image.transpose(1, 2, 0)
            
            # Handle different color channels
            if len(image.shape) == 2:  # Grayscale image
                pil_image = Image.fromarray((image * 255).astype('uint8'), 'L')
            elif len(image.shape) == 3:
                if image.shape[2] == 1:  # Grayscale with extra channel
                    pil_image = Image.fromarray((image[:, :, 0] * 255).astype('uint8'), 'L')
                elif image.shape[2] == 3:  # RGB
                    pil_image = Image.fromarray((image * 255).astype('uint8'), 'RGB')
                elif image.shape[2] == 4:  # RGBA
                    pil_image = Image.fromarray((image * 255).astype('uint8'), 'RGBA').convert('RGB')
                else:
                    raise ValueError(f"Unexpected number of channels: {image.shape[2]}")
            else:
                raise ValueError(f"Unexpected image shape: {image.shape}")
            
            logger.info(f"Processed PIL Image size: {pil_image.size}")
            
            # Convert PIL image to base64
            buffered = io.BytesIO()
            pil_image.save(buffered, format="JPEG")
            base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            # Prepare the request to Mistral API
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
                    ]
                }
            ]
            data = {
                "model": "pixtral-12b-2409",
                "messages": messages,
                "temperature": temperature
            }

            logger.info("Sending request to Mistral API")
            response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                logger.info("Received successful response from Mistral API")
                return (result["choices"][0]["message"]["content"],)
            else:
                error_message = f"API Error: {response.status_code}, {response.text}"
                logger.error(error_message)
                return (error_message,)
        
        except Exception as e:
            error_message = f"Error in process method: {str(e)}"
            logger.exception(error_message)
            return (error_message,)

# Register the node in ComfyUI
NODE_CLASS_MAPPINGS = {
    "ComfyUIPixtralVision": ComfyUIPixtralVision,
}