# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 23:04:56 2015
Script to download all the mbox files from the PyAr Mailing list.
example_url = "http://listas.python.org.ar/pipermail/pyar/2012-March.txt.gz"
@author: pdelboca
"""

import wget
import os
from progressbar import ProgressBar
import gzip
import requests

base_url = "http://listas.python.org.ar/pipermail/pyar/"
prefix_url = ".txt.gz" 
years = ['2010','2011','2012','2013','2014','2015']
months= ["January","February","March","April","May","June","July","August","September","October","November","December"]
current_path = path = os.path.dirname(os.path.abspath(__file__))
target_folder = current_path + "/data/raw_data/"

def validate_url(url):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. Returns False if 400 else, true.
    """    
    try:
        response = requests.head(url)
        if response.status_code == 404:
            return False
        else:
            return True
    except StandardError:
        return False


print "Downloading mboxs..."
total_mbox = len(years) * len(months)

## Download Files
pbar = ProgressBar(maxval=total_mbox).start()
ii = 0
for year in years:
    for month in months:
        file_name = year + "-" + month + prefix_url
        file_path = target_folder + file_name
        url = base_url + file_name
        if validate_url(url):
            wget.download(url, out = target_folder)
        ii = ii + 1
        pbar.update(ii)
pbar.finish()          

## Extract Files
# TODO: Once downloaded I should use the list of files to extract instead of for loops
print "Extracting files...."
pbar = ProgressBar(maxval=total_mbox).start()
ii = 0
for year in years:
    for month in months:
        file_name = year + "-" + month + prefix_url
        file_path = target_folder + file_name
        try:
            gzip_file = gzip.open(file_path, 'rb')
            out_file = open(target_folder + year + "-" + month + '.txt', 'wb')
            out_file.write( gzip_file.read() )
            gzip_file.close()
            out_file.close()
        except:
            print "Error!"
        ii = ii + 1
        pbar.update(ii)
pbar.finish()     

# Append into one big Mbox
print "Appending files into one big Mbox...."
mbox_file = target_folder + "mbox.txt"
f = open(mbox_file, 'w')
pbar = ProgressBar(maxval=total_mbox).start()
ii = 0
for year in years:
    for month in months:
        file_name = year + "-" + month + prefix_url
        file_path = target_folder + file_name
        try:
            particular_mbox = open(file_path,'rb')
            f.write(particular_mbox.read())
            particular_mbox.close()
        except:
            print "Error while appending mbox!"
        ii = ii + 1
        pbar.update(ii)
f.close()
pbar.finish()

    

