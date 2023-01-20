#!/usr/bin/env python3

from ffio import FrameReader
from PIL import Image

def main():
    with FrameReader('sample.mp4') as reader:
        i = 0
        while (frame := reader.read_frame()) is not None:
            i += 1
            img = Image.fromarray(frame)
            img.save(f'sample{i:03}.jpg')
        print(f'{i} frames are saved.')

if __name__ == '__main__':
    main()
