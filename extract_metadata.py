import numpy as ny
# import pandas as pd
import math as math
import csv
import os
import io
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs
content = []
from collections import defaultdict
import itertools

#uid_to_text = defaultdict(list)

def extract_metadata():

    uid_to_text = defaultdict(list)
    i = 0

    with open('test_metadata.csv', encoding='cp1252', errors='ignore') as f_in:
        reader = csv.DictReader(f_in)
        for row in reader:
        
            # access some metadata
            uid = row['uid']
            title = row['title']
            abstract = row['abstract']
            authors = row['authors']
            #source_x = row['source_x']
            #authors = row['authors'].split('; ')

            # access the full text (if available) for Intro
            #introduction = []
            #if row['pmc_json_files']:
            #    for json_path in row['pmc_json_files'].split('; '):
            #        with open(json_path) as f_json:
             #           full_text_dict = json.load(f_json)

                        # grab introduction section from *some* version of the full text
              #          for paragraph_dict in full_text_dict['body_text']:
               #             paragraph_text = paragraph_dict['text']
               #             section_name = paragraph_dict['section']
               #             if 'conclusion' in section_name.lower():
               #                 introduction.append(paragraph_text)

                        # stop searching other copies of full text if already got introduction
                #        if introduction:
                #            break
               # con_string = str(introduction)
            # save for later usage
            uid_to_text[uid].append(title + " " + abstract + " " + authors + " ")

        i += 1
        if (i % 5000 == 0):
            print("Indexed " , i , " rows")

    with open('output/output.dat', 'w', newline='') as f_out, \
         open('output/metadata.dat', 'w', newline='') as f_out_meta:

        output_writer = csv.writer(f_out)
        metadata_writer = csv.writer(f_out_meta)

        for key, value in uid_to_text.items():
            output_writer.writerow(value)
            metadata_writer.writerow([key])

def make_sample(n):
    with open('metadata.csv', 'r', encoding='cp1252', errors='ignore') as f_in, \
         open('metadata_samples.csv', 'w', newline='', encoding='utf8') as f_out:
        
        csv_reader = csv.reader(f_in)
        csv_writer = csv.writer(f_out)

        csv_writer.writerows(itertools.islice(csv_reader, 0, n))

        

#-------
# below code is to extract info into an output file
## Was also suing column 'uid'
# metadata_subset = pd.read_excel('metadata_sample.xlsx', index_col = None, na_values = None, usecols = ['title', 'abstract', 'authors'])
# print("I've been here")
# writer = pd.ExcelWriter('output.xlsx')
# metadata_subset.to_excel(writer)
# writer.save()
# print('DataFrame is written successfully')
#make_sample(1000)

extract_metadata()

#------------
# below code is to convert and extract info from XML file into text file

infile = open("test_queries.xml", "r")
contents = infile.read()
soup = bs(contents,'xml')
query = soup.find_all("query")
question = soup.find_all("question")
narrative = soup.find_all("narrative")

outfile = open ("queries.txt", "w")
for i in range(0, len(query)):
    #print(query[i].get_text(), sep = "\n")
    #print(question[i].get_text(), sep = "\n")
    outfile.write(query[i].get_text() + "," + question[i].get_text() + narrative[i].get_text() + "\n")
outfile.close()

# #--------------
# # below code eliminates the 0 score from qrels.txt and ouputs it to qrels_simplified.txt
# with open('qrels.txt', "r") as qrel_in:
#     with open ('qrels_simplified.txt', "w") as qrel_out:
#         for newline in qrel_in:
#             newline = newline.split()
#             if int(newline[2]) != 0:
#                 qrel_out.write(" ".join(newline))
#                 qrel_out.write("\n")




