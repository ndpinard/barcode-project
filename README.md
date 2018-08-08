# barcode-project
Scan barcodes through video or batch processing images using pyzbar and save them in a sqlite3 database.

To start run front.py.

You can scan barcodes from your webcam, setup a folder for batch image processing, or manually enter items.
Once a barcode is found if it exists in the API database it will automatically be used and if not it will ask for the item's name.
