# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///SurfsUp/Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
        return (f'All available route:<br/>'
                f'/api/v1.0/precipitation<br/>'
                f'/api/v1.0/stations<br/>'
                f'/api/v1.0/tobs<br/>'
                f'/apiv1.0/2010-01-23<br/>'
                f'/api/v1.0/2010-01-23/2010-08-23'
                )

@app.route("/api/v1.0/precipitation")
def prcp():
    date = dt.date(2017,8,23) - dt.timedelta(days=365)

    prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= date).all()
    
    session.close()

    prcp_dict = {key: value for key, value in prcp}
    
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
      stations = session.query(Measurement.station).group_by(Measurement.station).all()

      stations_list = list(np.ravel(stations))

      session.close()

      return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    date = dt.date(2017,8,23) - dt.timedelta(days=365)

    tobs = session.query(Measurement.date,Measurement.tobs).\
    filter(Measurement.date >= date).\
        filter(Measurement.station == 'USC00519281').all()
    
    tobs_list = list(np.ravel(tobs))

    session.close()

    return jsonify(tobs_list)

@app.route("/apiv1.0/2010-01-23")
def start():
     start = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= '2010-01-23').all()
     
     start_list = list(np.ravel(start))

     session.close()

     return jsonify(start_list)

@app.route("/apiv1.0/2010-01-23/2010-08-23")
def start_end():
      start_end = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= '2010-01-23').\
                filter(Measurement.date <= '2010-08-23').all()
      
      start_end_list = list(np.ravel(start_end))

      session.close()

      return jsonify(start_end_list)
   
if __name__ == '__main__':
      app.run(debug=True)