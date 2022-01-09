from flask import Flask, render_template, request, redirect
import pandas as pd
import requests
import os
#import plotly
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from bokeh.embed import file_html


app = Flask(__name__)
app.config['DEBUG'] = True

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


  #return "OK!"

def chart_draw(df, ticker, year, month):

  day_number = df.index
  close_prices = df["c"]
  #plot = figure()
  #plot.circle([1,2], [3,4])
  #html = file_html(plot, CDN, "my plot")

  x = [1, 2, 3, 4, 5]
  y = [6, 7, 2, 4, 5]
  
  graph_title = f'Graph of {ticker} for {month} of {year}'

  p = figure(title=graph_title, x_axis_label='Day', y_axis_label='Stock Price')
  p.line(day_number, close_prices, legend_label="Close Stock price", line_width=2)
  
  html = file_html(p, CDN, "Stock plot")

  return html

@app.route('/get_chart')
def getchart():
  # TODO get query params
  # TODO call API to get data
  # TODO render chart
  # get_chart?tickername=AAPL&year=2021&month=12
  ticker_name = request.args.get('tickername')
  year = request.args.get('year')
  month = request.args.get('month')
  return f"GETTING CHART for {ticker_name} for year: {year} and month {month}"

if __name__ == '__main__':
  app.run(port=33507)
