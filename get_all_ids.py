# -*- coding: utf-8 -*-
"""
Utilitary script to generate a JSON with all the ID's

the aim of the file generated is to be used on the 
'test_all_ids.py' script
"""
import sys
import json
import utils


if __name__ == "__main__":
    # Insert data
    with open("starlink_historical_data.json") as f:
        try:
            _data = json.load(f)
            all_ids = map(lambda x: x.get("id", ""), _data)
            # save as json
            with open(utils.DEFAULT_IDS_OUTPUT, "w") as output:
                json.dump(list(all_ids), output)
            print(f"Successfully saved {utils.DEFAULT_IDS_OUTPUT}...")
        except Exception as e:
            print(f"Unexpected exception: '{e}'")
            sys.exit(1)

