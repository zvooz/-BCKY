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
	md_BCKY_A = u"^BCKY.A tracks the fewest stocks. It uses the composition from [this post](https://www.reddit.com/r/wallstreetbets/comments/b6hvdf/i_indexed_beckys_portfolio_so_you_dont_have_to/)."
	
	
	# ^BCKY.B or ^BCKYB, the secondary ^BCKY portfolio, a superset of ^BCKY.A or ^BCKYA
	BCKY_B = {
		# US equities
		u"COTY"	:	155,
		u"VFC"	:	15
	}
	BCKY_B.update(BCKY_A)
	BCKY_B.update(BCKY_BV)
	md_BCKY_B = u"^BCKY.B is a much longer, and possibly over-done extension to ^BCKY.A. It uses the composition from [this post](https://www.reddit.com/r/wallstreetbets/comments/b6mudk/bcky_update_wsb_was_right_diversification_bad/). In addition to what is in ^BCKY.A, it has the following components:"
	
	
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
	md_BCKY_V = u"^BCKY.V uses the composition from [that r/investing post](https://www.reddit.com/r/investing/comments/9n31xf/introducing_the_white_girl_index/)."
	
	
	# ^KREN; "Faceplace is Instaspam for old dried up Beckies" ― u/Doc_Emmett_L_Brown
	KREN = {
		u"TGT"	:	15,
		u"KSS"	:	15,
		u"SBUX"	:	16,
		u"ADDYY":	9,
		u"FB"	:	8,
		u"TM"	:	9,
		u"AVP"	:	676
	}
	md_KREN = u"^KREN is from [this r/WallStreetBets post](https://www.reddit.com/r/wallstreetbets/comments/craedi/buy_the_karen/).\n> Faceplace is Instaspam for old dried up Beckies\n\t― [u/Doc_Emmett_L_Brown](https://www.reddit.com/user/Doc_Emmett_L_Brown/)"
	
	
	# ^RTRD, the r/WallStreetBets' Retard Portfolio
	RTRD = {
		u"BYND"	:   22,
		u"SHMP"	:	54054,
		u"YRIV"	:	267
	}
	md_RTRD = u"Just like the WSB, ^RTRD's components are all very retarded. It's quite self-explanatory."
	
	
	SPY = {
		u"SPY"	:	1
	}
	md_SPY = u"Not one day goes by without a $SPY FD post on the WSB."
	
	
	indices = {
		u"^BCKY.A"	:	[BCKY_A, md_BCKY_A],
		u"^BCKY.B"	:	[BCKY_B, md_BCKY_B],
		u"^BCKY.V"	:	[BCKY_V, md_BCKY_V],
		u"^KREN"	:	[KREN, md_KREN],
		u"^RTRD"	:	[RTRD, md_RTRD],
		u"$SPY"		:	[SPY, md_SPY]
	}