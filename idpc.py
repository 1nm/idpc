#!/usr/bin/env python3
import argparse
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image

class IDPhotoCreator:
    def __init__(self, photo_size, canvas_size, dpi, guide):
        self.dpi = dpi
        self.cw, self.ch = self._mm2px(canvas_size)  # canvas width and height
        self.pw, self.ph = self._mm2px(photo_size)  # photo width and height
        bw, bh = self._mm2px((10, 10))  # edge blank width and height
        self.cols, self.rows = int((self.cw - bw) / self.pw), int((self.ch - bh)/ self.ph)
        self.guide = guide

    def _mm2px(self, size):
        w, h = size
        return int(w / 25.4 * self.dpi), int(h / 25.4 * self.dpi)

    def _draw_guide(self, canvas):
        if self.guide:
            with Drawing() as draw:
                draw.stroke_color = Color('black')
                draw.stroke_width = 1
                l = int((self.cw - self.pw * self.cols - (self.cols + 1)) / 2)
                t = int((self.ch - self.ph * self.rows - (self.rows + 1)) / 2)
                for i in range(self.cols + 1):
                    draw.line((l, t + i * (self.ph + 1)), (l + self.pw * self.cols + self.cols, t + i * (self.ph + 1)))
                for j in range(self.rows + 1):
                    draw.line((l + j * (self.pw + 1), t), (l + j * (self.pw + 1), t + self.ph * self.rows + self.rows))
                draw(canvas)

    def create(self, photo, output):
        w, h = photo.size
        if w < self.pw or h < self.ph:
            raise TypeError('Image size must be no smaller than {}x{} while size of input is {}x{}'.format(self.pw, self.ph, w, h))

        with photo.clone() as photo_resized:
            aspect = float(self.pw) / float(self.ph)
            if float(w) / float(h) > aspect:
                w = int(h * aspect)
            else:
                h = int(w / aspect)
            photo_resized.crop(width=w, height=h, gravity='center')  # crop and resize input photo
            photo_resized.resize(self.pw, self.ph)

            with Color('white') as bg:
                with Image(width=self.cw, height=self.ch, background=bg, resolution=self.dpi) as canvas:
                    self._draw_guide(canvas)
                    l = int((self.cw - self.pw * self.cols - (self.cols + 1 if self.guide else 0)) / 2)
                    t = int((self.ch - self.ph * self.rows - (self.rows + 1 if self.guide else 0)) / 2)
                    for i in range(self.cols):
                        for j in range(self.rows):
                            left = l + i * self.pw + (i + 1 if self.guide else 0)
                            top = t + j * self.ph + (j + 1 if self.guide else 0)
                            canvas.composite(top=top, left=left, image=photo_resized)
                    canvas.save(filename=output)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='filename of input photo')
    parser.add_argument('output', nargs='?', default='output.jpg', help='output filename, default value is output.jpg')
    parser.add_argument('--photo-size', nargs='?', default='35x45', help='photo size (size of each tile) widthxheight in mm, default value is 35x45')
    parser.add_argument('--print-size', nargs='?', default='89x127', help='print size (size of output image) widthxheight in mm, default value is 89x127 (Japanese L ban)')
    parser.add_argument('--dpi', nargs='?', type=int, default='600', help='dpi, default value is 600')
    parser.add_argument('--guide', action='store_true', help='guide will be drawn if True')
    args = parser.parse_args()
    photo_size = map(int, args.photo_size.split('x'))
    canvas_size = map(int, args.print_size.split('x'))
    idpc = IDPhotoCreator(photo_size, canvas_size, args.dpi, args.guide)
    with Image(filename=args.input) as photo:
        idpc.create(photo, args.output)

if __name__ == '__main__':
    main()
