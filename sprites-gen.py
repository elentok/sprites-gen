#!/usr/bin/env python

import os
import argparse
import Image

def combine(input_files, output_file):
    """
    >>> os.remove('test/tmp.output.png')
    >>> combine(['test/image1.png', 'test/image2.png', 'test/image3.png'], 'test/tmp.output.png')
    >>> image = Image.open('test/tmp.output.png')
    >>> image.size
    (448, 256)
    >>> image.mode
    'RGBA'
    """
    output_image_size = get_output_image_size(input_files)
    mode = Image.open(input_files[0]).mode
    sprites_image = Image.new(mode, output_image_size)

    x = 0
    for input_filename in input_files:
        image = Image.open(input_filename)
        (width, height) = image.size
        box = (x, 0, x + width, height)
        sprites_image.paste(image, box)
        x += width

    sprites_image.save(output_file)



def get_output_image_size(input_files):
    """
    >>> get_output_image_size(['test/image1.png', 'test/image2.png'])
    (384, 256)
    """
    max_height = 0
    total_width = 0
    for input_filename in input_files:
        image = Image.open(input_filename)
        (width, height) = image.size
        total_width += width
        if height > max_height:
            max_height = height
    return (total_width, max_height)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output')
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()
    print args
