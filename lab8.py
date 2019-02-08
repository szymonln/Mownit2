from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


""" Zad 1.
    Korzystając z własności domeny częstotliwościowej odfiltruję składowe
    o wysokiej częstotliwości w celu odszumienia obrazu.
"""

image1 = Image.open("lenna_noise.jpg")
array1 = np.asarray(image1)
array_fft = np.fft.fft2(array1)

# Filtruję składowe o wysokiej energii

keep_fraction = 0.2

im_fft2 = array_fft.copy()

r, c = im_fft2.shapegit

im_fft2[int(r*keep_fraction):int(r*(1-keep_fraction))] = 0

im_fft2[:, int(c*keep_fraction):int(c*(1-keep_fraction))] = 0

final_img = np.fft.ifft2(im_fft2)
final_img = np.abs(final_img)


plt.subplot(131), plt.imshow(array1, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(132), plt.imshow(final_img, cmap='gray')
plt.title('Image after denoising'), plt.xticks([]), plt.yticks([])


""" Zad 2.
    Zastosuję tablice kwantyzacji w celu kompresji obrazu jpeg.
"""

i = 0
j = 0
for j in range(512):
    for i in range(512):
        """ Stosuję ideę tablic kwantyzacji realizując odszumianie obrazu podczas kompresji,
            współczynniki odpowiadające największym częstotliwościom ustawiam na
            wartości najbliższe 100, analogicznie współczynniki odpowiadające niskim częstotliwościom
            mają niskie wartości aby zachować najbardziej znaczące informacje.

            Współczynniki te obliczam w locie linijkę niżej.
        """
        im_fft2[j][i] /= (i/512.0 * 40 + j/512.0 * 40 + 10)

final_img_comp = np.abs(np.fft.ifft2(im_fft2))

plt.subplot(133), plt.imshow(final_img_comp, cmap='gray')
plt.title('Image after compression'), plt.xticks([]), plt.yticks([])

plt.show()

