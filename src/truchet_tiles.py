import os

import PIL
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon


def generate_truchet_tiles(image: PIL.Image, length):
    width, height = image.size
    mat_w = int(width / length)
    mat_h = int(height / length)
    mat = np.empty((mat_w, mat_h))

    for i, w in enumerate(range(0, mat_w * length, length)):
        for j, h in enumerate(range(0, mat_h * length, length)):
            grey = cal_greyscale(image, w, h, length)
            mat[i][mat_h - j - 1] = grey
    return mat


def convert_grey_to_center(mat):
    width, height = mat.shape
    centers = np.empty(mat.shape)
    for i in range(width):
        for j in range(height):
            unit_grey = mat[i][j] / 255
            if unit_grey <= 0.25:
                temp = 0
            elif unit_grey >= 0.75:
                temp = 1
            else:
                temp = 2 * unit_grey - 0.5
            centers[i][j] = 0.25 + 0.5 * (1 - temp)
    return centers


def cal_greyscale(image, w_start, h_start, step):
    sum_grey = 0
    # count = 0
    for w in range(w_start, w_start + step):
        for h in range(h_start, h_start + step):
            g = image.getpixel((w, h))
            sum_grey += g
            # count += 1
    return sum_grey / step / step


def gen_truchet_polygon(center, pattern, x_shift, y_shift, length):
    if pattern == 'A':
        polygon = [[0, 0], [0, length], [center * length, center * length],
                   [length, 0], [0, 0]]
    elif pattern == 'B':
        polygon = [[0, 0], [0, length], [length, length],
                   [center * length, (1 - center) * length], [0, 0]]
    elif pattern == 'C':
        polygon = [[length, length], [0, length],
                   [(1 - center) * length, (1 - center) * length], [length, 0],
                   [length, length]]
    elif pattern == 'D':
        polygon = [[0, 0], [(1 - center) * length, center * length],
                   [length, length], [length, 0], [0, 0]]
    else:
        raise ValueError('Invalid pattern: {}'.format(pattern))
    polygon = [[point[0] + x_shift, point[1] + y_shift] for point in polygon]
    return polygon


def draw_truchet_tiles(centers, length, file_name):
    width, height = centers.shape
    polygons = []
    for i in range(width):
        for j in range(height):
            if (i + j) % 2 == 0:
                pattern = 'A'
            else:
                pattern = 'C'
            polygons.append(
                gen_truchet_polygon(centers[i][j], pattern, i * length,
                                    j * length, length))

    _draw_plot(polygons, file_name, (width + 1) * length,
               (height + 1) * length)


def _draw_plot(polygons, file_name, width, height):
    fig, ax = plt.subplots()
    # patches = []
    # for polygon in polygons:
    #     poly = Polygon(polygon, True)
    #     patches.append(poly)
    patches = [Polygon(polygon, True) for polygon in polygons]
    p = PatchCollection(patches,
                        facecolors='k',
                        edgecolors='k',
                        linewidths=0.1)
    ax.add_collection(p)
    ax.set_xlim([0, width])
    ax.set_ylim([0, height])
    ax.axis('equal')
    # fig.tight_layout()
    # plt.axis('off')
    ax.set_axis_off()
    plt.margins(-0.49, 0)
    # plt.show()
    plt.savefig('{}.jpg'.format(file_name), bbox_inches='tight', pad_inches=0)
    plt.savefig('{}.pdf'.format(file_name), bbox_inches='tight', pad_inches=0)
    return


def read_image(file_name):
    return PIL.Image.open(file_name)


def main():
    length = 2
    file = os.path.join(os.pardir, 'data', 'input', 'pearl_wb.jpg')
    out_file = os.path.join(os.pardir, 'data', 'output',
                            'pearl_truchet_{}'.format(length))
    image = read_image(file)
    mat = generate_truchet_tiles(image, length=length)
    centers = convert_grey_to_center(mat)
    draw_truchet_tiles(centers, length, out_file)
    return


if __name__ == '__main__':
    main()
