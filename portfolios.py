# -*- coding: utf-8 -*- 

import datetime


class Portfolios:
	def __init__(self):
		pass
	
	epoch = datetime.date(2019, 3, 28)
	
	# MC = u"MC.PA"
	MC = u"LVMHF"
	# OR = u"OR.PA"
	OR = u"LRLCF"
	
	# ^BCKY.A or ^BCKYA, the primary ^BCKY portfolio
	BCKY_A = {
		u"AAPL"	: 5,
		u"ETSY"	: 15,
		u"LULU"	: 6,
		MC		:	3,
		OR		:	4,
		u"PLNT"	:	15,
		u"SBUX"	:	14,
		u"ULTA"	:	3
	}

	# ^BCKY.B or ^BCKYB, the secondary ^BCKY portfolio, a superset of ^BCKY.A or ^BCKYA
	BCKY_B = {
		u"COTY"	:	87,
		u"DECK"	:	7,
		u"DEO"	:	6,
		u"EL"	:	6,
		u"LB"	:	36,
		u"FIZZ"	:	18,
		u"NFLX"	:	3,
		u"NKE"	:	12,
		u"SNAP"	:	93,
		u"TGT"	:	12,
		u"TIF"	:	10,
		u"UAA"	:	47,
		u"VFC"	:	11
	}
	BCKY_B.update(BCKY_A)

	# ^BCKY.V or ^BCKYV, the Founders Edition
	BCKY_V = {
		# US equities, original
		u"AAPL"	:	5,
		u"DECK"	:	7,
		u"DIS"	:	9,
		u"EL"	:	6,
		u"FB"	:	6,
		u"LB"	:	36,
		u"LULU"	:	6,
		u"NKE"	:	12,
		u"SBUX"	:	14,
		u"UAA"	:	47,
		u"ULTA"	:	3,

		# non-US equities, original
		u"ADDYY":	8,
		u"DEO"	:	6,
		u"LRLCY":	19,
		u"LVMUY":	14,

		# community consensus
		u"ETSY"	:	15,
		u"FIZZ"	:	18,
		u"GOOS"	:	21,
		u"NFLX"	:	3,
		u"SNAP"	:	93,
		u"TGT"	:	12,
		u"TIF"	:	10
	}
	
	# ^RTRD, the r/WallStreetBets Retard Portfolio
	RTRD = {
		u"BYND"	:   22
	}
	
	SPY = {
		u"SPY"	: 1
	}
	
	indices = {
		u"^BCKY.A"	: BCKY_A,
		u"^BCKY.B"	: BCKY_B,
		u"^BCKY.V"	: BCKY_V,
		u"^RTRD"	: RTRD,
		u"$SPY"		: SPY
	}