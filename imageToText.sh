#!/usr/bash
tesseract --tessdata-dir /usr/local/share /home/pi/vira/image/image.png /home/pi/vira/text/textfile -l eng -psm 3
exit 0
