from PIL import Image
import numpy as np

img = Image.open("xyz.png").convert("RGB")
img = img.resize((500, 500))  # arbitrary size
img_np = np.array(img)

print(img_np.shape)
