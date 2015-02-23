# -*- coding: utf-8 -*-
import PIL
import math
import numbertoword
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
	
def DrawTextOnImage(img, wText, fontSize, x, y):
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", fontSize)
	img.text((x, y), wText, (0,0,0), font = font)
	
def SplitString(strToSplit, lines):
	s = strToSplit.split(' ')
	line1_is_not_full = 1
	line2_is_not_full = 1
	line3_is_not_full = 1
	where_1line = ""
	where_2line = ""
	where_3line = ""
	for word in s:
		if ((lines[0] > 0) and ((len(where_1line) + len(word)) < lines[0]) and line1_is_not_full):
			where_1line += word
			where_1line += " "
		else:
			line1_is_not_full = 0
			if ((lines[1] > 0) and ((len(where_2line) + len(word)) < lines[1]) and line2_is_not_full):
				where_2line += word
				where_2line += " "
			else:
				line2_is_not_full = 0
				if ((lines[2] > 0) and ((len(where_3line) + len(word)) < lines[2]) and line3_is_not_full):
					where_3line += word
					where_3line += " "
				else:
					line3_is_not_full = 0
	return [where_1line, where_2line, where_3line]
	
def GetCashFontSize(summ_str):
	length_summ_str = len(summ_str)
	font_size =  40
	if (length_summ_str > 35 and length_summ_str <= 40):
		font_size = 33
	elif (length_summ_str > 40 and length_summ_str <= 45):
		font_size = 29
	elif (length_summ_str > 45 and length_summ_str <= 50):
		font_size = 26
	elif (length_summ_str > 50 and len(summ_str) <= 55):
		font_size = 24
	elif (length_summ_str > 55):
		font_size = 22	
	return font_size
	
def DrawBlank1(imageBlank1, DataRxTx, cash):
	#draw recipient's name on "blank 1"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
	print DataRxTx.GetFioRx()
	imageBlank1.text((385, 1615), DataRxTx.GetFioRx(), (0,0,0), font = font)
	
	#self.DrawTextOnImage(imageBlank1, DataRxTx.GetFioRx(), 35, 385, 1615);
	
	#draw recipient's address on "blank 1"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
	adr = DataRxTx.GetAddressRx()
	lines_lens = [70, 60, 0]
	adr_lines = SplitString(adr, lines_lens)
	imageBlank1.text((630, 1700), adr_lines[0], (0,0,0), font = font)
	imageBlank1.text((230, 1780), adr_lines[1], (0,0,0), font = font)
	
	#draw recipient's index on "blank 1"
	ind = DataRxTx.GetIndexRx()
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 70)
	if (len(ind) == 6):
		for i in range(0, 6):
			imageBlank1.text((1974 + 56 * i, 1748), ind[i], (0,0,0), font = font)
		
	#draw sender's name on "blank 1"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
	imageBlank1.text((320, 950), DataRxTx.GetFioTx(), (0,0,0), font = font)
	
	#draw sender's address on "blank 1"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
	lines_lens = [80, 60, 0]
	where_lines = SplitString(DataRxTx.GetAddressTx(), lines_lens)
	imageBlank1.text((320, 1030), where_lines[0], (0,0,0), font = font)
	imageBlank1.text((220, 1110), where_lines[1], (0,0,0), font = font)
	
	#draw sender's index on "blank 1" and 			
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 70)
	ind = DataRxTx.GetIndexTx()
	if (len(ind) == 6):
		for i in range(0, 6):
			imageBlank1.text((1974 + 56 * i, 1090), ind[i], (0,0,0), font = font)
	if (cash):
		#draw X
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", 75)
		imageBlank1.text((212, 822), "X", (0,0,0), font = font)
		
		#Converting sum of cash into words
		summ = float(DataRxTx.GetCashSum().replace(',','.'))
		summ_str = numbertoword.WriteSum(summ, 1)
			
		kop, rub = math.modf(float(summ))
		kop = (kop+0.001) * 100
		kop = math.trunc(kop)
		
		#draw sum of cash (rubles) with words on "blank 1"
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
		imageBlank1.text((725, 700), summ_str, (0,0,0), font = font)
		
		#draw sum of cash with digits on "blank 1"
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
		imageBlank1.text((230, 755), str(int(rub)), (0,0,0), font = font)
		imageBlank1.text((517, 755), str(kop), (0,0,0), font = font)
		
def DrawBlank2(imageBlank2, DataRxTx, cash):
	if (cash):
		#second blank
		#Converting sum of cash into words
		summ = float(DataRxTx.GetCashSum().replace(',','.'))
		summ_str = numbertoword.WriteSum(summ, 0)
		trash, rub = math.modf(float(summ))
		
		summ_str = summ_str.rsplit(u'р', 1)[0]

		#draw sum of cash (rubles) with words on "blank 2"
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", GetCashFontSize(summ_str))
		imageBlank2.text((253, 739), summ_str, (0,0,0), font = font)
		imageBlank2.text((253, 839), summ_str, (0,0,0), font = font)
		
		#draw sum of cash (rubles) with digits on "blank 2"
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
		imageBlank2.text((450, 2070), str(int(rub)), (0,0,0), font = font)
		imageBlank2.text((1160, 2080), str(int(rub)), (0,0,0), font = font)
	
	#draw recipient's name on "blank 2"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 30)
	imageBlank2.text((385, 935), DataRxTx.GetFioRx(), (0,0,0), font = font)
	
	#draw recipient's address "blank 2"
	adr = DataRxTx.GetAddressRx()
	lines_lens = [30, 35, 25]
	where_lines = SplitString(adr, lines_lens)
	imageBlank2.text((400, 985), where_lines[0], (0,0,0), font = font)
	imageBlank2.text((260, 1035), where_lines[1], (0,0,0), font = font)
	imageBlank2.text((260, 1080), where_lines[2], (0,0,0), font = font)
	
	#draw recipient's index "blank 2"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 50)
	ind = DataRxTx.GetIndexRx()
	if (len(ind) == 6):
		for i in range(0, 6):
			imageBlank2.text((653 + 58 * i, 1075), ind[i], (0,0,0), font = font)
	
	#draw sender's name "blank 2"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 30)
	imageBlank2.text((450, 1145), DataRxTx.GetFioTx(), (0,0,0), font = font)
	
	#draw sender's address "blank 2"
	lines_lens = [60, 45, 0]
	where_lines = SplitString(DataRxTx.GetAddressTx(), lines_lens)
	imageBlank2.text((411, 1203), where_lines[0], (0,0,0), font = font)
	imageBlank2.text((311, 1260), where_lines[1], (0,0,0), font = font)
	
	#draw sender's index "blank 2"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 50)
	ind = DataRxTx.GetIndexTx()
	if (len(ind) == 6):
		for i in range(0, 6):
			imageBlank2.text((1160 + 58 * i, 1247), ind[i], (0,0,0), font = font)
	
	#draw sender's passport information "blank 2"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)	
	imageBlank2.text((480, 1425), DataRxTx.GetPassportIDTx(), (0,0,0), font = font)
	imageBlank2.text((760, 1430), DataRxTx.GetPassportSerialTx(), (0,0,0), font = font)
	imageBlank2.text((905, 1430), DataRxTx.GetPassportNumberTx(), (0,0,0), font = font)
	imageBlank2.text((1250, 1430), DataRxTx.GetPassportDataTx(), (0,0,0), font = font)
	imageBlank2.text((1455, 1434), DataRxTx.GetPassportYearTx(), (0,0,0), font = font)
	imageBlank2.text((260, 1485), DataRxTx.GetPassportAddressTx(), (0,0,0), font = font)
	
	#draw recipient's Name "blank 2"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)	
	imageBlank2.text((387, 2148), DataRxTx.GetFioRx(), (0,0,0), font = font)
	
	#draw recipient's address "blank 2"
	adr = DataRxTx.GetAddressRx()
	lines_lens = [55, 35, 0]
	adr_lines = SplitString(adr, lines_lens)
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)	
	imageBlank2.text((400, 2208), adr_lines[0], (0,0,0), font = font)
	imageBlank2.text((290, 2270), adr_lines[1], (0,0,0), font = font)
	
	#draw recipient's index "blank 2"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 50)
	ind = DataRxTx.GetIndexRx()
	if (len(ind) == 6):
		for i in range(0, 6):
			imageBlank2.text((1160 + 58 * i, 2275), ind[i], (0,0,0), font = font)
			
def DrawBlank3(imagePck, DataRxTx, cash):
	#draw recipient's name on "posilka blank"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 25)
	fio = DataRxTx.GetFioRx()
	lines_lens = [30, 40, 0]
	fio_lines = SplitString(fio, lines_lens)
	imagePck.text((520, 390), fio_lines[0], (0,0,0), font = font)
	imagePck.text((470, 430), fio_lines[1], (0,0,0), font = font)
	

	#draw recipient's address on "posilka blank"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 30)
	lines_lens = [25, 35, 35]
	adr_lines = SplitString(DataRxTx.GetAddressRx(), lines_lens)
	imagePck.text((530, 467), adr_lines[0], (0,0,0), font = font)
	imagePck.text((480, 505), adr_lines[1], (0,0,0), font = font)
	imagePck.text((480, 540), adr_lines[2], (0,0,0), font = font)
	
	#if "nalojenii platej" put X
	if (cash):
		imagePck.text((546, 172), "x", (0,0,0), font = font)
	
	#draw recipient's index on  "posilka blank"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 55)
	ind = DataRxTx.GetIndexRx()
	if (len(ind) == 6):
		for i in range(0, 6):
			imagePck.text((90 + 58 * i, 600), ind[i], (0,0,0), font = font) 
			
	#draw sender's name on "posilka blank"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 25)
	whom_splitted = DataRxTx.GetFioTx().split()
	imagePck.text((100, 240), whom_splitted[0] + " " + whom_splitted[1], (0,0,0), font = font)
	imagePck.text((45, 275), whom_splitted[2], (0,0,0), font = font)
	
	#draw sender's address on "posilka blank"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 25)
	lines_lens = [25, 30, 10]
	where_lines = SplitString(DataRxTx.GetAddressTx(), lines_lens)		
	imagePck.text((85, 321), where_lines[0], (0,0,0), font = font)
	imagePck.text((45, 360), where_lines[1], (0,0,0), font = font)
	imagePck.text((45, 400), where_lines[2], (0,0,0), font = font)
	
	#draw sender's index on "posilka blank"
	ind = DataRxTx.GetIndexTx()
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 40)
	if (len(ind) == 6):
		for i in range(0, 6):
			imagePck.text((225 + 34 * i, 388), ind[i], (0,0,0), font = font)
	
	if (cash):
		#Converting sum of cash into words
		summ = float(DataRxTx.GetCashSum().replace(',','.'))
		summ_str = numbertoword.WriteSum(summ, 0)
		
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", 40)
		summ_str = summ_str.rsplit(u'р', 1)[0]
		trash, rub = math.modf(float(summ))
		
		#draw sum of cash (rubles) with words on "posilka blank"
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", GetCashFontSize(summ_str) - 10)
		imagePck.text((445, 270), summ_str, (0,0,0), font = font)
		
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
		imagePck.text((530, 340), str(int(rub)), (0,0,0), font = font)