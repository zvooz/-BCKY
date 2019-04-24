# -*- coding: utf-8 -*- 

import datetime
from directoryelements import DirectoryElements
from matplotlib.dates import FRIDAY, DateFormatter, MonthLocator, WeekdayLocator, date2num
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
# from matplotlib.pyplot import figure
from mpl_finance import candlestick_ohlc
import os
import pandas
from portfolios import Portfolios



SPY		= "SPY"
BCKY_A	= "BCKY.A"
BCKY_B	= "BCKY.B"
BCKY_V	= "BCKY.V"

date_column		= u"date"
symbol_column	= u"symbol"
close_column	= u"close"
OHLC_columns	= [u"open", u"high", u"low", u"close"]

portfolios = Portfolios()
directory_elements = DirectoryElements()



def get_close(BCKY, df):
	close = 0
	for index, row in df.iterrows():
		close += float(row[close_column]) * BCKY[row[symbol_column]]
	return close


		
def get_OHLC(BCKY, df):
	OHLC = [0, 0, 0, 0]
	for index, row in df.iterrows():
		for i in range(4):
			OHLC[i] += float(row[OHLC_columns[i]]) * BCKY[row[symbol_column]]
	return OHLC



def get_EOD_data(BCKY, BCKY_dir):
	BCKY_close = []
	BCKY_OHLC = []

	for trading_day in trading_days:
		BCKY_df = pandas.read_csv(os.path.join(BCKY_dir, trading_day))

		BCKY_close.append(get_close(BCKY, BCKY_df))
		BCKY_OHLC.append(get_OHLC(BCKY, BCKY_df))

	return (BCKY_close, BCKY_OHLC)



def set_font():
	font = {"size": 4}
	matplotlib.rc("font", **font)



def plot_mountains(indices, names):
	colors = ["#9D67E5", "#678fE5", "#6DE567", "#E5A067"]

	fridays = WeekdayLocator(FRIDAY)
	daysFmt = DateFormatter("%Y-%m-%d")

	fig, ax = plt.subplots()

	for index, name, color in zip(indices, names, colors):
		ax.plot([date2num(datetime.datetime.strptime(day, "%Y-%m-%d")) for day in trading_days], [price / index[0] - 1 for price in index],
			color		= color,
			linestyle	= '-',
			linewidth	= 1,
			alpha		= 0.75
		)	

		# ax.fill_between([date2num(datetime.datetime.strptime(day, "%Y-%m-%d")) for day in trading_days], 0, BCKY_close,
		# 	facecolor	= "#678fE5",
		# 	alpha		= 0.5
		# )

	ax.xaxis.set_major_locator(fridays)
	ax.xaxis.set_major_formatter(daysFmt)
	ax.autoscale_view()
	ax.xaxis.grid(True, "major")
	ax.grid(True)

	y_axis_vals = ax.get_yticks()
	ax.set_yticklabels(['{:,.2%}'.format(x) for x in y_axis_vals])

	fig.set_dpi(300)
	fig.set_figheight(3.375)
	fig.set_figwidth(6)
	fig.suptitle("Comparisons to $SPY", fontsize=8)
	fig.autofmt_xdate()

	plt.legend(names)
	plt.xlabel("Date", fontsize=6)
	plt.ylabel("Percent Change", fontsize=6)
	plt.savefig(os.path.join(directory_elements.plots_dir, "$SPY-lol..."),
		edgecolor	= "#FFFFFF00",
		orientation	= "landscape",
		format		= "png",
		pad_inches	= 0
	)



def plot_mountain(BCKY_close, BCKY_name):
	fridays = WeekdayLocator(FRIDAY)
	daysFmt = DateFormatter("%Y-%m-%d")

	fig, ax = plt.subplots()

	ax.plot([date2num(datetime.datetime.strptime(day, "%Y-%m-%d")) for day in trading_days], BCKY_close,
		color		= "#678fE5",
		linestyle	= '-',
		linewidth	= 1,
		alpha		= 0.75
	)

	# ax.fill_between([date2num(datetime.datetime.strptime(day, "%Y-%m-%d")) for day in trading_days], 0, BCKY_close,
	# 	facecolor	= "#678fE5",
	# 	alpha		= 0.5
	# )

	ax.xaxis.set_major_locator(fridays)
	ax.xaxis.set_major_formatter(daysFmt)
	ax.autoscale_view()
	ax.xaxis.grid(True, "major")
	ax.grid(True)

	fig.set_dpi(300)
	fig.set_figheight(3.375)
	fig.set_figwidth(6)
	fig.suptitle("{} Mountain Chart".format(BCKY_name), fontsize=8)
	fig.autofmt_xdate()

	plt.xlabel("Date", fontsize=6)
	plt.ylabel("End-of-Day Quote", fontsize=6)
	plt.savefig(os.path.join(directory_elements.plots_dir, "{}-Mountain".format(BCKY_name)),
		edgecolor	= "#FFFFFF00",
		orientation	= "landscape",
		format		= "png",
		pad_inches	= 0
	)


def plot_OHLC(BCKY_OHLC, BCKY_name):
	fridays = WeekdayLocator(FRIDAY)
	daysFmt = DateFormatter("%Y-%m-%d")

	fig, ax = plt.subplots()

	quotes = []
	for day, OHLC in zip(trading_days, BCKY_OHLC):
		OHLC.insert(0,date2num(datetime.datetime.strptime(day, "%Y-%m-%d")))
		quotes.append(OHLC)

	candlestick_ohlc(ax, quotes,
		colorup		= 'g',
		colordown	= 'r',
		alpha		= 0.75
	)

	ax.xaxis.set_major_locator(fridays)
	ax.xaxis.set_major_formatter(daysFmt)
	ax.autoscale_view()
	ax.xaxis.grid(True, "major")
	ax.grid(True)

	fig.set_dpi(300)
	fig.set_figheight(3.375)
	fig.set_figwidth(6)
	fig.suptitle("{} Candlestick Chart".format(BCKY_name), fontsize=8)
	fig.autofmt_xdate()

	plt.xlabel("Date", fontsize=6)
	plt.ylabel("End-of-Day Quote", fontsize=6)
	plt.savefig(os.path.join(directory_elements.plots_dir, "{}-OHLC".format(BCKY_name)),
		edgecolor	= "#FFFFFF00",
		orientation	= "landscape",
		format		= "png",
		pad_inches	= 0
	)



trading_days = os.walk(directory_elements.EODs_dir).next()[-1]
trading_days.sort()

(BCKY_A_close, BCKY_A_OHLC) = get_EOD_data(portfolios.BCKY_A, directory_elements.BCKY_A_dir)
(BCKY_B_close, BCKY_B_OHLC) = get_EOD_data(portfolios.BCKY_B, directory_elements.BCKY_B_dir)
(BCKY_V_close, BCKY_V_OHLC) = get_EOD_data(portfolios.BCKY_V, directory_elements.BCKY_V_dir)

set_font()

plot_OHLC(BCKY_A_OHLC, BCKY_A)
plot_OHLC(BCKY_B_OHLC, BCKY_B)
plot_OHLC(BCKY_V_OHLC, BCKY_V)

plot_mountain(BCKY_A_close, BCKY_A)
plot_mountain(BCKY_B_close, BCKY_B)
plot_mountain(BCKY_V_close, BCKY_V)

SPY_df = pandas.read_csv(os.path.join(directory_elements.portfolios_dir, SPY))
SPY_df.sort_values(by = date_column)
SPY_close = SPY_df[close_column].tolist()

plot_mountains(
	[
		BCKY_A_close,
		BCKY_B_close,
		BCKY_V_close,
		SPY_close
	],
	[
		BCKY_A,
		BCKY_B,
		BCKY_V,
		SPY
	]
)
