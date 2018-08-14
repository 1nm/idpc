#!/usr/bin/env python3
import argparse
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image


class IDPhotoCreator:
    """
    doc string
    """

    def __init__(self, photo_size, canvas_size, dpi, border_width):
        self.dpi = dpi
        self.canvas_width, self.canvas_height = self._mm2px(
            canvas_size)  # canvas width and height
        self.photo_width, self.photo_height = self._mm2px(
            photo_size)  # photo width and height
        blank_width, blank_height = self._mm2px(
            (10, 10))  # edge blank width and height
        self.cols, self.rows = int(
            (self.canvas_width - blank_width) / self.photo_width), int(
                (self.canvas_height - blank_height) / self.photo_height)
        self.border_width = border_width

    def _mm2px(self, size):
        width, height = size
        return int(width / 25.4 * self.dpi), int(height / 25.4 * self.dpi)

    def _draw_guide(self, canvas):
        if self.border_width > 0:
            with Drawing() as draw:
                draw.stroke_color = Color('black')
                draw.stroke_width = self.border_width
                initial_left = int(
                    (self.canvas_width - self.photo_width * self.cols -
                     (self.cols + 1) * self.border_width) / 2)
                initial_top = int(
                    (self.canvas_height - self.photo_height * self.rows -
                     (self.rows + 1) * self.border_width) / 2)
                for i in range(self.rows + 1):
                    draw.line(
                        (initial_left - int(self.border_width / 2), initial_top +
                         i * (self.photo_height + self.border_width)),
                        (initial_left + int(self.border_width / 2) +
                         (self.photo_width + self.border_width) * self.cols,
                         initial_top + i *
                         (self.photo_height + self.border_width)))
                for j in range(self.cols + 1):
                    draw.line(
                        (initial_left + j *
                         (self.photo_width + self.border_width),
                         initial_top - int(self.border_width / 2)),
                        (initial_left + j *
                         (self.photo_width + self.border_width),
                         initial_top + int(self.border_width / 2) +
                         (self.photo_height + self.border_width) * self.rows))
                draw(canvas)

    def _annotate(self, canvas):
        pass

    def create(self, photo, output):
        """
        doc string
        """

        width, height = photo.size

        if width < self.photo_width or height < self.photo_height:
            raise TypeError(
                'Image size must be no smaller than {}x{} while size of input is {}x{}'.
                format(self.photo_width, self.photo_height, width, height))

        with photo.clone() as photo_resized:
            aspect = float(self.photo_width) / float(self.photo_height)
            if float(width) / float(height) > aspect:
                width = int(height * aspect)
            else:
                height = int(width / aspect)
            photo_resized.crop(width=width, height=height, gravity='center')
            # crop and resize input photo
            photo_resized.resize(self.photo_width, self.photo_height)

            with Color('white') as background:
                with Image(
                        width=self.canvas_width,
                        height=self.canvas_height,
                        background=background,
                        resolution=self.dpi) as canvas:
                    self._draw_guide(canvas)
                    initial_left = int(
                        (self.canvas_width - self.photo_width * self.cols -
                         (self.cols + 1) * self.border_width) / 2)
                    initial_top = int(
                        (self.canvas_height - self.photo_height * self.rows -
                         (self.rows + 1) * self.border_width) / 2)
                    for i in range(self.cols):
                        for j in range(self.rows):
                            left = initial_left + i * self.photo_width + \
                                (i + 1) * self.border_width - int(self.border_width / 2)
                            top = initial_top + j * self.photo_height + \
                                (j + 1) * self.border_width - int(self.border_width / 2)
                            canvas.composite(
                                top=top, left=left, image=photo_resized)
                    canvas.save(filename=output)


def main():
    """
    main function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='filename of input photo')
    parser.add_argument(
        'output',
        nargs='?',
        default='output.jpg',
        help='output filename, default value is output.jpg')
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
        '-d',
        '--dpi',
        nargs='?',
        type=int,
        default='600',
        help='dpi, default value is 600')
    parser.add_argument(
        '-w',
        '--border-width',
        nargs='?',
        type=int,
        default=2,
        help='border width in mm, default value is 2')
    args = parser.parse_args()
    photo_size = map(int, args.photo_size.split('x'))
    canvas_size = map(int, args.paper_size.split('x'))
    idpc = IDPhotoCreator(photo_size, canvas_size, args.dpi, args.border_width)
    with Image(filename=args.input) as photo:
        idpc.create(photo, args.output)


if __name__ == '__main__':
    main()
