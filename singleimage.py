from pyzbar import pyzbar
import cv2
from airdropped import Findy
import imutils
import os

class Oneimage:
    def process(self,file):

        image = cv2.imread(file)
        frame = imutils.resize(image, height = 400,width=400)
        barcodes = pyzbar.decode(frame)

        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw the
            # bounding box surrounding the barcode on the image
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # the barcode data is a bytes object so if we want to draw it on
            # our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 0, 255), 2)

            # print the barcode type and data to the terminal
            print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
            delete = input("Delete files? y/n: ")
            if delete == 'y':
                print("Cleaning files for next use...")
                os.remove(file)

            upc = str((barcode[0]))
            upc = upc.strip("a,b,'")
            return str(upc)


        # show the output image
            # cv2.imshow("Barcode Scanner", image)
            # key = cv2.waitKey(1) & 0xFF
