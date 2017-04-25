# ID Photo Creator

Create ready-for-print tiled ID photos

# Prerequisites

* Python 3
  * Wand 0.4.3
  * argparse 1.4.0
* Imagemagick 6


## Install Prerequisites with Homebrew

```SH
brew install python3 imagemagick@6
pip3 install -r requirements.txt
```

# Usage

```
usage: idpc.py [-h] [--photo-size [PHOTO_SIZE]] [--paper-size [PAPER_SIZE]]
               [--dpi [DPI]] [--guide-width [GUIDE_WIDTH]]
               input [output]

positional arguments:
  input                 filename of input photo
  output                output filename, default value is output.jpg

optional arguments:
  -h, --help            show this help message and exit
  --photo-size [PHOTO_SIZE]
                        photo size (size of photo in printed size)
                        widthxheight in mm, default value is 35x45
  --paper-size [PAPER_SIZE]
                        paper size (size of paper used for print) widthxheight
                        in mm, default value is 89x127 (L size)
  --dpi [DPI]           dpi, default value is 600
  --guide-width [GUIDE_WIDTH]
                        guide width, default value is 0 (no guide)
```

# Example

```SH
./idpc.py --photo-size 35x45 --paper-size 89x127 --dpi 600 --guide-width photo.jpg 35x45-lban-printable.jpg
```

![output](https://1nm.org/git/1nm/idpc/uploads/5707c61aa78527c7e9a158197b054dbb/output.jpg)
