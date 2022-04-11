# -*- coding: utf-8 -*-
"""
"""
import os
import argparse
from datetime import datetime

DEFAULT_MONGODB_PORT = 27017
DEFAULT_DBNAME = os.environ.get("DEFAULT_DBNAME", "spacex-api")
DEFAULT_SCHEMA = "spacex-data"
DEFAULT_IDS_OUTPUT = "all_ids.json"
# avg earth radius 
EARTH_RADIUS_KM = 6371.0088


def get_parser():
    parser = argparse.ArgumentParser(
        description="""Calculate the last known position of a satellite""")
    parser.add_argument(
        'id',
        type=str,
        help="""
        ID of the given Satelite
        Example: 5f487be7d76203000692e502
        """
    )
    parser.add_argument(
        'date',
        type=lambda s: datetime.strptime(s, "%Y-%m-%dT%H:%M:%S"),
        nargs="?",
        default=datetime.now(),
        help="""
        Date to calculate the last known position, If date is not provided then set $today as default
        the Script expects the date in format 'YYYY-MM-DDTHH:MM:SS'
        Examples:
            2020-10-13T04:16:08 , 2021-01-21T06:26:10
        """
    )
    parser.add_argument(
        '--latitude', nargs='?', metavar='latitude',
        type=float, help='Latitude to calculate haversine')
    parser.add_argument(
        '--longitude', nargs='?', metavar='longitude',
        type=float, help='longitude to calculate haversine')
    return parser


def validate_is_last_position(db, id: str, dt: datetime, _to_assert: dict):
    """
    Utilitary function to check manually if the query works as expected
    db.getCollection('spacex-data').find({"id": "$id"})
    Args:
        db (_type_): Class that handle the connection to DB
        id (str): satelite ID
        dt (datetime): T value
        _to_assert (dict): Dict to be compared with the result of this function
    """
    # Get all the records that match with ID
    tmp_res = db.collection.find({"id": id})
    last_row = None
    for row in tmp_res:
        # If the date is bigger than the expected, just skip it
        if row.get("creation_date") > dt:
            continue
        if last_row is None:
            last_row = row
            continue
        else:
            if row.get("creation_date") >= last_row.get("creation_date"):
                # check if the row has a most recent date
                print("{id}: '{d1}' is newer than '{d2}'".format(
                    id=last_row.get("id", ""),
                    d1=row.get("creation_date"),
                    d2=last_row.get("creation_date")
                ))
                last_row = row
    
    last_row["_id"] = last_row["id"]
    last_row.pop("id")
    print("ID: '{id}' - '{date}' -- Last known position:  Lat: {lat} Lng : {lng} ".format(
        id=last_row.get("_id"),
        date=last_row.get("creation_date"),
        lat=last_row.get("latitude"),
        lng=last_row.get("longitude"),
    ))
    
    # custom dict assertion
    from unittest import TestCase
    TestCase().assertDictEqual(_to_assert, last_row)

