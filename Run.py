import emailFunctions
from time import sleep
import Scanning as scan
import pandas as pd
import DeleteAddShow

while True:
    print('Checking emails to see if users want to add or delete websites from their csv file')

    print(emailFunctions.add_delete_website())

    print('\nScanning each user\'s website lists to see if there are any changes in their websites')
    sleep(15)
    scan.scanning()
    print('\nFinished scanning')

    sleep(20)



    #where you iterate through email list and iterate through their websites to see if there are changes (Threading)!!

