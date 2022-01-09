from flask import Flask, render_template, request, redirect
import requests
#import plotly
from bokeh.plotting import figure
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
  r = requests.get('https://api.github.com/anastasia-pashkova')
  return r.json()


  #return "OK!"

@app.route('/chart_draw')
def chart_draw():
  plot = figure()
  plot.circle([1,2], [3,4])
  html = file_html(plot, CDN, "my plot")
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
