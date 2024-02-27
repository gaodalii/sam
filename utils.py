from functools import wraps

import numpy as np
import gradio as gr
import cv2
import torch

from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

sam_checkpoint = "weights/sam_vit_h_4b8939.pth"
model_type = "vit_h"
device = "cuda"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
mask_generator = SamAutomaticMaskGenerator(sam)    

def resize_image(img, max_size):
    """
    Resize the image using OpenCV to ensure that its dimensions do not exceed the specified maximum size,
    while maintaining the aspect ratio.

    Parameters:
    - image_path: str, the path to the input image file.
    - max_size: int, the maximum size of the image's width or height.

    Returns:
    - A numpy array of the resized image if resizing was necessary, otherwise the original image.
    """
    # Get the current height and width of the image
    original_height, original_width = img.shape[:2]

    # Determine the aspect ratio
    aspect_ratio = original_width / original_height

    # Check if the image exceeds the maximum size
    if original_width > max_size or original_height > max_size:
        # Determine the new dimensions
        if aspect_ratio > 1:
            # Image is wider than it is tall
            new_width = max_size
            new_height = int(max_size / aspect_ratio)
        else:
            # Image is taller than it is wide
            new_height = max_size
            new_width = int(max_size * aspect_ratio)

        # Resize the image
        resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

        return resized_img

    # If the image is within the size limit, return the original image
    return img

def custom_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with torch.inference_mode():            
                return func(*args, **kwargs)
        except Exception as e:
            raise gr.Error(repr(e))            
    return wrapper    
         
@custom_wrapper    
def seg_everything(input_image):
    input_image = resize_image(input_image, 1920)
    masks = mask_generator.generate(input_image)
    mask_image = np.zeros_like(input_image)
    cv2.imwrite("tmp.png", mask_image)        
    anns = masks
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)    
    for ann in sorted_anns:
        m = ann['segmentation']
        color_mask = np.random.randint(0, 255, size=(3,), dtype=np.uint8) 
        mask_image[m] = color_mask      
    alpha = 0.5
    mask_image = cv2.addWeighted(mask_image, alpha, input_image, 1-alpha, 0)
    return mask_image     

def seg_with_prompts(prompts):
    print(prompts["points"])
        
     
    