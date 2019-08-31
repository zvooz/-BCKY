# -*- coding: utf-8 -*- 

import datetime
from directoryelements import DirectoryElements
import os
import pandas
import plotly
import plotly.graph_objs as go
from portfolios import Portfolios
from progressbar import ProgressBar

# date_column		= u"date"
col_o = u"open"
col_h = u"high"
col_l = u"low"
col_c = u"close"
col_v = u"volume"
ohlcv_cols = [col_o, col_h, col_l, col_c, col_v]
symbol_column = u"symbol"

portfolios = Portfolios()
directory_elements = DirectoryElements()
progress_bar = ProgressBar(progress_report_count=2)


# std_slider = {
# 	"xaxis": [
# 		go.layout.XAxis(
# 			{
# 				"rangeselector": {
# 					"buttons": [
# 						{
# 							"count": 1,
# 							"label": "1m",
# 							"step": "month",
# 							"stepmode": "backward"
# 						},
# 						{
# 							"count": 6,
# 							"label": "6m",
# 							"step": "month",
# 							"stepmode": "backward"
# 						},
# 						{
# 							"count": 1,
# 							"label": "YTD",
# 							"step": "month",
# 							"stepmode": "backward"
# 						},
# 						{
# 							"count": 1,
# 							"label": "1y",
# 							"step": "year",
# 							"stepmode": "backward"
# 						},
# 						{
# 							"step": "all"
# 						}
# 					]
# 				},
# 				"rangeslider": {"visible": True},
# 				"type": "date"
# 			}
# 		)
# 	]
# }


def plot_comparison(indices):
	data_layout = go.Figure(
		layout={
			u"xaxis": {
				u"title": u"date"
			},
			u"yaxis": {
				u"title": u"change",
				u"tickformat": u".2%"
			},
			u"title": {u"text": u"Indices Comparison"}
		}
	)
	
	for index in indices:
		data_layout.add_trace(
			go.Scatter(
				{
					u"x": indices_ohlcvs[index].index,
					u"y": (indices_ohlcvs[index][col_c] / indices_ohlcvs[index][indices_ohlcvs[index][col_c] > 0][col_c].iloc[0]).where(indices_ohlcvs[index][col_c] > 0, 1) - 1,
					u"name": index,
					u"opacity": 0.8,
					u"mode": u"lines"
				}
			)
		)
	
	# data_layout.update_layout(std_slider, xaxis_range=[trading_days[0], trading_days[-1]], title_text=u"comparisons")
	
	plotly.offline.plot(
		data_layout,
		filename=DirectoryElements.plots_dir + u"/comparison.html",
		auto_open=False,
		image_filename=u"all mountain",
		include_mathjax=u"cdn",
		auto_play=False
	)


def plot_mountains(index):
	data_layout = go.Figure(
		data=[
			go.Scattergl(
				{
					u"x": indices_ohlcvs[index].index,
					u"y": indices_ohlcvs[index][col_c],
					u"name": index,
					u"opacity": 0.8,
					u"mode": u"lines"
				}
			)
		],
		layout={
			u"xaxis": {
				u"title": u"date"
			},
			u"yaxis": {
				u"title": u"price"
			},
			u"title": {u"text": index}
		}
		
	)
	
	# data_layout.update_layout(std_slider, xaxis_range=[trading_days[0], trading_days[-1]])
	
	plotly.offline.plot(
		data_layout,
		filename=DirectoryElements.plots_dir + u'/' + index + u" mountain.html",
		auto_open=False,
		image_filename=index + u" mountain",
		include_mathjax=u"cdn",
		auto_play=False
	)


def plot_candlesticks(index):
	data_layout = go.Figure(
		data=[
			go.Candlestick(
				{
					u"x": indices_ohlcvs[index].index,
					u"open": indices_ohlcvs[index][col_o],
					u"high": indices_ohlcvs[index][col_h],
					u"low": indices_ohlcvs[index][col_l],
					u"close": indices_ohlcvs[index][col_c],
					u"name": index
				}
			)
		]
	)
	
	plotly.offline.plot(
		data_layout,
		filename=DirectoryElements.plots_dir + u'/' + index + u" candlestick.html",
		auto_open=False,
		image_filename=index + u" candlestick",
		include_mathjax=u"cdn",
		auto_play=False
	)


def plot_all():
	indices = portfolios.indices.keys()
	indices.sort()
	
	for index in indices:
		plot_candlesticks(index)
		plot_mountains(index)
	
	plot_comparison(indices)


def track(index):
	weight = pandas.DataFrame.from_dict({symbol: [portfolios.indices[index][symbol]] for symbol in portfolios.indices[index].keys()})
	data = {trading_day: weight.dot(pandas.read_csv(os.path.join(directory_elements.indices_dirs[index], trading_day)).set_index(symbol_column)[ohlcv_cols]).sum(axis=0).to_dict() for trading_day in trading_days}
	return pandas.DataFrame.from_dict(data, orient=u"index")


trading_days = os.walk(directory_elements.EODs_dir).next()[-1]
trading_days.sort()

indices_ohlcvs = {index: track(index) for index in portfolios.indices.keys()}

plot_all()
