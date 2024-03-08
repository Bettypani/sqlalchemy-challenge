
# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api route."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= prev_year).all()

    session.close()

    precipitation_dict = {date: prcp for date, prcp in results}

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def all_stations():

    session = Session(engine)

    # Query all stations
    results = session.query(station.station).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_stations_list = list(np.ravel(results))

    return jsonify(all_stations_list)

@app.route("/api/v1.0/tobs")
def temperature():

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    session = Session(engine)

    #Query results
    results_2 = session.query(measurement.date, measurement.tobs).\
    filter(measurement.station == 'USC00519281').\
    filter(measurement.date >= prev_year).all()
    
    session.close()

    #Convert results to a dictionary
    tobs_dict = {date: tobs for date, tobs in results_2}

    return jsonify(tobs_dict)


@app.route("/api/v1.0/<start>")
def start(start=None):


    start = dt.datetime.strptime(start, "%Y-%m-%d")

    session = Session(engine)

    results_3 = session.query(func.avg(measurement.tobs), func.max(measurement.tobs), func.min(measurement.tobs)).\
    filter(measurement.date >= start).all()


    session.close()

    #start_dict = {start for date, average in results_3, max in results_3, min in results_3}
    for avg, min, max in results_3:
        start_dict = {
            "Average Temperature": round(avg, 2),
            "Min Temp": min, 
            "Max_Temp": max
        }


    return jsonify(start_dict)



@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):

    start = dt.datetime.strptime(start, "%Y-%m-%d")
    end = dt.datetime.strptime(end, "%Y-%m-%d")

    session = Session(engine)

    results_4 = session.query(func.avg(measurement.tobs), func.max(measurement.tobs), func.min(measurement.tobs)).\
    filter(measurement.date >= start).\
    filter(measurement.date <= end).all()
    
    session.close()

    for avg, min, max in results_4:
        end_dict = {
            "Average Temperature": round(avg, 2),
            "Min Temp": min, 
            "Max_Temp": max

        }

    return jsonify(end_dict)

if __name__ == '__main__':
    app.run(debug=True)
    


if __name__ == '__main__':
    app.run(debug=True)
