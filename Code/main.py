import numpy as np
from PIL import Image, ImageOps, ImageFilter
from colorthief import ColorThief

DEFAULT_IMG = Image.open('images/Default.jpg')  # Any Size just plug into Cube The Square (Future replicate it)
# Default Images - 2048x2048 each image
DEFAULT_BACK = Image.open('images/Default_Back.bmp')  # Directly
DEFAULT_BOTTOM = Image.open('images/Default_Bottom.bmp')
DEFAULT_FRONT = Image.open('images/Default_Front.bmp')
DEFAULT_LEFT = Image.open('images/Default_Left.bmp')  # Directly
DEFAULT_RIGHT = Image.open('images/Default_Right.bmp')  # Directly
DEFAULT_TOP = Image.open('images/Default_Top.bmp')

STARFIELD031 = Image.open('images/starfield031.png')
TRANSITIONOVERLAY = Image.open('images/TransitionOverlay.png')
color_thief = ColorThief('images/Default.jpg')
dominant_color = color_thief.get_color(quality=1)

def show(file_image):
    file_image.show()


def smooth(file_image):
    return file_image.filter(ImageFilter.SMOOTH)


def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


def get_file():
    # Read image file path from user, or use the default file
    file_image = input('Enter image file (or press enter for default): ')
    if file_image == '':
        file_image = DEFAULT_IMG
    else: 
        file_image = DEFAULT_IMG

    print("")
    return file_image


def start_overlay():
    # Easy stuff
    Sky = STARFIELD031.copy()
    Sky.paste(DEFAULT_LEFT, (0, 2048))
    Sky.paste(DEFAULT_RIGHT, (4096, 2048))
    Sky.paste(DEFAULT_BACK, (4096, 0))

    # Harder stuff
    Transition = TRANSITIONOVERLAY.copy()
    Transition.paste(DEFAULT_TOP, (0, 0))
    Transition.paste(DEFAULT_FRONT, (0, 2048))
    Transition.paste(DEFAULT_BOTTOM, (0, 4096))

    print(Transition.size)

    npPic = np.array(Transition)

    for i in range(0, 6144):
        for j in range(1020, 1028):
            if npPic[i][j][0] > 250 and npPic[i][j][1] > 250 and npPic[i][j][2] > 250:
                npPic[i][j][0] = dominant_color[0]
                npPic[i][j][1] = dominant_color[1]
                npPic[i][j][2] = dominant_color[2]

    pil_image = Image.fromarray(npPic)
    # pil_image.show()

    Transition = pil_image.filter(ImageFilter.GaussianBlur())

    # TransCrop = Transition.copy().crop((512, 512, 1024, 6144))
    # TransInvert = ImageOps.mirror(TransCrop)
    # Transition.paste(TransInvert, (1024, 0))

    # 1. Crop image to half - Yes
    # 2. Create horizontal inversion - Yes
    # 3. Paste - Yes
    # 4. Blend Middle (Gaussian Blur) - Not Finished

    Sky.paste(Transition.copy().crop((0, 0, 2048, 2048)), (2048, 0))
    Sky.paste(Transition.copy().crop((0, 2048, 2048, 4096)), (2048, 2048))
    Sky.paste(Transition.copy().crop((0, 4096, 2048, 6144)), (0, 0))

    Sky.save('out\starfield031.png')


if __name__ == '__main__':
    file_image = get_file()

    while True:
        ans = input('What would you like to do? (or press enter to exit): ')
        if ans == "":
            break
        elif ans.lower() == 'show':
            show(file_image)
        elif ans.lower() == 'help':
            print("Show, Convert, Help")
        elif ans.lower() == 'convert':
            start_overlay()
        else:
            print("That isn't a command, help for a list of commands.")
        print()
        print()
