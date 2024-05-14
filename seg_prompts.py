import numpy as np
import torch
import matplotlib
matplotlib.use("TkAgg") # 不能与下一行交换顺序
import matplotlib.pyplot as plt
import cv2
from PIL import Image


from segment_anything import sam_model_registry, SamPredictor

def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
    
def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   
    
def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))    

  
sam_checkpoint = "weights/sam_vit_h_4b8939.pth"
model_type = "vit_h"
device = "cuda"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
predictor = SamPredictor(sam)

input_box = np.array([1050, 57, 2785, 3921])
# input_point = None
# input_label = None
input_point = np.array([[1625, 773],[2513,1145],[565,957]])
input_label = np.array([0, 1, 1])
input_fname = "DJI_20231205115622_0615_D.JPG"
image = cv2.imread(f'data/{input_fname}')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # h,w,c uint8
  
predictor.set_image(image)
masks, _, _ = predictor.predict(
    # point_coords=input_point,
    # point_labels=input_label,
    box=input_box[None, :],
    multimask_output=False,
) # masks[0] h,w bool

# masked_image = image.copy()
# masked_image[np.logical_not(masks[0])] = 255
# masked_image = cv2.cvtColor(masked_image, cv2.COLOR_RGB2BGR)
# cv2.imwrite(f"output/{input_fname}", masked_image)

# numerical_mask = masks[0].astype(np.uint8)*255
# cv2.imwrite(f"data/building/masks/{input_fname}.png", numerical_mask)

plt.figure(figsize=(10, 10))
plt.imshow(image)
show_mask(masks[0], plt.gca())
show_box(input_box, plt.gca())
plt.axis('off')
plt.show()

####################
alpha = masks[0].astype(np.uint8)*255
alpha = alpha[:,:,np.newaxis]
rgba = np.concatenate([image.copy(), alpha], axis=-1)
# print(f"alpha:{alpha.shape}")
# print(f"rgba:{rgba.shape}")
rgba = Image.fromarray(rgba, 'RGBA')
rgba.save(f"output/{input_fname.replace('JPG','png')}")
print(rgba)

  