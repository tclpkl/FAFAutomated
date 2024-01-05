import matplotlib
import matplotlib.pyplot as plt
from matplotlib import image
from scipy.ndimage import gaussian_filter
from skimage import img_as_float
from skimage.morphology import reconstruction
from PIL import Image
import numpy as np
import os
import sys

class FAF:
    def __init__(self, img_as_numpy_array):
        self.original_image = img_as_numpy_array
        # Converts image to float and applies gaussian filter
        self.float_gaussian = gaussian_filter(img_as_float(img_as_numpy_array), 1)

    def processPhoto(self):
        tiles = self.__splitPhotosAndProcess()

        # Keeping track of proportion of black pixels
        total_pixels = 0.0
        black_pixels = 0.0

        # Recombining photo
        combined = [[None for a in range(768)] for b in range(768)]

        for tile in tiles:
            x_range = tile[1][0]
            y_range = tile[1][1]
            processed = tile[0]

            for i in range(x_range[0], x_range[1] + 1):
                for j in range(y_range[0], y_range[1] + 1):
                    combined[i][j] = processed[i - x_range[0]][j - y_range[0]]
        for i in range(768):
            for j in range(768):
                if (self.float_gaussian[i][j] == 0).all():
                    combined[i][j] = [0, 0, 0.5451]
                else:
                    total_pixels += 1.0
                    if (combined[i][j] == 0).all():
                        black_pixels += 1.0
                # Making grids
                red = [96, 672, 288, 480]
                if (i % 96 == 0 and (j < 97 or j > 671)) or (j % 96 == 0 and (i < 97 or i > 671)):
                    combined[i][j] = [100, 0, 0]
                if i in red or j in red:
                    combined[i][j] = [100, 0, 0]
                if ((i - 96) % 192 == 0 and (j < 289 or j > 479)) or ((j - 96) % 192 == 0 and (i < 289 or i > 479)):
                    combined[i][j] = [100, 0, 0]
        combined = np.array(combined)
        combined = Image.fromarray((combined * 255).astype(np.uint8))
        combined = img_as_float(combined)
        black_percentage = black_pixels / total_pixels
        return combined, black_percentage

    # Private method to split image into 16 sections stored in image array
    def __splitPhotosAndProcess(self):
        im = self.float_gaussian
        tiles = [((0, 95), (0, 95)), ((0, 95), (96, 191)), ((0, 95), (192, 287)), ((0, 95), (288, 383)),
                 ((0, 95), (384, 479)), ((0, 95), (480, 575)), ((0, 95), (576, 671)), ((0, 95), (672, 767)),
                 ((96, 191), (0, 95)), ((96, 287), (96, 287)), ((96, 287), (288, 479)), ((96, 287), (480, 671)),
                 ((96, 191), (671, 767)), ((192, 287), (0, 95)), ((192, 287), (671, 767)), ((288, 383), (0, 95)),
                 ((288, 479), (96, 287)), ((288, 479), (288, 479)), ((288, 479), (480, 671)), ((288, 383), (671, 767)),
                 ((384, 479), (0, 95)), ((384, 479), (671, 767)), ((480, 575), (0, 95)), ((480, 671), (96, 287)),
                 ((480, 671), (288, 479)), ((480, 671), (480, 671)), ((480, 575), (671, 767)), ((576, 671), (0, 95)),
                 ((576, 671), (671, 767)), ((672, 767), (0, 95)), ((672, 767), (96, 191)), ((672, 767), (192, 287)),
                 ((672, 767), (288, 383)), ((672, 767), (384, 479)), ((672, 767), (480, 575)), ((672, 767), (576, 671)),
                 ((672, 767), (671, 767))]
        processed = []

        count = 0
        for tile in tiles:
            x_range = tile[0]
            y_range = tile[1]
            to_process = [[None for j in range(y_range[1] - y_range[0] + 1)] for i in
                          range(x_range[1] - x_range[0] + 1)]
            for i in range(x_range[1] - x_range[0] + 1):
                for j in range(y_range[1] - y_range[0] + 1):
                    to_process[i][j] = im[i + (x_range[0])][j + (y_range[0])]
            to_process = np.array(to_process)
            p = None
            if tile == ((288, 479), (288, 479)):
                p = self.__process_subsection(to_process, h_threshold=0.1)
            elif x_range[1] - x_range[0] == 191:
                p = self.__process_subsection(to_process, h_threshold=0.5)
            else:
                p = self.__process_subsection(to_process, h_threshold=0.6)
            processed.append((p, tile))
        return processed

    # Private method to process sub-photo
    def __process_subsection(self, img, h_threshold=0):
        seed = img - h_threshold
        mask = img
        dilated = reconstruction(seed, mask, method='dilation')
        hdome = img - dilated

        # Loop through all pixels, and replace those that are not strict white or black with white
        for x in range(hdome.shape[0]):
            for y in range(hdome.shape[1]):
                if (hdome[x, y] != 0).all() and (hdome[x, y] != 1).all():
                    hdome[x, y] = [1, 1, 1]
        return hdome


def process_FAF(input_filepath, output_filepath):

    # Getting file name, converting to image and making FAF object
    filename = (input_filepath.split("/")[-1]).split(".")[0]
    img = image.imread(input_filepath)
    faf = FAF(img)
    
    # Processing photo 
    print("**BEFORE PROCESSING")
    print("Input filepath:", input_filepath)
    combined, black_percentage = faf.processPhoto()
    print("\n**AFTER PROCESSING")
    print("Output filepath:", output_filepath)

    # Making output image of original on left, processed on right, and title + proportion deteriorated
    matplotlib.use('agg')
    f, axarr = plt.subplots(1, 2)
    axarr[0].imshow(faf.original_image)
    axarr[1].imshow(combined)
    plt.title("(" + filename + ") Fraction Black " + str(int(black_percentage * 10000) / 10000))

    # Saving to output filepath
    plt.savefig(output_filepath)

    return black_percentage
