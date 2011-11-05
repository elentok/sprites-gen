#!/usr/bin/env python

import os
import argparse
import Image

def combine(input_files, output_file, fixed_height=None, quality=None):
    """
    >>> if os.path.exists('test/tmp.output.png'): os.remove('test/tmp.output.png')
    >>> combine(['test/image1.png', 'test/image2.png', 'test/image3.png'], 'test/tmp.output.png')
    >>> image = Image.open('test/tmp.output.png')
    >>> image.size
    (448, 256)
    >>> image.mode
    'RGBA'

    >>> if os.path.exists('test/tmp.output.png'): os.remove('test/tmp.output.png')
    >>> combine(['test/image600x399.png'], 'test/tmp.output.png', fixed_height=100)
    >>> image = Image.open('test/tmp.output.png')
    >>> image.size
    (150, 100)
    >>> image.mode
    'RGB'
    """
    output_image_size = get_output_image_size(input_files, fixed_height)
    mode = Image.open(input_files[0]).mode
    sprites_image = Image.new(mode, output_image_size)

    x = 0
    for input_filename in input_files:
        image = Image.open(input_filename)
        (width, height) = image.size
        if fixed_height:
            (width, height) = calculate_new_image_size(width, height, fixed_height)
            image = image.resize((width, height), Image.ANTIALIAS)
        box = (x, 0, x + width, height)
        sprites_image.paste(image, box)
        x += width

    if quality:
        sprites_image.save(output_file, quality=quality)
    else:
        sprites_image.save(output_file)


def get_output_image_size(input_files, fixed_height=None):
    """
    >>> get_output_image_size(['test/image1.png', 'test/image2.png'])
    (384, 256)

    >>> get_output_image_size(['test/image1.png', 'test/image2.png'], fixed_height=100)
    (200, 100)
    
    >>> get_output_image_size(['test/image600x399.png'], fixed_height=100)
    (150, 100)
    """
    max_height = 0
    total_width = 0
    for input_filename in input_files:
        image = Image.open(input_filename)
        (width, height) = image.size
        if fixed_height:
            (width, height) = calculate_new_image_size(width, height, fixed_height)
        total_width += width
        if height > max_height:
            max_height = height
    return (total_width, max_height)

def calculate_new_image_size(width, height, new_height):
    """
    >>> calculate_new_image_size(300, 200, new_height=100)
    (150, 100)
    """
    new_width = int(width * (new_height * 1.0 / height))
    return (new_width, new_height)

def describe_args(args):
    print "Input ({0} files): {1}".format(len(args.input), ', '.join(args.input))
    print "Output: ", args.output
    print "Fixed Height: ", args.fixed_height


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output', nargs=1, help='the name of the output image file')
    parser.add_argument('input', nargs='+', help='the input image files')
    parser.add_argument('--fixed-height', '-fh', type=int, help='set a fixed height (rescale all of the images)')
    parser.add_argument('--silent', '-s', action='store_true', help='do not show any output')
    parser.add_argument('--quality', '-q',type=int, help='the quality of output image (0-100)')
    args = parser.parse_args()
    if not args.silent:
        describe_args(args)
    combine(args.input, args.output[0], 
            fixed_height=args.fixed_height,
            quality=args.quality)
