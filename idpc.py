#!/usr/bin/env python3
import argparse
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
        self.annotation = 'Photo size: {} , Paper size: {}'.format(
            ' x '.join(str(x) + 'mm' for x in photo_size),
            ' x '.join(str(x) + 'mm' for x in canvas_size)) if annotation else None

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


def main():
    """
    Main function, parses the arguments and create the photo
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='filename of input photo')
    parser.add_argument(
        'output',
        nargs='?',
        default='output.jpg',
        help='output filename, default value is output.jpg')
    parser.add_argument(
        '-a',
        '--annotation',
        nargs='?',
        const=True,
        type=lambda x: x.lower() in ['yes', 'true', 't', 'y', '1'],
        default=False,
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
        'paper size (size of paper used for print) widthxheight in mm, default value is 89x127 (L size)'
    )
    parser.add_argument(
        '-w',
        '--border-width',
        nargs='?',
        type=int,
        default=2,
        help='border width in px, default value is 2')
    args = parser.parse_args()
    photo_size = tuple(map(int, args.photo_size.split('x')))
    canvas_size = tuple(map(int, args.paper_size.split('x')))
    idpc = IDPhotoCreator(photo_size, canvas_size, args.dpi, args.border_width, args.annotation)
    with Image(filename=args.input) as photo:
        idpc.create(photo, args.output)


if __name__ == '__main__':
    main()
