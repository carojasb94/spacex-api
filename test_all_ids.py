# -*- coding: utf-8 -*-
"""
Script to validate all the ID's from  starlink_historical_data.json

The script will iterate over each ID, and validate that the query has the expected result
"""
import sys
import json
import utils
from datetime import datetime
from models import DBHandler
from calculate_position import (get_last_position)


if __name__ == '__main__':
    db = DBHandler(
        utils.DEFAULT_DBNAME,
        utils.DEFAULT_SCHEMA,
        init_schema=False
    )
    _date = datetime.now()
    with open(utils.DEFAULT_IDS_OUTPUT) as f:
        try:
            all_ids = json.load(f)
            # save as json
            for i, id in enumerate(all_ids, 1):
                print(f"\t{i} - {id} ...")
            # Get position by a given ID
            _res = get_last_position(db, id, _date)
            utils.validate_is_last_position(db, id, _date, _res)
        except Exception as e:
            print(f"Unexpected exception: '{e}'")
            sys.exit(1)

