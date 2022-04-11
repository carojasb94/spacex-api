# -*- coding: utf-8 -*-
"""
"""
import os
from datetime import datetime
from pymongo import (DESCENDING)
from models import DBHandler
import utils


DEFAULT_MONGODB_PORT = 27017
DEFAULT_DBNAME=os.environ.get("DEFAULT_DBNAME", "spacex-api")
DEFAULT_SCHEMA="spacex-data"
DEFAULT_STRFORMAT = "%Y-%m-%d %H:%M:%S"


from math import radians, cos, sin, asin, sqrt, degrees, pi, atan2


def get_haversine(row: dict, lat2, lng2) -> float:
    """
    Args:
        row (dict): _description_
        lat (_type_): _description_
        lng (_type_): _description_
    """
    # get lat/lng from satelite
    lat1, lng1 = row.get("latitude"), row.get("longitude")
    if lat1 is None or lng1 is None:
        print("Satelite's Latitude and longitude must not be None, haversine skipped")
        return
    if lat2 is None or lng2 is None:
        print("Both Latitude and longitude must be passed, haversine skipped")
        return
    
    print("Calculating haversine:")
    print(f"\tP1: ({lat1}, {lng1}) - P2: ({lat2}, {lng2})")
    # convert to radians
    lat1 = radians(lat1)
    lng1 = radians(lng1)
    lat2 = radians(lat2)
    lng2 = radians(lng2)

    # calculate haversine
    _lat = lat2 - lat1
    _lng = lng2 - lng1
    
    d = sin(_lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(_lng * 0.5) ** 2
    _res =  2 * utils.EARTH_RADIUS_KM * asin(sqrt(d))
    print(f"\t\thaversine value is {_res} Km.")


def get_last_position(db, id: str, date: datetime):
    """
    Function to calculate the last known position of a satellite
    
    The query that performs the search is:
    
    db.getCollection('spacex-data').aggregate([
        {$sort: {creation_date:-1}},
        {$match: {id: "$id", "creation_date": {$lte: ISODate("2020-09-19 06:25:10.000Z")}}},
        {$group: {_id: "$id",
            creation_date : {$first:"$creation_date"},
            latitude: {$first:"$latitude"},
            longitude: {$first:"$longitude"}
        }}
    ])
    
    Args:
        db (_type_): Class that handle the connection to DB
        id (str): satelite ID
        date (datetime): T value
    Returns:
        _type_: Satelite Row
    """
    pipeline = [
        {"$sort": {"creation_date": DESCENDING}},
        {"$match": {"id": f"{id}"}},
        {"$match": {
            "id": f"{id}",
            "creation_date": {
                "$lte": date
                }
            }
        },
        {"$group": {
            "_id" : f"{id}",
            "creation_date": {
                "$first": "$creation_date"
            },
            "latitude": {
                "$first": "$latitude"
            },
            "longitude": {
                "$first": "$longitude"
            }
        }}
    ]
    # Query gets a single result
    tmp_res = db.collection.aggregate(pipeline)
    _res = next(tmp_res)
    print("\tID: '{id}' - '{date}' -- Last known position:  Lat: {lat} Lng : {lng} ".format(
        id=_res.get("_id"),
        date=_res.get("creation_date"),
        lat=_res.get("latitude"),
        lng=_res.get("longitude"),
    ))
    return _res


if __name__ == '__main__':
    parser = utils.get_parser()
    args = parser.parse_args()
    # connect to DB
    db = DBHandler(
        utils.DEFAULT_DBNAME,
        utils.DEFAULT_SCHEMA,
        init_schema=False
    )    
    print(f"Calculating the last Position for '{args.id}' given T as '{args.date}'...\n")
    # Get position by a given ID
    _res = get_last_position(db, args.id, args.date)
    # call to assert expected result
    # utils.validate_is_last_position(db, args.id, args.date, _res)
    
    # If lat & lng is valid, then calculate haversine
    get_haversine(_res, args.latitude, args.longitude)

