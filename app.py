import pandas as pd
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# DB Setup
# ---------------------------------------------------------
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

Base = automap_base()
Base.prepare(engine, reflect = True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route('/')
def welcome():
    return (
        f'Welcome to the Hawaii climate analysis site!<br/>'
        f'Below are the available API routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/temp_calc/<start><br/'
        f'/api/v1.0/temp_calc/<start>/<end>'
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # querying precipation data from final day in dataset to one year prior to final day
    prcp_results = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date <="2017-08-23")\
    .filter(Measurement.date >="2016-08-23").all()

    # list comprehension to create dict of query results
    precip = {date: prcp for date, prcp in prcp_results}
  
    # jsonifying precipitation dict
    return jsonify(precip)
    


@app.route('/api/v1.0/stations')
def stations():
    station_results = session.query(Station.station, Station.name).all()
    
    # unraveling results to array and converting to list   
    stations = list(np.ravel(station_results))
    
    # converting station list to json object
    return jsonify(stations)



@app.route('/api/v1.0/tobs')
def tobs():
    # gathering tobs between final day in dataset and one year prior to final day
    # tobs_results = session.query(Measurement.date, Measurement.tobs)\
    # .filter(Measurement.date.between("2017-08-23","2016-08-23")).all()

    tobs_results = session.query(Measurement.date, Measurement.tobs)\
    .filter(Measurement.date <="2017-08-23")\
    .filter(Measurement.date >="2016-08-23").all()

    # unraveling results to array and converting to list
    tobs = list(np.ravel(tobs_results))

    # jsonifying tobs list
    return jsonify(tobs)

@app.route('/api/v1.0/temp_calc/<start>')
def temp_start(start=None):
    start_date = "2015-08-23"
    # gathering min, avg, max temps 
    min_avg_max = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # temp calc results for all dates after start date
    start_results = session.query(*min_avg_max).filter(Measurement.date >= start_date).all()
        
    # unraveling results to array and converting to list
    start_temps = list(np.ravel(start_results))

    # converting to json object
    return jsonify(start_temps)

@app.route('/api/v1.0/temp_calc/<start>/<end>')
def temp_all(start=None, end=None):
    start_date = "2015-08-23"
    end_date = "2016-08-23"

    # gathering min, avg, max temps
    min_avg_max = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # min/max/avg temps between start and end date
    all_results = session.query(*min_avg_max).filter(Measurement.date.between(start_date, end_date)).all()
        
    # unraveling results to array and converting to list
    all_temps = list(np.ravel(all_results))

    # creating json object of all temps in list
    return jsonify(all_temps)


if __name__ == '__main__':
    app.run()
