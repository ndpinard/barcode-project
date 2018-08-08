import os
import glob

class Findy():

    def findlatest(self,directory): #get the name of the newest JPG file in specified directory
        list_of_files = glob.glob('/'+str(directory)+ '/*.JPG') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file

    def findall(self,directory): # get a list of all JPG files in specified directory
        list_of_files = glob.glob('/'+str(directory)+ '/*.JPG')
        return list_of_files