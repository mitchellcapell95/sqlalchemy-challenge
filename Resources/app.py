import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date><br/>"
        f"/api/v1.0/<start_e>/<end_s><br/>"
    )

## /api/v1.0/precipitation
## Convert the query results to a Dictionary using date as the key and prcp as the value.
## Return the JSON representation of your dictionary

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation Values"""
    # Query all passengers
    results = session.query(Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_prcps

    all_prcps = []
    for prcps in results:
        measurement_dict = {}
        measurement_dict["prcp"] = prcps
        all_prcps.append(measurement_dict)

    return jsonify(all_prcps)


## Return a JSON list of stations from the dataset.


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all stations
    results2 = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results2))

    return jsonify(all_stations)

## query for the dates and temperature observations from a year from the last data point.
## Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route("/api/v1.0/tobs")
def dates_tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observation data including dates and tobs"""
    # Query all dates and temperatures

    results3 = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").filter(Measurement.date <= "2017-08-23").all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results3))

    return jsonify(all_tobs)


## Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
## When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.


@app.route("/api/v1.0/<start_date>")
def start(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observation data including min,max and avg"""
    # Query all min,max and avg for specified start date to the end of the data set (08-23-2017) - no specified end date

    results4 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    # >= needs to be a datetime data type...append results4 to empty list ?

    session.close()

    # Convert list of tuples into normal list
    all_starts = list(np.ravel(results4))

    return jsonify(all_starts)



## When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.


@app.route("/api/v1.0/<start_e>/<end_s>")
def start_end(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observation data including min,max and avg"""
    # Query all min, max and avg for specified start and end date

    results5 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Convert list of tuples into normal list
    all_starts_end = list(np.ravel(results5))

    return jsonify(all_starts_ends)



if __name__ == '__main__':
    app.run(debug=True)


