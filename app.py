import logging
import pandas as pd
import requests
import os
#import plotly
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import file_html
from flask import Flask, render_template, request, redirect
from calendar import monthrange

app = Flask(__name__)
app.config['DEBUG'] = True
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers


@app.route('/')
def index():
  #return render_template('index.html') #TODO remove
  return render_template('form.html')


@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/fun_api')
def fun_api():

  api_key = os.environ.get("AAP_ALPHA_API_KEY")
  query_params = {
    'adjusted': True, 
    'sorat': 'sc', 
    'limit': '120',
    'apiKey': api_key
   }

  ticker = 'AAPL'
  year = 2021
  month = '07'
  days = 30
  # TODO - for number of days in month and month is 2 digits
  url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{year}-{month}-01/2021-{month}-{days}'

  r = requests.get(url,
    params=query_params
  )

  stock_data = r.json()
  stock_data_prices = stock_data.get("results")
  df = pd.DataFrame(stock_data_prices)

  print(df)

  html = chart_draw(df, ticker, year, month)

  return html


def chart_draw(df, ticker, year, month):

  day_number = df.index
  close_prices = df["c"]
  
  graph_title = f'Graph of {ticker} for {month} of {year}'

  p = figure(title=graph_title, x_axis_label='Day', y_axis_label='Stock Price')
  p.line(day_number, close_prices, legend_label="Close Stock price", line_width=2)
  
  html = file_html(models=p, resources=CDN, title="Stock plot")
  # html = file_html(models=p, resources=CDN, title="Stock plot", template='full_layout.html')

  return html


def retrieve_ticker_data(ticker, year, month):
  api_key = os.environ.get("AAP_ALPHA_API_KEY")
  query_params = {
    'adjusted': True, 
    'sorat': 'sc', 
    'limit': '120',
    'apiKey': api_key
   }

  # finds the number of days in that month
  _, days = monthrange(int(year), int(month))
  url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{year}-{month}-01/2021-{month}-{days}'

  r = requests.get(url,
    params=query_params
  )

  stock_data = r.json()
  # print(stock_data)
  stock_data_prices = stock_data.get("results")
  df = pd.DataFrame(stock_data_prices)

  return df


@app.route('/get_chart')
def getchart():
  """
    Gets the query params
    Calls Alpha Vantag API to retrieve Data for that month
    Renders Line Chart in Bokeh of the Stock prices
  """
  # get_chart?tickername=AAPL&year=2021&month=12
  ticker_name = request.args.get('tickername')
  year = request.args.get('year')
  month = request.args.get('month')

  app.logger.info(f"GETTING CHART for {ticker_name} for year: {year} and month {month}")

  df = retrieve_ticker_data(ticker_name, year, month)
  # print(df)

  html = chart_draw(df, ticker_name, year, month)

  app.logger.info(f"DONE getting chart for {ticker_name} for year: {year} and month {month}")

  return html

if __name__ == '__main__':
  app.run(port=33507)
