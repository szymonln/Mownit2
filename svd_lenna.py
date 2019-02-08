import numpy.linalg as la
import numpy as np
from skimage import data, io
from skimage.color import rgb2gray
from skimage import img_as_ubyte, img_as_float
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt

"""
    Image compression using svd decomposition
"""


def compress(original_image, img, k): # k like kuality
    U, s, V = la.svd(img, full_matrices=False)

    axcolor = 'lightgoldenrodyellow'
    axqual = plt.axes( facecolor=axcolor)

    #quality = Slider(axqual, "Quality", 1, 512, valinit=256)
    reconst_matrix = np.dot(U[:, :k], np.dot(np.diag(s[:k]), V[:k, :]))

    def update(k):
        k = int(k)
        reconst_matrix = np.dot(U[:, :k], np.dot(np.diag(s[:k]),V[:k,:]))
        image_reconst = reconst_matrix.reshape(original_shape)
        axarr[0].imshow((image_reconst * 255).astype(np.uint8))
        plt.show()




    image_reconst = reconst_matrix.reshape(original_shape)
    f, axarr = plt.subplots(1, 2)
    f.suptitle("SVD Image Compression")
    axarr[0].imshow((image_reconst*255).astype(np.uint8))
    axarr[0].set_title("Compressed")
    axarr[1].imshow(original_image)
    axarr[1].set_title("Original")
    quality = Slider(axqual, "Quality", 1, 256, valinit=100)
    quality.on_changed(update)
    plt.show()



#if __name__ == "__main__":
image = img_as_float(io.imread("lena.jpg"))
original_shape = image.shape
reshaped_img = image.reshape(original_shape[0], original_shape[1] * 3)
print(reshaped_img.shape)

compress(image, reshaped_img, 20)