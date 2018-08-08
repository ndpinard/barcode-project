import requests
import json

class Post:

    def postitem(self,name,gtin14):
        arr = {}

        url = "https://www.datakick.org/api/items/"

        arr.update({'name':name,'gtin14':gtin14})

        requests.put(url+str(gtin14),json=arr)
        print("{} sent to api database.".format(arr))