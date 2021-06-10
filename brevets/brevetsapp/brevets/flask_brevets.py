"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
import os
from flask import request, redirect, url_for, render_template
from pymongo import MongoClient
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.tododb
CONFIG = config.configuration()

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')

@app.route("/submitroute", methods= ['POST'])
def submitroute():
    app.logger.debug("MADE IT TO SUB")
    mydata = flask.request.get_json(force=True)
    for row in mydata:
        item_doc = {
                'km': row[0],
                'open_time': row[1],
                'close_time': row[2]
             }
        app.logger.debug(item_doc) 
        #app.logger.debug("km type", type(request.form['km']))
        #app.logger.debug("km", request.form['km'])
        db.tododb.insert_one(item_doc)
    return redirect(url_for('index'))

@app.route("/displayroute")
def diplayroute():
    app.logger.debug("DISPLAy")
    items = list(db.tododb.find())
    app.logger.debug(items)
    return render_template('display.html', items=list(db.tododb.find()))

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404



###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet_dist_km = request.args.get('brevet_dist_km', type=int)
    start = request.args.get('begin_date')
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME!
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!
    open_time = acp_times.open_time(km, brevet_dist_km, arrow.get(str(start))).format('YYYY-MM-DDTHH:mm')

    close_time = acp_times.close_time(km, brevet_dist_km, arrow.get(str(start))).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############


app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
