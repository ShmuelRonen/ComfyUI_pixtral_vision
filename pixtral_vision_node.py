import requests
import base64
import io
from PIL import Image
import torch
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiImagesInput:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 2, "max": 1000, "step": 1}),
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "combine"
    CATEGORY = "ComfyUI/Pixtral Vision"

    def combine(self, inputcount, **kwargs):
        from nodes import ImageBatch  # Make sure 'nodes' is accessible

        image_batch_node = ImageBatch()
        image = kwargs["image_1"]
        for c in range(1, inputcount):
            new_image = kwargs[f"image_{c + 1}"]
            (image,) = image_batch_node.batch(image, new_image)
        return (image,)


class ComfyUIPixtralVision:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Describe the image"}),
                "images": ("IMAGE", {"multiple": True}),
                "api_key": ("STRING", {"default": "Enter your Mistral API key here"}),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.5, "step": 0.1})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "process"
    CATEGORY = "ComfyUI/Pixtral Vision"

    def process(self, prompt, images, api_key, temperature):
        try:
            image_urls = []
            for image in images:
                logger.info(f"Processing image. Type: {type(image)}, Shape: {getattr(image, 'shape', 'No shape')}")

                if isinstance(image, torch.Tensor):
                    image = image.squeeze().cpu().numpy()

                if len(image.shape) == 3 and image.shape[0] in [1, 3, 4]:
                    image = image.transpose(1, 2, 0)

                if len(image.shape) == 2:
                    pil_image = Image.fromarray((image * 255).astype('uint8'), 'L')
                elif len(image.shape) == 3:
                    if image.shape[2] == 1:
                        pil_image = Image.fromarray((image[:, :, 0] * 255).astype('uint8'), 'L')
                    elif image.shape[2] == 3:
                        pil_image = Image.fromarray((image * 255).astype('uint8'), 'RGB')
                    elif image.shape[2] == 4:
                        pil_image = Image.fromarray((image * 255).astype('uint8'), 'RGBA').convert('RGB')
                    else:
                        raise ValueError(f"Unexpected number of channels: {image.shape[2]}")
                else:
                    raise ValueError(f"Unexpected image shape: {image.shape}")

                logger.info(f"Processed PIL Image size: {pil_image.size}")

                buffered = io.BytesIO()
                pil_image.save(buffered, format="JPEG")
                base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
                image_urls.append(f"data:image/jpeg;base64,{base64_image}")


            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            content_list = [{"type": "text", "text": prompt}]
            for image_url in image_urls:
                content_list.append({"type": "image_url", "image_url": image_url})

            messages = [
                {
                    "role": "user",
                    "content": content_list
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


NODE_CLASS_MAPPINGS = {
    "ComfyUIPixtralVision": ComfyUIPixtralVision,
    "MultiImagesInput": MultiImagesInput,
}