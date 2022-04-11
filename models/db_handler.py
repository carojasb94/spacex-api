# -*- coding: utf-8 -*-
"""  """
import os
import sys
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import (InvalidURI, CollectionInvalid, InvalidOperation)
import utils


class DBHandler(object):
    """
    """
    def __init__(self, dbname: str, collection_name: str, init_schema=False):
        """
        Args:
            con (dict): arguments to connect to the db
        """
        self.client = self.__connect(dbname)
        self.db = self.client[dbname]
        if init_schema:
            self.init_schema(collection_name)
        else:
            self.collection = self.db[collection_name]
    
    def get_con_vars(self):
        """
        Reads from default values and from env. variables
        to return the values to connec to DB
        Returns:
            _type_: str, int
        """
        conn_string = os.environ.get("MONGODB_URL", "")
        port = utils.DEFAULT_MONGODB_PORT
        try:
            port = int(os.environ.get("MONGODB_PORT", port))
        except ValueError as e:
            print("Failed to parse port")
            sys.exit(1)
        print(f"\nConecting to host '{conn_string}'...")
        return conn_string, port
    
    def __connect(self, dbname: str) -> MongoClient:
        conn_string, port = self.get_con_vars()
        try:
            return MongoClient(conn_string, port)
        except InvalidURI as e:
            print(f"Failed to connect: '{e}'")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected exception at __connect: '{e}'")
            sys.exit(1)
    
    def __create_schema(self, collection_name: str, *args, **kwargs) -> None:
        """
        Function to initialize the time-series collection
        
        Args:
            collection_name (str): Name given to the collection
        """
        try:
            self.collection = self.db.create_collection(
                name=collection_name,
                timeseries={
                    "timeField": "creation_date",
                    "metaField": "id"},
                *args,
                **kwargs
            )
        except CollectionInvalid as e:
            print(f"Failed to setup collection: '{e}'")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected exception at __create_schema: '{e}'")
            sys.exit(1)
    
    def init_schema(self, collection_name: str):
        """
        Args:
            collection_name (str): _description_
        """
        self.__create_schema(collection_name)

    def build_data(self, row) -> dict:
        """
        function used on map operation
        it build the row to be inserted on mongo collection
        Args:
            row (_type_): dict
        Returns:
            dict: dict
        """
        return {
            "id": row.get("id", ""),
            "creation_date": datetime.strptime(
                row.get("spaceTrack", {}).get("CREATION_DATE"),
                "%Y-%m-%dT%H:%M:%S"),
            "longitude": row.get("longitude", ""),
            "latitude": row.get("latitude", ""),
        }
    
    def insert_data(self, fpath: str) -> None:
        """
        Args:
            fpath (str): source path of the data
        """
        import json
        with open(fpath) as f:
            try:
                _data = json.load(f)
                _reduced_list = map(self.build_data, _data)
                x = self.collection.insert_many(_reduced_list, ordered=False)
                print(f"Successfully Inserted {len(x.inserted_ids)} rows...")
            except InvalidOperation as e:
                print(f"Failed to perform InsertMany: '{e}'")
                sys.exit(1)
            except Exception as e:
                print(f"Unexpected exception at insert_data: '{e}'")
                sys.exit(1)

