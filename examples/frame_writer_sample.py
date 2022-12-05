# https://matplotlib.org/matplotblog/posts/animated-fractals/

import numpy as np
from ffmpeg_frame_io import FrameWriter

def main():
    x_start, y_start = -2, -2
    width, height = 4, 4
    density_per_unit = 100
    with FrameWriter('sample.mp4', size=(width * density_per_unit, height * density_per_unit), stdout=True) as writer:
        for X in generate_julia_set((x_start, y_start), (width, height), density_per_unit):
            writer.frame[:, :, 1] = 255 * X // np.max(X)
            writer.write_frame()

def julia_quadratic(zx, zy, cx, cy):
    threshold = 20
    z = complex(zx, zy)
    c = complex(cx, cy)
    for i in range(threshold):
        z = z**2 + c
        if abs(z) > 4.:
            return i
    return threshold - 1

def generate_julia_set(start, dim, density_per_unit):
    re = np.linspace(start[0], start[0] + dim[0], dim[0] * density_per_unit)
    im = np.linspace(start[1], start[1] + dim[1], dim[1] * density_per_unit)
    r = 0.7885
    a = np.linspace(0, 2*np.pi, 100)
    X = np.empty((len(re), len(im)))
    for i in range(len(a)):
        cx, cy = r * np.cos(a[i]), r * np.sin(a[i])
        for i in range(len(im)):
            for j in range(len(re)):
                X[i, j] = julia_quadratic(re[j], im[i], cx, cy)
        yield X

if __name__ == '__main__':
    main()
