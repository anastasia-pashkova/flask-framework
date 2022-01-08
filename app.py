from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
  #return render_template('index.html') #TODO remove
  return render_template('form.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/get_chart')
def getchart():
  # TODO get query params
  # TODO call API to get data
  # TODO render chart
  return "GETTING CHART ..."

if __name__ == '__main__':
  app.run(port=33507)
