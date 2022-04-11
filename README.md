# SPACEX-API EXERCISE

## How to execute it

**1 - Build the image/container**

```
make build
```
---

**2 - Run the container and open a ssh session inside it**

```
make devshell
```

---

**3 - Populate the DB**

```
make initdb
```

The make command will call the `initdb.py` script.

It makes insert the data into the MongoDB database as a TimeSeries

The script must be called just once.

---

## RUN SCRIPT(s)

### Calculate position

```
usage: calculate_position.py [-h] [--latitude [latitude]]
                             [--longitude [longitude]]
                             id [date]

Calculate the last known position of a satellite

positional arguments:
  id                    ID of the given Satelite Example:
                        5f487be7d76203000692e502
  date                  Date to calculate the last known position, If date is
                        not provided then set $today as default the Script
                        expects the date in format 'YYYY-MM-DDTHH:MM:SS'
                        Examples: 2020-10-13T04:16:08 , 2021-01-21T06:26:10

optional arguments:
  -h, --help            show this help message and exit
  --latitude [latitude]
                        Latitude to calculate haversine
  --longitude [longitude]
                        longitude to calculate haversine

```

Where: 

- id: Satelite ID identifier:

examples:

`5eed770f096e59000698560d`

`60106f1e0c72a20006004c0e`

- date: T time to calculate the last known position 

the argument is expected at the format: `%Y-%m-%dT%H:%M:%S`

if the argument is not provided, then is set as default to `$TODAY`

examples:

`2020-09-19T06:25:10`

`2018-06-19T06:26:10`

---

#### Usage example

```
// Base usage
python calculate_position.py 60106f20e900d60006e32cbd 2020-09-19T06:25:10

// date was not passed, set $TODAY as default
python calculate_position.py 60106f20e900d60006e32cbd 
```

### Calculate Haversine

In order to calculate the Haversine value is required to pass 
both longitude & longitude as reference

The script will skip it if any latitude or longitude is None
(Satellite's values or arguments values)

##### Example

```
// Running the script without set a date, but the lat & lng values
python calculate_position.py 60106f20e900d60006e32cbd --latitude 1.0 --longitude 82
```
---


## QUERY USED

``` 
db.getCollection('spacex-data').aggregate([
    {$sort: {creation_date:-1}},
    {$match: {
        id: "$GIVEN_ID", 
        "creation_date": {
            $lte: "$GIVEN_T_DATE"
            }
        }
    },
    {$group: {_id: "$GIVEN_ID",
        creation_date : {$first:"$creation_date"},
        latitude: {$first:"$latitude"},
        longitude: {$first:"$longitude"}
    }}
])
``` 
Where `GIVEN_ID` is replaced with the given satelite ID 

and `GIVEN_T_DATE` with the T time

# @todo Improvements

- Use a SQL backend to store the data
- Calculate Haversine on different measure units
- Mock Database Handler to to Unit Test
- Query Benchmark test

