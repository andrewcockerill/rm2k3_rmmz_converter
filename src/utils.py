# Packages
import numpy as np
import pandas as pd
import cv2
from PIL import Image

# Class


class SpriteConverter:
    """Converts a standard RPG Maker 2003 player sprite sheet into an RMMZ format by repositioning
    sprite locations to match the layout expected by MZ. Nearest neighbor scaling can also be
    performed along with the matching of background color to a transparent alpha channel.

    Attributes
    ----------

    loc : str
        When set, the location of the source image in PNG format

    image : array
        Numpy array of the input image after ingested via Pillow

    Methods
    -------

    set_image(loc):
        Sets image based on path provided by `loc`

    reset_image():
        Resets image to that stored in original directory

    get_dims():
        Returns the y, x dimensions of the image as a tuple

    scale(scale_factor):
        Performs nearest neighbor scaling on the image (must be a factor >=1). Factor will be cast as
        an integer

    reposition_rm2k_to_mz():
        Peforms rearrangement of sprite sheet from RM2K format to RMMZ format

    remove_bg():
        Samples the background color in the top left most pixel and sets this color to be
        transparent

    show_image():
        Displays image from console

    save_image(loc):
        Saves image to `loc`

    """

    def __init__(self, loc=None):
        if loc is not None:
            self.set_image(loc)

    def set_image(self, loc):
        self.loc = loc
        img = Image.open(loc)
        arr_img = np.asarray(img)
        self.image = arr_img
        return self

    def reset_image(self):
        self.set_image(self.loc)
        return self

    def get_dims(self):
        return self.image.shape[0], self.image.shape[1]

    def scale(self, scale_factor=1):
        assert scale_factor >= 1, "scale factor must be greater than 1"
        scale_factor = int(scale_factor)
        if scale_factor == 1:
            return self
        else:
            y_size, x_size = tuple(
                map(lambda x: x*scale_factor, self.get_dims()))
            self.image = cv2.resize(
                self.image, (x_size, y_size), interpolation=cv2.INTER_NEAREST)
            return self

    def show_image(self):
        Image.fromarray(self.image).show()

    def reposition_rm2k_to_mz(self):
        img = self.image.copy()
        vert_px, _ = self.get_dims()

        # Partition the 8 rows of sprites
        vert_chunks = [i for i in range(0, vert_px, int(vert_px/8))]+[vert_px]

        # These are the dimensions of each row as a list of tuples (y, x)
        row_dims = [(vert_chunks[i], vert_chunks[i+1]-1)
                    for i in range(len(vert_chunks)-1)]

        # Assign each row a number 0-7 in a dict format row_number:(y, x)
        assignment_dict = {k: v for k, v in enumerate(row_dims)}

        # Remapping
        mappings = [(0, 3), (1, 2), (2, 0), (3, 1),
                    (4, 7), (5, 6), (6, 4), (7, 5)]

        output_dict = {w[1]: assignment_dict[w[0]] for w in mappings}

        output_list = [output_dict[key] for key in sorted(output_dict.keys())]

        self.image = np.concatenate(
            [img[i[0]:i[1]+1, :, :] for i in output_list])
        return self

    def remove_bg(self, tol=0):
        img = self.image[:, :, 0:3].copy()
        color_0, color_1, color_2 = (img[0, 0, 0], img[0, 0, 1], img[0, 0, 2])
        alpha_layer = (255-np.multiply(
            np.multiply(
                np.logical_and(img[:, :, 0] <= color_0 + tol,
                               img[:, :, 0] >= color_0 - tol),
                np.logical_and(img[:, :, 1] <= color_1 + tol, img[:, :, 1] >= color_1 - tol)),
            np.logical_and(img[:, :, 2] <= color_2 + tol, img[:, :, 2] >= color_2 - tol))*255).astype('uint8')
        self.image = np.append(img, alpha_layer.reshape(
            alpha_layer.shape[0], alpha_layer.shape[1], 1), 2)
        return self

    def save_image(self, loc):
        pil_img = Image.fromarray(self.image)
        pil_img.save(loc)
