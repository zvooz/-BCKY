# -*- coding: utf-8 -*- 

import copy
import datetime
from dateutil import rrule, parser
from ftplib import FTP
from typing import List, Any
from directoryelements import DirectoryElements
import json
import multiprocessing
import multiprocessing.dummy as mpd
import os
import pandas
from portfolios import Portfolios
from progressbar import ProgressBar
import requests
import sys
import time

testing = False  # True for development and testing, False for production
poolsize = multiprocessing.cpu_count()  # make my cpu cry!

NASDAQ_ftp = u"ftp.nasdaqtrader.com"
NASDAQ_crosses_dir = u"files/crosses"

credentials = u"credentials"
IEX_baseurl = u"https://cloud.iexapis.com/stable"
IEX_testurl = u"https://sandbox.iexapis.com/stable"
get_stock = u"/stock/"
get_date = u"/chart/date/"
query_parameters = {u"chartByDay": u"true"}  # this gets only the daily OHLCV data

empty_response = {
	u"date": u"",
	u"open": 0,
	u"high": 0,
	u"low": 0,
	u"close": 0,
	u"volume": 0,
	u"uOpen": 0,
	u"uHigh": 0,
	u"uLow": 0,
	u"uClose": 0,
	u"uVolume": 0,
	u"change": 0,
	u"changePercent": 0,
	u"label": u"",
	u"changeOverTime": 0
}

symbol_column = u"symbol"
columns_to_remove = [
	u"label",
	u"date"
]

portfolios = Portfolios()
directory_elements = DirectoryElements()
progress_bar = ProgressBar(progress_report_count=2)


def get_trading_days_all(ftp):
	templist = []
	
	for filename in ftp.nlst()[2:]:
		try:
			templist.append(datetime.datetime.strptime(filename, u"CrossStats%Y%m%d.txt").date())
		except Exception:
			continue
			
	templist.sort()
	
	if len(templist) > 0:
		del templist[-1]
	
	return set(templist)


def get_trading_days():
	trading_days_processed = set(
		[datetime.datetime.strptime(EOD, u"%Y-%m-%d").date() for EOD in os.walk(directory_elements.EODs_dir).next()[-1]])

	trading_days_unprocessed = set([
		datetime_object.date() for datetime_object in list(
			rrule.rrule(
				rrule.DAILY,
				dtstart=portfolios.epoch,
				until=datetime.date.today()
			)
		)
	])

	ftp = FTP(NASDAQ_ftp)
	ftp.login()
	ftp.cwd(NASDAQ_crosses_dir)
	
	trading_days_all = get_trading_days_all(ftp)

	trading_days_unprocessed = list(trading_days_unprocessed.intersection(trading_days_all) - trading_days_processed)
	trading_days_unprocessed.sort()

	return trading_days_unprocessed


def get_credentials():
	with open(credentials, u'r') as credentials_file:
		credentials_data = credentials_file.read()
		credentials_json = json.loads(credentials_data)

	tokens = credentials_json[u"tokens" if not testing else u"test tokens"]

	token = str(tokens[u"publishable token"])
	if not token:
		token = str(tokens[u"secret token"])
		if not token:
			progress_bar.err_report(u"no tokens available")
			exit(1)

	return token


# def query_thread(symbol):
# 	global EOD_ohlcv
# 	global indices_ohlcvs
#
# 	symbol_ohlcv = json.loads(
# 		requests.get((IEX_baseurl if not testing else IEX_testurl) + get_stock + symbol + get_date_query, params=query_parameters).text)[0]
# 	for column in columns_to_remove:
# 		del symbol_ohlcv[column]
# 	symbol_ohlcv[symbol_column] = symbol
#
# 	EOD_ohlcv.append(symbol_ohlcv)
# 	for index in portfolios.indices.keys():
# 		if symbol in indices_components[index]:
# 			indices_ohlcvs[index].append(symbol_ohlcv)
#
# 	time.sleep(0.05)


def dict_to_DataFrame(BCKY_dict):
	BCKY_df = pandas.DataFrame(BCKY_dict)
	BCKY_df_columns = BCKY_df.columns.tolist()
	BCKY_df_columns.remove(symbol_column)
	BCKY_df_columns.insert(0, symbol_column)
	BCKY_df = BCKY_df[BCKY_df_columns]
	BCKY_df.sort_values(by=symbol_column)
	return BCKY_df


def pd_to_csv(file_path, pd):
	if os.path.isfile(file_path):
		pd.to_csv(file_path, mode=u'a', header=False, index=False)
	else:
		pd.to_csv(file_path, index=False)


query_parameters[u"token"] = get_credentials()

indices_components = {index: set(portfolios.indices[index].keys()) for index in portfolios.indices.keys()}
symbols = set.union(*indices_components.values())

days_iter = 0

big_start_time = datetime.datetime.now()

trading_days = get_trading_days()
for trading_day in trading_days:
	progress_bar.out(days_iter, len(trading_days), start_time=big_start_time, prefix=trading_day, suffix=u"done", decimals=2, position=0)
	
	get_date_query = get_date + trading_day.strftime(u"%Y%m%d")
	
	indices_ohlcvs = {index: [] for index in portfolios.indices.keys()}
	EOD_ohlcv = []
	
	u"""
	unsuccessful multi-threaded implementation
	"""
	# if symbols:
	# 	if __name__ == '__main__':
	# 		trading_days_pool = mpd.Pool(poolsize)
	# 		trading_days_pool.map(query_thread, symbols)
	# 	trading_days_pool.join()
	
	u"""
	in the following try
	waste some data here to ensure data integrity
	use SPY, because if SPY isn't there, then market isn't there
	"""
	try:
		SPY_ohlcv = json.loads(
			requests.get((IEX_baseurl if not testing else IEX_testurl) + get_stock + u"SPY" + get_date_query, params=query_parameters).text)
	except Exception:
		progress_bar.wrn_report(u"No $SPY data on {}. Is it not a trading day?\n".format(trading_day.isoformat()))
		days_iter += 1
		continue

	if not SPY_ohlcv:
		progress_bar.wrn_report(u"No valid $SPY data on {}.\n\tIs it a not trading day?\n\tOr, maybe IEX just hasn't updated the data yet?\n".format(trading_day.isoformat()))
		days_iter += 1
		continue

	symbol_iter = 0

	small_start_time = datetime.datetime.now()

	for symbol in symbols:
		progress_bar.out(symbol_iter, len(symbols), start_time=small_start_time, prefix=symbol, suffix=u"done", decimals=2, position=1)
		
		try:
			symbol_ohlcv = json.loads(
				requests.get((IEX_baseurl if not testing else IEX_testurl) + get_stock + symbol + get_date_query, params=query_parameters).text)[0]
			if not symbol_ohlcv:
				symbol_ohlcv = empty_response
		except Exception:
			symbol_ohlcv = empty_response
		
		# if symbol == u"BYND":
		# 	print symbol_ohlcv

		for column in columns_to_remove:
			if column in symbol_ohlcv:
				del symbol_ohlcv[column]
		symbol_ohlcv[symbol_column] = symbol

		EOD_ohlcv.append(symbol_ohlcv)
		for index in portfolios.indices.keys():
			if symbol in indices_components[index]:
				indices_ohlcvs[index].append(symbol_ohlcv)
		
		symbol_iter += 1
		
		time.sleep(0.025)
	
	progress_bar.out(symbol_iter, len(symbols), start_time=small_start_time, prefix=symbol, suffix=u"done", decimals=2, position=1)

	if EOD_ohlcv:
		EOD_df = dict_to_DataFrame(EOD_ohlcv)
		pd_to_csv(os.path.join(directory_elements.EODs_dir, trading_day.isoformat()), EOD_df)
	
	for index in portfolios.indices.keys():
		pd_to_csv(os.path.join(directory_elements.indices_dirs[index], trading_day.isoformat()), dict_to_DataFrame(indices_ohlcvs[index]))
	
	days_iter += 1
	
	time.sleep(0.025)

progress_bar.out(days_iter, len(trading_days), start_time=big_start_time, prefix=trading_day, suffix=u"done", decimals=2, position=0)
