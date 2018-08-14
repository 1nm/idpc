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
usage: idpc.py [-h] [-a] [-d [DPI]] [-s [PHOTO_SIZE]] [-S [PAPER_SIZE]]
               [-w [BORDER_WIDTH]]
               INPUT_FILE [OUTPUT_FILE]

positional arguments:
  INPUT_FILE            filename of input photo
  OUTPUT_FILE           output filename, default value is output.jpg

optional arguments:
  -h, --help            show this help message and exit
  -a, --annotation      writes photo size and paper size on image
  -d [DPI], --dpi [DPI]
                        dpi, default value is 600
  -s [PHOTO_SIZE], --photo-size [PHOTO_SIZE]
                        photo size (size of photo in printed size)
                        widthxheight in mm, default value is 35x45
  -S [PAPER_SIZE], --paper-size [PAPER_SIZE]
                        paper size (size of paper used for print) widthxheight
                        in mm, default value is 89x127 (3R)
  -w [BORDER_WIDTH], --border-width [BORDER_WIDTH]
                        border width in px, default value is 2
```

# Example

```SH
./idpc.py -a -S 3R input.jpg
```
