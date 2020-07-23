import json
import os
import requests as req
import sys
import time
from collections import Counter
from glob import glob

def get_json(json_path):

    # get updated master bulk JSON file if it isn't already in directory
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    else:
        print("JSON files exist\n")

    if not os.path.exists(json_path + "MASTER_BULK.json") and not os.path.exists(json_path + "UNIQUE_ARTWORK.json"):
        master_bulk_url = "https://api.scryfall.com/bulk-data"
        master_bulk = req.get(master_bulk_url, allow_redirects=True)
        open(bulkDir + "MASTER_BULK.json", 'wb').write(master_bulk.content)

        # now get json for unique flavour text
        f = open(json_path + "MASTER_BULK.json")
        master_json_dicts = json.load(f)

        for object in master_json_dicts['data']:
            if object['name'] == 'Unique Artwork':
                unique_bulk_url = object['download_uri']

        unique_artwork_bulk = req.get(unique_bulk_url, allow_redirects=True)
        open(json_path + "UNIQUE_ARTWORK.json", 'wb').write(unique_artwork_bulk.content)


def get_flavor_text(json_file, working_directory):
    textDir = working_directory + '/FlavorText'
    if not os.path.exists(textDir):
        os.makedirs(textDir)
    # Make file containing all flavor text from all cards, concatenated
    filename = 'flavortext_corpus.txt'
    f = open(os.path.join(textDir, filename),'w+')
    f.close()
    f = open(os.path.join(textDir, filename), 'a')

    # concatenate all flavor text
    for card in json_file:
        id = card["id"]
        type = card['type_line']
        filename = id + ".txt"

        if "flavor_text" in card.keys():
            text = card["flavor_text"] #req.get(card["flavor_text"], allow_redirects=True)
            f.write(text+"\n----------\n")
            #time.sleep(0.1)

def main():
    #define current working directory
    currDir = os.path.dirname(os.path.realpath(__file__))

    #define where json files will live
    bulkDir = currDir + os.sep + "Bulk_JSON" + os.sep

    #dowload and format JSON files
    get_json(bulkDir)

    #open unique artwork json file
    with open(bulkDir + "UNIQUE_ARTWORK.json", encoding="utf8") as json_file:
        unique_json_dicts = json.load(json_file)

    #get images, choosing colours for example here
    get_flavor_text(unique_json_dicts, currDir)

if __name__=="__main__":
    main()
