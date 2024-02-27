from functools import wraps

import numpy as np
import gradio as gr
import cv2

from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

sam_checkpoint = "weights/sam_vit_h_4b8939.pth"
model_type = "vit_h"
device = "cuda"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
mask_generator = SamAutomaticMaskGenerator(sam)    

def report_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise gr.Error(repr(e))            
    return wrapper    
         
@report_error    
def seg_everything(input_image):
    masks = mask_generator.generate(input_image)
    mask_image = np.zeros_like(input_image)
    cv2.imwrite("tmp.png", mask_image)        
    anns = masks
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)    
    for ann in sorted_anns:
        m = ann['segmentation']
        color_mask = np.random.randint(0, 255, size=(3,), dtype=np.uint8) 
        mask_image[m] = color_mask      
    return mask_image     
     
    