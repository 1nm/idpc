#!/usr/bin/env python3
import argparse
import re
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image


class IDPhotoCreator:
    """
    Creates ID photos
    """

    def __init__(self, photo_size, canvas_size, dpi, border_width, annotation):
        self.dpi = int(dpi)
        self.border_width = int(border_width)

        mm = 'x'.join(map(str, canvas_size))
        index = PHOTO_SIZES['mm'].index(mm) if mm in PHOTO_SIZES['mm'] else -1
        code = None if index == -1 else PHOTO_SIZES['us-code'][index] if PHOTO_SIZES['us-code'][index] else PHOTO_SIZES['jp-code'][index]

        self.annotation = 'Photo size: {} , Paper size: {} {}'.format(
            ' x '.join(str(x) + 'mm' for x in photo_size),
            ' x '.join(str(x) + 'mm' for x in canvas_size),
            '({})'.format(code) if code else "") if annotation else None

        self.canvas_size = self._mm2px(canvas_size)
        self.photo_size = self._mm2px(photo_size)
        self.shape = tuple(
            map(lambda x, y, z: int((x - y) / z),
                self.canvas_size,
                self._mm2px((10, 10)),
                self.photo_size))  # number of columns and rows
        self.pos = tuple(
            map(lambda x, y, z: int((x - y * z - (z + 1) * self.border_width) / 2),
                self.canvas_size,
                self.photo_size,
                self.shape))  # initial top and left

    def _mm2px(self, size):
        return tuple(map(lambda x: int(x / 25.4 * self.dpi), size))

    def draw_border(self, canvas):
        """
        Draws the border around photos
        """
        if self.border_width > 0:
            with Drawing() as draw:
                draw.stroke_color = Color('black')
                draw.stroke_width = self.border_width
                initial_left, initial_top = self.pos
                cols, rows = self.shape
                photo_width, photo_height = self.photo_size
                for i in range(rows + 1):
                    draw.line(
                        (initial_left - int(self.border_width / 2),
                         initial_top + i * (photo_height + self.border_width)),
                        (initial_left + int(self.border_width / 2) +
                         (photo_width + self.border_width) * cols,
                         initial_top + i * (photo_height + self.border_width)))
                for j in range(cols + 1):
                    draw.line(
                        (initial_left + j * (photo_width + self.border_width),
                         initial_top - int(self.border_width / 2)),
                        (initial_left + j * (photo_width + self.border_width),
                         initial_top + int(self.border_width / 2) +
                         (photo_height + self.border_width) * rows))
                draw(canvas)

    def annotate(self, canvas):
        """
        Annotate photo size and paper size
        """
        if self.annotation:
            with Drawing() as draw:
                draw.font_size = 40
                draw.text(100, 100, self.annotation)
                draw(canvas)

    def create(self, photo, output):
        """
        Resizes the image, creates tiles, and writes the final image to file
        """

        width, height = photo.size
        photo_width, photo_height = self.photo_size
        canvas_width, canvas_height = self.canvas_size

        if width < photo_width or height < photo_height:
            raise TypeError(
                'Image size must be no smaller than {}x{} while size of input is {}x{}'.
                format(photo_width, photo_height, width, height))

        with photo.clone() as photo_resized:
            aspect = float(photo_width) / float(photo_height)
            if float(width) / float(height) > aspect:
                width = int(height * aspect)
            else:
                height = int(width / aspect)
            photo_resized.crop(width=width, height=height, gravity='center')
            # crop and resize input photo
            photo_resized.resize(photo_width, photo_height)

            with Color('white') as background:
                with Image(
                        width=canvas_width,
                        height=canvas_height,
                        background=background,
                        resolution=self.dpi) as canvas:
                    self.draw_border(canvas)
                    initial_left, initial_top = self.pos
                    cols, rows = self.shape
                    for i in range(cols):
                        for j in range(rows):
                            left = initial_left + i * photo_width + \
                                (i + 1) * self.border_width - int(self.border_width / 2)
                            top = initial_top + j * photo_height + \
                                (j + 1) * self.border_width - int(self.border_width / 2)
                            canvas.composite(
                                top=top, left=left, image=photo_resized)
                    self.annotate(canvas)
                    canvas.save(filename=output)


PHOTO_SIZES = {"notes":["Very often called \"wallet\" size.","Size in inches is approximate.","","envelope size","postcard size","standard 135 film & print size","new size for most consumer level digital cameras and Micro 4/3 cameras[4]","envelope size","twice the size of a 3R print","postcard size","twice the size of a 4R print","for B&W paper","Can be used for contact prints from 8x10 film.","closest approximation to A4 (210×297mm), twice the size of a 6R print","for B&W paper","","At 14.5 in (368 mm), the Japanese 4PW size is slightly shorter than S10R.","","","","for B&W paper",""],"jp-code":["","DSC","L","","PC","KG","","","2L","","8P","","6P","6PW","","4P","4PW","","","","",""],"us-code":["","","3R","","","4R","4D","","5R","","6R","","8R","S8R","","10R","S10R","11R","S11R","12R","","S12R"],"inch":["2x3","3.25x4.5","3.5x5","3.5x8.1","3.9x5.8","4x6","4.5x6","4.7x9.3","5x7","5.8x7.9","6x8","7x9.5","8x10","8x12","9.5x12","10x12","10x15","11x14","11x17","12x15","12x16","12x18"],"mm":["51x76","89x119","89x127","90x205","100x148","102x152","114x152","120x235","127x178","148x200","152x203","178x240","203x254","203x305","240x305","254x305","254x381","279x356","279x432","305x381","305x406","305x457"]}
SIZE_PATTERN = re.compile(r'[0-9]+x[0-9]+')

def parse_size(photo_size):
    for code_type in ['us-code', 'jp-code', 'mm']:
        if photo_size and photo_size in PHOTO_SIZES[code_type]:
            return PHOTO_SIZES['mm'][PHOTO_SIZES[code_type].index(photo_size)]
    if not SIZE_PATTERN.match(photo_size):
        raise ValueError('Size {} cannot be parsed!'.format(photo_size))
    return photo_size


def main():
    """
    Main function, parses the arguments and create the photo
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='filename of input photo', metavar='INPUT_FILE')
    parser.add_argument(
        'output',
        metavar='OUTPUT_FILE',
        nargs='?',
        default='output.jpg',
        help='output filename, default value is output.jpg')
    parser.add_argument(
        '-a',
        '--annotation',
        action='store_true',
        help='writes photo size and paper size on image')
    parser.add_argument(
        '-d',
        '--dpi',
        nargs='?',
        type=int,
        default='600',
        help='dpi, default value is 600')
    parser.add_argument(
        '-s',
        '--photo-size',
        nargs='?',
        default='35x45',
        help=
        'photo size (size of photo in printed size) widthxheight in mm, default value is 35x45'
    )
    parser.add_argument(
        '-S',
        '--paper-size',
        nargs='?',
        default='89x127',
        help=
        'paper size (size of paper used for print) widthxheight in mm, default value is 89x127 (3R)'
    )
    parser.add_argument(
        '-w',
        '--border-width',
        nargs='?',
        type=int,
        default=2,
        help='border width in px, default value is 2')
    args = parser.parse_args()
    photo_size = tuple(map(int, parse_size(args.photo_size).split('x')))
    canvas_size = tuple(map(int, parse_size(args.paper_size).split('x')))
    idpc = IDPhotoCreator(photo_size, canvas_size, args.dpi, args.border_width, args.annotation)
    with Image(filename=args.input) as photo:
        idpc.create(photo, args.output)


if __name__ == '__main__':
    main()
