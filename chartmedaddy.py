# -*- coding: utf-8 -*- 

import chart_studio.tools as tls
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

md_str = u"\n"
iframe_tag = u"<iframe id=\"chart-iframe\" scrolling=\"no\" style=\"margin:0; border:none; overflow:hidden;\" seamless=\"seamless\" src=\"{}\" height=\"525\" width=\"100%\" onload=\"AdjustIframeHeightOnLoad()\"></iframe>"

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


def std_layout(index=u"indices comparison", yaxis=u"price"):
	return {
		u"title": go.layout.Title(
			text=index,
			xref=u"paper",
			x=0
		),
		u"xaxis": go.layout.XAxis(
			title=go.layout.xaxis.Title(
				text=u"date"
			)
		),
		u"yaxis": go.layout.YAxis(
			title=go.layout.yaxis.Title(
				text=yaxis
			)
		)
	}


def generate_md_index(index, link_candlestick, link_mountain):
	global md_str
	md_str += u"### {}\n\n{}\n\ncomponent|weight\n---------|------\n".format(index, portfolios.indices[index][1])
	tickers = portfolios.indices[index][0].keys()
	tickers.sort()
	md_str += u"{}\n\n".format(u'\n'.join([u"{}|{}".format(ticker, portfolios.indices[index][0][ticker]) for ticker in tickers]))
	md_str += u"{} candlestick chart:\n\n{}\n\n{} mountain chart:\n\n{}\n\n".format(index, iframe_tag.format(link_candlestick), index, iframe_tag.format(link_mountain))


def generate_md_comparison(link_comparison):
	global md_str
	md_str += u"### performance comparison between indices:\n{}\n\n".format(iframe_tag.format(link_comparison))


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
	
	data_layout.update_layout(std_layout(yaxis=u"percent change"))
	# data_layout.update_layout(std_slider, xaxis_range=[trading_days[0], trading_days[-1]], title_text=u"comparisons")
	
	filename = os.path.join(DirectoryElements.plots_subdir, u"comparison.html")
	
	plotly.offline.plot(
		data_layout,
		filename=filename,
		auto_open=False,
		image_filename=u"all mountain",
		include_mathjax=u"cdn",
		auto_play=False
	)
	
	return filename


def plot_mountain(index):
	data_layout = go.Figure(
		data=[
			go.Scattergl(
				{
					u"x": indices_ohlcvs[index].index,
					u"y": indices_ohlcvs[index][col_c],
					u"name": index,
					u"opacity": 0.8,
					u"mode": u"lines",
					u"fill": u"tozeroy"
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
	
	data_layout.update_layout(std_layout(index=index))
	data_layout.update_layout(xaxis_rangeslider_visible=True)
	
	# data_layout.update_layout(std_slider, xaxis_range=[trading_days[0], trading_days[-1]])
	
	filename = os.path.join(DirectoryElements.plots_subdir, index + u" mountain.html")
	
	plotly.offline.plot(
		data_layout,
		filename=filename,
		auto_open=False,
		image_filename=index + u" mountain",
		include_mathjax=u"cdn",
		auto_play=False
	)
	
	return filename


def plot_candlestick(index):
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
	
	data_layout.update_layout(std_layout(index=index))
	
	filename = os.path.join(DirectoryElements.plots_subdir, index + u" candlestick.html")
	
	plotly.offline.plot(
		data_layout,
		filename=filename,
		auto_open=False,
		image_filename=index + u" candlestick",
		include_mathjax=u"cdn",
		auto_play=False
	)
	
	return filename


def plot_all():
	global md_str
	md_str += u"## Fantasy Indices\n\nThe following are the descriptions and performances of indices currently tracked by this project. This section is automatically generated whenever the indices are updated. charts might not show up because of [this](https://github.github.com/gfm/#disallowed-raw-html-extension-).\n"
	
	indices = portfolios.indices.keys()
	indices.sort()
	
	for index in indices:
		link_candlestick = plot_candlestick(index)
		link_mountain = plot_mountain(index)
		generate_md_index(index, link_candlestick, link_mountain)
	
	link_comparison = plot_comparison(indices)
	generate_md_comparison(link_comparison)


def track(index):
	weight = pandas.DataFrame.from_dict({symbol: [portfolios.indices[index][0][symbol]] for symbol in portfolios.indices[index][0].keys()})
	data = {trading_day: weight.dot(pandas.read_csv(os.path.join(directory_elements.indices_dirs[index], trading_day)).set_index(symbol_column)[ohlcv_cols]).sum(axis=0).to_dict() for trading_day in trading_days}
	return pandas.DataFrame.from_dict(data, orient=u"index")


trading_days = os.walk(directory_elements.EODs_dir).next()[-1]
trading_days.sort()

indices_ohlcvs = {index: track(index) for index in portfolios.indices.keys()}

plot_all()

md_file = open(u"indices.md", u'w')
md_file.write(md_str.encode(u"utf8"))
md_file.close()
