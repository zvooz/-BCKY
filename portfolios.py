# -*- coding: utf-8 -*- 

import datetime

class Portfolios:
	epoch = datetime.date(2019, 3, 28)

	# MC = "MC.PA"
	MC = "LVMHF"
	# OR = "OR.PA"
	OR = "LRLCF"

	# ^BCKY.A or ^BCKYA, the primary ^BCKY portfolio
	BCKY_A = {
		"AAPL"	:	5,
		"ETSY"	:	15,
		"LULU"	:	6,
		MC		:	3,
		OR		:	4,
		"PLNT"	:	15,
		"SBUX"	:	14,
		"ULTA"	:	3
	}

	# ^BCKY.B or ^BCKYB, the secondary ^BCKY portfolio, a superset of ^BCKY.A or ^BCKYA
	BCKY_B = {
		"COTY"	:	87,
		"DECK"	:	7,
		"DEO"	:	6,
		"EL"	:	6,
		"LB"	:	36,
		"FIZZ"	:	18,
		"NFLX"	:	3,
		"NKE"	:	12,
		"SNAP"	:	93,
		"TGT"	:	12,
		"TIF"	:	10,
		"UAA"	:	47,
		"VFC"	:	11
	}
	BCKY_B.update(BCKY_A)

	# ^BCKY.V or ^BCKYV, the Founders Edition
	BCKY_V = {
		# US equities, original
		"AAPL"	:	5,
		"DECK"	:	7,
		"DIS"	:	9,
		"EL"	:	6,
		"FB"	:	6,
		"LB"	:	36,
		"LULU"	:	6,
		"NKE"	:	12,
		"SBUX"	:	14,
		"UAA"	:	47,
		"ULTA"	:	3,

		# non-US equities, original
		"ADDYY"	:	8,
		"DEO"	:	6,
		"LRLCY"	:	19,
		"LVMUY"	:	14,

		# community consensus
		"ETSY"	:	15,
		"FIZZ"	:	18,
		"GOOS"	:	21,
		"NFLX"	:	3,
		"SNAP"	:	93,
		"TGT"	:	12,
		"TIF"	:	10
	}
