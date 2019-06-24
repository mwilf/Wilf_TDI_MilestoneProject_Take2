###https://github.com/realpython/flask-bokeh-example/blob/master/tutorial.md

from flask import Flask, render_template, request, url_for, redirect
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.models import ColumnDataSource, DatetimeTickFormatter 
import datetime as dt
import pandas as pd
import pandas_datareader
#import pandas_datareader.data as web #how we're going to grab data and put it into pandas
#from math import pi
#import quandl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

#https://www.youtube.com/watch?time_continue=41&v=hAEJajltHxc
#How to process incoming requests

@app.route('/example', methods=['POST'])
def example():
    ticker = (request.form['ticker'])#new
    start = dt.datetime(2019,1,1)
    end = dt.datetime(2019,1,31)
    #start = "2017-01-01"
    #end = "2017-01-21"
    
    #PULL DATA FROM WEB
    df = pandas_datareader.DataReader(ticker, 'yahoo', start, end) #TSLA = tesla
    #df = quandl.get("WIKI/%s" % ticker, start_date=start, end_date=end)
    ds = ColumnDataSource(df) #allows for calling the date as index below
    #output_file("lines.html") ##if using this, add "from bokeh.plotting import figure, **output_file**, show
    
    TOOLS="hover,crosshair,pan,wheel_zoom,box_zoom,reset,tap,save,box_select,poly_select,lasso_select"
    p = figure(title="Stock price (adjusted close) for ticker '" + ticker + "', 2019 Jan 1 - 2019 Jan 31", x_axis_type='datetime', x_axis_label='Date', y_axis_label='Adjusted Closing Price', tools=TOOLS)
    p.xaxis.formatter=DatetimeTickFormatter(
            hours=["%d %B %Y"],
            days=["%d %B %Y"],
            months=["%d %B %Y"],
            years=["%d %B %Y"],
        )
    p.xaxis.major_label_orientation = 3.141592/4
    p.line(source=ds, x='Date', y='Adj Close')
    p.circle(source=ds, x='Date', y='Adj Close')


    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(p)
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)
    

if __name__ == "__main__":
    app.run()
