# -*- coding: utf-8 -*- 

import datetime


class Portfolios:
	def __init__(self):
		pass
	
	epoch = datetime.date(2019, 1, 1)
	
	
	# MC = u"MC.PA"
	MC = u"LVMHF"
	# OR = u"OR.PA"
	OR = u"LRLCF"
	
	
	# ^BCKY, the part that's common to all ^BCKY's
	BCKY = {
		# US equities
		u"AAPL"	:	6,
		u"ETSY"	:	22,
		u"LULU"	:	8,
		u"ULTA"	:	4,
		u"SBUX"	:	16,
		
		# non-US equities
		MC		:	3,
		OR		:	4
	}
	
	
	# ^BCKY.BV or ^BCKYBV, common to both ^BCKY.B and ^BCKY.V, but not ^BCKY.A
	BCKY_BV = {
		# US equities
		u"DECK"	:	8,
		u"EL"	:	8,
		u"LB"	:	40,
		u"NKE"	:	14,
		u"UAA"	:	57,
		
		# non-US equities
		u"DEO"	:	7,
		
		# community consensus
		u"FIZZ"	:	14,
		u"NFLX"	:	4,
		u"SNAP"	:	186,
		u"TGT"	:	15,
		u"TIF"	:	13
	}
	
	
	# ^BCKY.A or ^BCKYA, the primary ^BCKY portfolio
	BCKY_A = {
		# US equities
		u"PLNT"	:	19
	}
	BCKY_A.update(BCKY)
	
	
	# ^BCKY.B or ^BCKYB, the secondary ^BCKY portfolio, a superset of ^BCKY.A or ^BCKYA
	BCKY_B = {
		# US equities
		u"COTY"	:	155,
		u"VFC"	:	15
	}
	BCKY_B.update(BCKY_A)
	BCKY_B.update(BCKY_BV)
	
	
	# ^BCKY.V or ^BCKYV, the Founders Edition
	BCKY_V = {
		# US equities, original
		u"DIS"	:	9,
		u"FB"	:	8,

		# non-US equities, original
		u"ADDYY":	9,

		# community consensus
		u"GOOS"	:	23,
	}
	BCKY_V.update(BCKY)
	BCKY_V.update(BCKY_BV)
	
	
	# ^RTRD, the r/WallStreetBets Retard Portfolio
	RTRD = {
		u"BYND"	:   22
	}
	
	
	SPY = {
		u"SPY"	:	1
	}
	
	
	indices = {
		u"^BCKY.A"	: BCKY_A,
		u"^BCKY.B"	: BCKY_B,
		u"^BCKY.V"	: BCKY_V,
		u"^RTRD"	: RTRD,
		u"$SPY"		: SPY
	}