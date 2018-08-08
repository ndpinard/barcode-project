import requests
import json

class Pull:

    def pullitem(self, gtin14):
        url = "https://www.datakick.org/api/items/"
        #item = input("What is the upc code? ")
        reqs = requests.get(url+str(gtin14))

        item = reqs.json()

        try:    #this is error handling for when an empty dict object is retrieved
            item = item['name']
            return item
        except KeyError:
            out =  'upc not found'




# p = Pull()
# print(p.pullitem(184078000008))
