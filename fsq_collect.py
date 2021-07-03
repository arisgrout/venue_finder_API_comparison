#!/usr/bin/env python3

"""
FSQ get Data
With a free account, Foursquare only allows 50 requests an hour to reach endpoint venues/VENUE_ID

As a work around, I created 3 free FSQ accounts, and a function to run a get request to venues/VENUE_ID for each on the hour + 5 minutes. Pulling 150 new unique json files an hour until all 858 unique ids have been requested for. 
"""

import os
import numpy as np
import pandas as pd
import requests as re
import foursquare as fsq
import json
import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# establish DB connection
connection = create_connection("./sm_app.sqlite")

# open fsq_master from DB
fsq_master = pd.read_sql_query("SELECT * from fsq", connection, index_col="index")
id_fsq = fsq_master["fsq_bus_id"].drop_duplicates().astype(str).tolist()

# close DB connection
connection.close()

# import all free account details (all 3)
fsq_id = os.environ["FOURSQUARE_CLIENT_ID"]
fsq_secret = os.environ["FOURSQUARE_CLIENT_SECRET"]
client = fsq.Foursquare(client_id=fsq_id, client_secret=fsq_secret)

fsq_id2 = os.environ["FSQ_CID2"]
fsq_secret2 = os.environ["FSQ_S2"]
client2 = fsq.Foursquare(client_id=fsq_id2, client_secret=fsq_secret2)

fsq_id3 = os.environ["FSQ_CID3"]
fsq_secret3 = os.environ["FSQ_S3"]
client3 = fsq.Foursquare(client_id=fsq_id3, client_secret=fsq_secret3)

# open list for storing JSONs
fsq_jsons = []


def fsq_daily_data(start, stop):

    from datetime import datetime, timedelta
    import time

    count = start

    while count < stop:
        try:
            while 1:
                fsq_jsons.append(client.venues(id_fsq[count]))
                count += 1
        except Exception:
            pass

        try:
            while 1:
                fsq_jsons.append(client2.venues(id_fsq[count]))
                count += 1
        except Exception:
            pass

        try:
            while 1:
                fsq_jsons.append(client3.venues(id_fsq[count]))
                count += 1
        except Exception:
            pass

        print(f"json collected: {len(fsq_jsons)}, index on: {count}")

        # try writing out with run (every 4 hours)
        with open(f"fsq_details{count}.txt", "w") as outfile:  ## write jsons to file
            try:
                json.dump(fsq_jsons, outfile)
            finally:
                outfile.close()

        dt = datetime.now() + timedelta(hours=4)

        while datetime.now() < dt:
            time.sleep(1)

    return fsq_jsons, count


# final write out once complete
fsq_done = fsq_daily_data(0, len(id_fsq))

with open("fsq_details_done.txt", "w") as outfile:  ## write jsons to file
    json.dump(fsq_done, outfile)
