# -*- coding: utf-8 -*-
import math
import sys

vseg = [ 1e9, 1e6, 1e3, 1]
dhun = [u"", u"сто ", u"двести ", u"триста ", u"четыреста ", u"пятьсот ", u"шестьсот ", u"семьсот ", u"восемьсот ", u"девятьсот "]
ddec = [ u"", u"десять ", u"двадцать ", u"тридцать ",u"сорок ", u"пятьдесят ",u"шестьдесят ",u"семьдесят ",u"восемьдесят ",u"девяносто "]
dde = [ u"одиннадцать ", u"двенадцать ", u"тринадцать ", u"четырнадцать ", u"пятнадцать ", u"шестнадцать ", u"семнадцать ", u"восемнадцать ", u"девятнадцать "]
ded = [ u"", u"один ", u"два ", u"три ", u"четыре ", u"пять ", u"шесть ", u"семь ", u"восемь ", u"девять "]
dedt = [ u"одна ", u"две " ]
dseg = [ u"миллиард", u"миллион", u"тысяч", u"рубл" ]
dsem = [[ u" ",   u"а ",  u"ов " ], # миллиард
	[ u" ",   u"а ",  u"ов " ], #миллион
	[ u"а ",  u"и ",  u" "   ], # тысяч
	[ u"ь ",  u"я ",  u"ей " ], # рубл
	[ u"йка", u"йки", u"ек"  ]] # копе


def HowSay(n):
	n %= 100
	if (n >= 10  and  n <= 20): 
		return 3
	n %= 10
	return 1 if (n == 1) else (n <= 4)  and  2 if (n > 0) else 3

def Round(op, pow):
	if (pow <= 0.):
		return  op
	if (op>0. and op<pow or op<0. and op>pow):
		return 0.
	op = math.floor(op/pow + 0.5) * pow
	return  0. if ( op>0. and op<pow or op<0. and op>pow) else op

def WriteSum(v, cents):
	buf = ""
	if (v >= 1e12  or  v <= 0.009):
		return buf

	v = Round(v, 0.01)
	
	for seg in range(0, 4):
		vt = int(v / vseg[seg])
		v -= vseg[seg] * vt
		if (vt  or  seg == 3):
			how = HowSay(vt)
			# 1 - миллиард   миллион   тысяча рубль  копейка
			# 2 - миллиарда  миллиона  тысячи рубля  копейки
			# 3 - миллиардов миллионов тысяч  рублей копеек
			if (vt):
				buf += dhun[int(vt/100)]
				vt %= 100
				if (vt >= 20  or  vt <= 10):
					buf += ddec[int(vt/10)]
					vt %= 10
					if (seg == 2  and  (vt == 1  or  vt == 2)):
						buf += dedt[int(vt-1)]
					else:  
						buf += ded[int(vt)]
				else:  
					buf += dde[int(vt-11)]
			else:
				if (buf):
					pass
					#buf += u"ноль "
			buf += dseg[seg]
			buf += dsem[seg][how-1]
	if (cents):
		buf += u"%02.0lf копе%s" % (v * 100, dsem[4][HowSay(int(Round(v*100,1))) - 1])
	return  buf

#print sys.argv[1]
#print WriteSum(float(sys.argv[1]))


