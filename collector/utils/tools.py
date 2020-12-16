import random
import string
from PIL import Image
from PIL import ExifTags
from io import BytesIO

def random_name_generator(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))


def ratate_image(image):
    """
    이미지 저장 시 회전되는 문제를 해결하기 위해 사용합니다.
    """
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    exif = dict(image._getexif().items())

    if orientation in exif:

        if exif[orientation] == 8:
            image = image.rotate(-90, expand=True)
        elif exif[orientation] == 1:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 3:
            image = image.rotate(-90, expand=True)

    return image
