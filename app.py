# App that takes ticket number
from flask import Flask, render_template, request
import requests
import datetime
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show, save


app = Flask(__name__)

def plot_ticket(symbol, days):
	
	now = datetime.datetime.now()
	start_date = now + datetime.timedelta(-days)
	end_date = now.strftime('%Y-%m-%d')
	start_date = start_date.strftime('%Y-%m-%d')
	print  (start_date, ' to ', end_date)






	# preprocessing
	symbol = symbol.upper()
	url0  = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json' % symbol



	pars  = {'column_index':'4',
			 'start_date': start_date, 
			 'end_date': now,
			 'collapse': 'daily',    # none, daily, weekly, monthly, quarterly, annual
			 'transform': 'none',    # none, diff, rdiff, rdiff_from, cumul, normalize
			 'api_key':'fj2gQaWni8TeZ78qXSqh'}


	r = requests.get(url0, params=pars)


	dataset = r.json()['dataset']
	data = dataset['data']

	data_np = np.array(data)

	df = pd.DataFrame(data_np, columns=dataset['column_names'])
	df.Close  = pd.to_numeric(df.Close)
	df.index = pd.to_datetime(df.Date)
	df = df.drop('Date', axis=1)


	# p = df.plot(style = '--o', label = symbol, x_compat=True)
	# 
	# plt.ylabel(symbol)
	# p.set_xticks(p.get_xticks()[::2])
	# plt.grid(True)
	# plt.show()


	#######



	# output to static HTML file
	output_file("templates/lines.html")

	# create a new plot with a title and axis labels
	p = figure( title="Close price for the last __ calendar days", 
				x_axis_label='Date', 
				y_axis_label=symbol,
				x_axis_type="datetime")
	# add a line renderer with legend and line thickness
	p.line( df.index,df.Close, legend=symbol+'-close', line_width=1, 
			line_dash="4 4", line_color="orange")
	p.circle(df.index, df.Close,  fill_color="red", size=6)
	# show the results
	save(p)
# 	return render_template("lines.html")



app.vars = {}
# Index page, no args
# request a form
@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'GET':
		return render_template("index.html")
	else:
		#request was a POST
		app.vars['ticket'] = request.form['ticket']
		app.vars['days'] = int(request.form['days'])
		symbol = 		app.vars['ticket']
		days =   		app.vars['days']
		print 4*'*********'
		print 4*'*********'

		plot_ticket(symbol, days)
		return render_template("lines.html")

# @app.route("/plot/", methods=['POST'])



# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)