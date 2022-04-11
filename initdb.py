# -*- coding: utf-8 -*-
"""
"""
import utils
from models import DBHandler


if __name__ == "__main__":
    print("Initdb...")
    # Connect to DB
    db = DBHandler(
        utils.DEFAULT_DBNAME, 
        utils.DEFAULT_SCHEMA, 
        init_schema=True
    )

    # Insert data
    print("Inserting data...")
    db.insert_data("starlink_historical_data.json")

