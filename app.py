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

@app.route("/")
def welcome():
    return (
        f'Welcome to the Hawaii climate analysis site!<br/>'
        f'Below are the available API routes:<br/>'
        f'api/v1.0/precipitation<br/>'
        f'api/v1.0/stations<br/>'
        f'api/v1.0/tobs<br/>'
        f'api/v1.0/temp/<start'
        f'api/v1.0/temp<start>/<end>'
    )

@app.route("/api/v1.0/precipitaton")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date <="2017-08-23")\
    .filter(Measurement.date >="2016-08-23").all()

    temps = list(np.ravel(results))

    return(jsonify(temps)
    )

# @app.route("/api/v1.0/stations")

# @app.route("/api/v1.0/tobs")

if __name__ == '__main__':
    app.run()
