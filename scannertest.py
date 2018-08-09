# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import cv2
from pull import Pull
from posts import Post
from db import Database

class Vscan:

    def startscan(self):
        database = Database()

        print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()

        #vs = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)

        found = set()
        unfound = set()
        empty = set()
        # loop over the frames from the video stream
        while True:
            # grab the frame from the threaded video stream and resize it to
            # have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)

            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)
            	# loop over the detected barcodes
            for barcode in barcodes:
        		# extract the bounding box location of the barcode and draw
        		# the bounding box surrounding the barcode on the image
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        		# the barcode data is a bytes object so if we want to draw it
        		# on our output image we need to convert it to a string first
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type

        		# draw the barcode data and barcode type on the image
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                upc = str((barcode[0]))
                upc = upc.strip("a,b,'")
                print(upc)
                item = None
                if len(database.checkforitem(upc)) is 0: #politely check for data before sending api request
                    p = Pull()
                    item = p.pullitem(upc)
                    print(item)

                if item is None and len(database.checkforitem(upc)) is 0: #item does not exist in either
                    print("Detected unknown item...")
                    time.sleep(0.2)
                    a = input("What is the name of the object with barcode: {}: ".format(str(upc)))
                    database.insert(a,upc)
                    dopost = input("Would you like to send this to the api for future reference? y/n: ")
                    if dopost is "y":
                        post = Post()
                        post.postitem(a,upc)
                    time.sleep(2) #prevents multiple entries of the same item

                elif item is None and len(database.checkforitem(upc)) is not 0: #item already found, increasing quantity instead
                    print("Item found in local database, increasing quantity by one.")
                    database.selectbyupc(upc)
                    time.sleep(1.5)

                elif item != None: #api request successful
                    print("Found upc code {}, inserting into known database.".format(str(upc)))
                    database.insert(str(item),upc)
                    time.sleep(2)

                	# show the output frame
            cv2.imshow("Barcode Scanner", frame)
            key = cv2.waitKey(1) & 0xFF

        	# if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

        print("[INFO] cleaning up...")

        cv2.destroyAllWindows()
        vs.stop()
