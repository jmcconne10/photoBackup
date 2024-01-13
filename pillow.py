#this is a simple example of opening an image

from PIL import Image

# Open an image file
image_path = "/Volumes/Video/Google Takeout/TakeoutLatest/Google Photos/Photos from 2019/IMG_4002.HEIC"
img = Image.open(image_path)

# Display basic information about the image
print("Image format:", img.format)
print("Image size:", img.size)

# Show the image
img.show()