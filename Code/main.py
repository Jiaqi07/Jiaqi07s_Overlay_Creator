from PIL import Image

def main():
    try:
        # Relative Path
        img = Image.open("picture.jpg")
        width, height = img.size

        area = (0, 0, width / 2, height / 2)
        img = img.crop(area)

        # Saved in the same relative location
        img.save("cropped_picture.jpg")

    except IOError:
        pass


if __name__ == "__main__":
    main()