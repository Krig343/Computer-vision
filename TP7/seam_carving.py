import sys
import numpy as np
import cv2 as cv
from scipy.ndimage.filters import convolve
from skimage import filters, color


# Calculer l'énergie de chaque pixel
def energy(img):
    x_filter = np.array([
        [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])
    x_filter = np.stack([x_filter] * 3, axis=2)

    y_filter = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])
    y_filter = np.stack([y_filter] * 3, axis=2)

    img = img.astype('float32')
    convolved = np.absolute(convolve(img, x_filter)) + \
        np.absolute(convolve(img, y_filter))

    energy_map = convolved.sum(axis=2)

    return energy_map


# Calculer la liste de chemin à éliminer
def minimum_energy(img):
    size = img.shape
    energy_map = energy(img)

    suppresed = np.zeros_like(energy_map, dtype=np.int)

    for i in range(1, size[0]):
        for j in range(0, size[1]):
            if j == 0:
                index = np.argmin(energy_map[i-1, 0:2])
                suppresed[i, j] = index
                min_energy = energy_map[i-1, index]
            else:
                index = np.argmin(energy_map[i - 1, j - 1:j + 2])
                suppresed[i, j] = index + j - 1
                min_energy = energy_map[i - 1, index + j - 1]

            energy_map[i, j] += min_energy

    return energy_map, suppresed


# Elimine le chemin de poids le plus faible
def remove_min_track(img):
    size = img.shape

    energy_map, suppresed = minimum_energy(img)
    mask = np.ones(size[0:2], dtype=np.bool)

    j = np.argmin(energy_map[-1])
    for i in reversed(range(size[0])):
        mask[i, j] = False
        j = suppresed[i, j]

    mask = np.stack([mask] * 3, axis=2)
    img = img[mask].reshape((size[0], size[1] - 1, 3))
    return img


# Elimine les chemins de poids les plus faible tant que l'image n'a pas la bonne taille
def remove(img, scale):
    size = img.shape
    new_col_nb = int(scale * size[1])

    for i in range(size[1] - new_col_nb):
        img = remove_min_track(img)

    return img


scale = float(sys.argv[2])

# Choisir l'image
img = cv.imread(sys.argv[1])

out = remove(img, scale)

res = np.concatenate((img, out), axis=1)

cv.imshow('seam', res)
cv.waitKey(0)
cv.destroyAllWindows()
