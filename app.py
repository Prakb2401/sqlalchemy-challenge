import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import datetime, timedelta
from flask import Flask, jsonify

# SQLALCHEMY engine creation
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#Flask Setup
app=Flask(__name__)

#Variables
Recent1 = "2017-08-23"
date_precipitation = dt.date (2017,8,23) - dt.timedelta(days = 365)
station_counter = func.count(Measurement.station)
Station_Activity = session.query(Measurement.station, station_counter).group_by(Measurement.station).order_by(station_counter.desc()).all()
print(Station_Activity)
session.close()
#Flask Routes
@app.route("/")
def welcome():
    return(
        f"/api/v1.0/precipitation"    
        f"/api/v1.0/stations"    
        f"/api/v1.0/tobs"   
        f"/api/v1.0/<start>  date format mm-dd-yyyy"     
        f"/api/v1.0/<start>/<end>  date format mm-dd-yyyy"  
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    query=session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= date_precipitation).\
        order_by(Measurement.date).all()
    session.close()

    precipitations = []
    for date, prcp in query:
        precipitation_dict ={}
        precipitation_dict["prcp"]= prcp
        precipitation_dict["date"]= date
        precipitations.append(precipitation_dict)

    return jsonify(precipitations)


@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    query=session.query(Station.station).all()
    session.close()
    query_list = list(np.ravel(query))
    return jsonify(query_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs1 = session.query(Measurement.tobs).order_by(Measurement.date).\
        filter(Measurement.date >= date_precipitation)
    session.close()
    tobs_list = list(np.ravel(tobs1))
    return jsonify(tobs_list)

if __name__ == '__main__':
    app.run(debug=True)