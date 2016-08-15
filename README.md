# ID Photo Creator

+ Create tiled ID photos that are ready for print
+ Adjustable parameters
  - Photo size (i.e size of each tile), 35mm x 45mm by default
  - Print size (i.e size of final image), 89mm x 127mm (L size) by default
  - DPI, 600 by default
  - Guide (see example)


# Usage

    usage: idpc [-h] [--photo-size [PHOTO_SIZE]] [--print-size [PRINT_SIZE]]
                [--dpi [DPI]] [--guide]
                input [output]

    positional arguments:
      input                 filename of input photo
      output                output filename, default value is output.jpg

    optional arguments:
      -h, --help            show this help message and exit
      --photo-size [PHOTO_SIZE]
                            photo size (size of each tile) widthxheight in mm,
                            default value is 35x45
      --print-size [PRINT_SIZE]
                            print size (size of output image) widthxheight in mm,
                            default value is 89x127 (L size)
      --dpi [DPI]           dpi, default value is 600
      --guide               guide will be drawn if True


# Example

    ./idpc.py --photo-size 35x45 --print-size 89x127 --dpi 600 --guide photo.jpg 35x45-lban-printable.jpg

![output](https://1nm.org/git/1nm/idpc/uploads/5707c61aa78527c7e9a158197b054dbb/output.jpg)