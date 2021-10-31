# Fractal_Image_Generator

Sometimes you may want your wallpapers/backgrounds to be different from others. Fractal images can satisfy this need. Although generating fractal images is generally simple, adjusting the parameters to make an image look harmonious may not be easy. Here this repository provides (is going to provide...) some examples of generating such images. If you like these styles, you may use these codes (directly, or as a starting point) to generate your own image.

## Newton Fractal (Dark wallpaper)
See newton_wallpaper.py

This code uses opencv-python and numpy. It may run about 20min to generate a wallpaper (this time may vary if you change the parameters e.g. wallpaper shape in the code).

This code generates 10 images and calculate the average of them to generate a wallpaper. Each image is generated with Newton fractal from 10 randomly generated complex points. The color is set to dirtribute evenly in the range of [0, 0.3]. The default shape of the images is 1920x1080.

Below is an example:

![example image](./newton_example.png)
