#!/usr/bin/env python

import argparse
import Image

def combine(input_files, output_file):
    """
    >>> combine(['test/image1.png', 'test/image2.png'], 'test/tmp.output.png')
    >>> Image.open('test/tmp.output.png').im_size
    (384, 256)
    """
    output_image_size = get_output_image_size(input_files)

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
