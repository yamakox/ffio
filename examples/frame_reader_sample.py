#!/usr/bin/env python3

from ffio import FrameReader
from PIL import Image

def main():
    with FrameReader('sample.mp4') as reader:
        count = 0
        for i, frame in enumerate(reader.frames(), 1):
            img = Image.fromarray(frame)
            img.save(f'sample{i:03}.jpg')
            count += 1
        print(f'{count} frames are saved.')

if __name__ == '__main__':
    main()
