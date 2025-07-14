from moviepy.editor import ImageClip
from PIL import Image
import numpy as np

# Load the background image
img = Image.open("xyz.png").convert("RGB")
img = img.resize((500, 500))  # arbitrary size
img_np = np.array(img)

# Create ImageClip and export as video
clip = ImageClip(img_np).set_duration(3)
clip.write_videofile("bg_only.mp4", codec="libx264", fps=24)
