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
	
def SplitAndWrapString(strToSplit, lines_limits):
	s = strToSplit.split(' ')
	listWraped = []
	wrapStr = u""
	for word in s:
		if (len(listWraped) < len(lines_limits)):
			if ((len(wrapStr) + len(word)) < lines_limits[len(listWraped)]):
				wrapStr += word  + u' '
			else:
				listWraped.append(wrapStr)
				wrapStr = word + u' '
		else:
			wrapStr += word  + u' '
	listWraped.append(wrapStr)
	return listWraped
	
def FinfFontSize(imagePck, stringText, width_limit, max_fontsize = 50):
	font_size = max_fontsize
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", font_size)
	str_w,str_h = imagePck.textsize(stringText, font = font)
	while (str_w > width_limit):
		font_size = font_size - 1
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", font_size)
		str_w,str_h = imagePck.textsize(stringText, font = font)
	return font_size, str_h

def DrawBlankCash(imageBlank1, DataRxTx, cash):
	#draw recipient's name on "blank 1"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
	#print DataRxTx.GetFioRx()
	imageBlank1.text((385, 1615), DataRxTx.GetFioRx(), (0,0,0), font = font)
	
	#self.DrawTextOnImage(imageBlank1, DataRxTx.GetFioRx(), 35, 385, 1615);
	
	#draw recipient's address on "blank 1"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
	adr = DataRxTx.GetAddressRx()
	adr_lines = SplitAndWrapString(adr, [90, 60, 0])
	if (len(adr_lines) > 0):
		imageBlank1.text((630, 1700), adr_lines[0], (0,0,0), font = font)
	if (len(adr_lines) > 1):
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
	where_lines = SplitAndWrapString(DataRxTx.GetAddressTx(), [90, 90, 0])
	if (len(where_lines) > 0):
		imageBlank1.text((320, 1030), where_lines[0], (0,0,0), font = font)
	if (len(where_lines) > 1):
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
		
		#draw sum of cash (rubles) with words on "blank 1" 683 - 752
		font_size, ch_w = FinfFontSize(imageBlank1, summ_str, 1500, 40)
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", font_size)
		imageBlank1.text((720, 680 + (70 - ch_w) / 2), summ_str, (0,0,0), font = font)
		
		#draw sum of cash with digits on "blank 1"
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
		imageBlank1.text((230, 755), str(int(rub)), (0,0,0), font = font)
		imageBlank1.text((517, 755), str(kop), (0,0,0), font = font)
	
def DrawBlankMain(imageBlank2, DataRxTx, cash):
	if (cash):
		#second blank
		#Converting sum of cash into words
		summ = float(DataRxTx.GetCashSum().replace(',','.'))
		summ_str = numbertoword.WriteSum(summ, 0)
		trash, rub = math.modf(float(summ))
		
		summ_str = summ_str.rsplit(u'р', 1)[0]

		#draw sum of cash (rubles) with words on "blank 2" 740 - 790
		font_size, ch_w = FinfFontSize(imageBlank2, summ_str, 750, 45)
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", font_size)
		imageBlank2.text((253, 739 + (50 - ch_w) / 2 ), summ_str, (0,0,0), font = font)
		imageBlank2.text((253, 830 + (50 - ch_w) / 2 ), summ_str, (0,0,0), font = font)
		
		#draw sum of cash (rubles) with digits on "blank 2"
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
		imageBlank2.text((450, 2070), str(int(rub)), (0,0,0), font = font)
		imageBlank2.text((1160, 2080), str(int(rub)), (0,0,0), font = font)
	
	#draw recipient's name on "blank 2"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 30)
	imageBlank2.text((385, 935), DataRxTx.GetFioRx(), (0,0,0), font = font)
	
	#draw recipient's address "blank 2"
	where_lines = SplitAndWrapString(DataRxTx.GetAddressRx(), [35, 45, 25])
	if (len(where_lines) > 0):
		imageBlank2.text((400, 985), where_lines[0], (0,0,0), font = font)
	if (len(where_lines) > 1):
		imageBlank2.text((260, 1035), where_lines[1], (0,0,0), font = font)
	if (len(where_lines) > 2):
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
	where_lines = SplitAndWrapString(DataRxTx.GetAddressTx(), [60, 45, 0])
	if (len(where_lines) > 0):
		imageBlank2.text((411, 1203), where_lines[0], (0,0,0), font = font)
	if (len(where_lines) > 1):
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
	adr_lines = SplitAndWrapString(DataRxTx.GetAddressRx(), [55, 35, 0])
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)	
	if (len(adr_lines) > 0):
		imageBlank2.text((400, 2208), adr_lines[0], (0,0,0), font = font)
	if (len(adr_lines) > 1):
		imageBlank2.text((290, 2270), adr_lines[1], (0,0,0), font = font)
	
	#draw recipient's index "blank 2"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 50)
	ind = DataRxTx.GetIndexRx()
	if (len(ind) == 6):
		for i in range(0, 6):
			imageBlank2.text((1160 + 58 * i, 2275), ind[i], (0,0,0), font = font)
	
def DrawBlankAddress(imagePck, DataRxTx, cash, resolution):
	dict_coordinates = {}
	dict_coordinates['pack_number'] = [(10,10),(60, 60)]
	dict_coordinates['recipients_name_1'] = [(520,390),(950, 700)]
	dict_coordinates['recipients_name_2'] = [(470,430),(850, 770)]
	dict_coordinates['recipients_address_1'] = [(530,467),(950, 840)]
	dict_coordinates['recipients_address_2'] = [(480,505),(850, 910)]
	dict_coordinates['recipients_address_3'] = [(480,540),(850, 980)]
	dict_coordinates['recipients_address_4'] = [(480,575),(850, 1050)]
	dict_coordinates['recipient_index1'] = [(90,600),(150, 1070)]
	dict_coordinates['recipient_index2'] = [(90,600),(1350, 960)]
	#draw pack Number
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 70)
	imagePck.text(dict_coordinates['pack_number'][1], DataRxTx.GetPackNumber(), (0,0,0), font = font)
	
	#draw recipient's name on "posilka blank"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 25)
	fio_lines = SplitAndWrapString(DataRxTx.GetFioRx(), [30, 30, 0])
	if (len(fio_lines) > 0):
		imagePck.text(dict_coordinates['recipients_name_1'][1], fio_lines[0], (0,0,0), font = font)
	if (len(fio_lines) > 1):
		imagePck.text(dict_coordinates['recipients_name_2'][1], fio_lines[1], (0,0,0), font = font)
	

	#draw recipient's address on "posilka blank"
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 30)
	adr_lines = SplitAndWrapString(DataRxTx.GetAddressRx(), [40, 50, 50, 30])
	if (len(adr_lines) > 0):
		imagePck.text(dict_coordinates['recipients_address_1'][1], adr_lines[0], (0,0,0), font = font)
	if (len(adr_lines) > 1):
		imagePck.text(dict_coordinates['recipients_address_2'][1], adr_lines[1], (0,0,0), font = font)
	if (len(adr_lines) > 2):
		imagePck.text(dict_coordinates['recipients_address_3'][1], adr_lines[2], (0,0,0), font = font)
	if (len(adr_lines) > 3):
		imagePck.text(dict_coordinates['recipients_address_4'][1], adr_lines[3], (0,0,0), font = font)
	
	#if "nalojenii platej" put X
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 40)
	dict_coordinates['X'] = [(546,172),(875, 300)]
	if (cash):
		imagePck.text(dict_coordinates['X'][1], "x", (0,0,0), font = font)
	
	#draw recipient's index on  "posilka blank"
	font1 = ImageFont.truetype("ttf\DejaVuSans.ttf", 80)
	font2 = ImageFont.truetype("ttf\DejaVuSans.ttf", 60)
	ind = DataRxTx.GetIndexRx()
	if (len(ind) == 6):
		for i in range(0, 6):
			imagePck.text((dict_coordinates['recipient_index1'][1][0] + 110 * i, dict_coordinates['recipient_index1'][1][1]), ind[i], (0,0,0), font = font1) 
			imagePck.text((dict_coordinates['recipient_index2'][1][0] + 60 * i, dict_coordinates['recipient_index2'][1][1]), ind[i], (0,0,0), font = font2) 
	#draw sender's name on "posilka blank"
	dict_coordinates['sender_name_1'] = [(100,240),(190, 430)]
	dict_coordinates['sender_name_2'] = [(45,275),(60, 500)]
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 25)
	whom_splitted = DataRxTx.GetFioTx().split()
	imagePck.text(dict_coordinates['sender_name_1'][1], whom_splitted[0] + " " + whom_splitted[1], (0,0,0), font = font)
	imagePck.text(dict_coordinates['sender_name_2'][1], whom_splitted[2], (0,0,0), font = font)
	
	#draw sender's address on "posilka blank"
	dict_coordinates['sender_address_1'] = [(85,321),(190, 580)]
	dict_coordinates['sender_address_2'] = [(45,360),(50, 640)]
	dict_coordinates['sender_address_3'] = [(45,400),(50, 710)]
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 25)
	where_lines = SplitAndWrapString(DataRxTx.GetAddressTx(), [35, 40, 20])	
	if (len(where_lines) > 0):	
		imagePck.text(dict_coordinates['sender_address_1'][1], where_lines[0], (0,0,0), font = font)
	if (len(where_lines) > 1):	
		imagePck.text(dict_coordinates['sender_address_2'][1], where_lines[1], (0,0,0), font = font)
	if (len(where_lines) > 2):	
		imagePck.text(dict_coordinates['sender_address_3'][1], where_lines[2], (0,0,0), font = font)
	
	#draw sender's index on "posilka blank"
	dict_coordinates['sender_index'] = [(225,388),(410, 680)]
	ind = DataRxTx.GetIndexTx()
	font = ImageFont.truetype("ttf\DejaVuSans.ttf", 40)
	if (len(ind) == 6):
		for i in range(0, 6):
			imagePck.text((dict_coordinates['sender_index'][1][0] + i * 60, dict_coordinates['sender_index'][1][1]), ind[i], (0,0,0), font = font)
	
	if (cash):
		#Converting sum of cash into words
		summ = float(DataRxTx.GetCashSum().replace(',','.'))
		summ_str = numbertoword.WriteSum(summ, 0)
		
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", 40)
		summ_str = summ_str.rsplit(u'р', 1)[0]
		trash, rub = math.modf(float(summ))
		
		#draw sum of cash (rubles) with words on "posilka blank"
		#width = 500px
		dict_coordinates['summ_1'] = [(445,260),(785, 455)]
		dict_coordinates['summ_2'] = [(530,340),(785, 580)]
		font_size, ch_w = FinfFontSize(imagePck, summ_str, 900)
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", font_size)
		imagePck.text((dict_coordinates['summ_1'][1][0], (dict_coordinates['summ_1'][1][1] + (50 - ch_w) / 2)), summ_str, (0,0,0), font = font)
		summ_str = str(int(rub)) +' (' + summ_str + ')'
		font_size, ch_w = FinfFontSize(imagePck, summ_str, 900)
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
		imagePck.text((dict_coordinates['summ_2'][1][0], (dict_coordinates['summ_2'][1][1] + (50 - ch_w) / 2)), summ_str, (0,0,0), font = font)