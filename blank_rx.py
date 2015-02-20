# -*- coding: utf-8 -*-
import wx
import os
import PIL
import math
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import numbertoword
import webbrowser

class RxPage(wx.Panel):
	def __init__(self, parent, TxPage):
		settings_file = open("settings_rx", "r")
		with settings_file as f:
			lines = [line.decode('unicode-escape').rstrip(u'\n') for line in f]
		settings_file.close()
		if (len(lines) != 4):
			for index in range(0, 4):
				lines.append(u'')
		
		# A "-1" in the size parameter instructs wxWidgets to use the default size.
		# In this case, we select 200px width and the default height.
		#wx.Frame.__init__(self, parent, title=title, size=(200,-1))
		wx.Panel.__init__(self, parent)
		
		self.TxPage = TxPage
		
		self.quoteFIOrx = wx.StaticText(self, label=u"ФИО получателя")#1 385/1655 2 367/959 
		self.textFIOrx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = lines[0])
		
		self.quoteADRrx = wx.StaticText(self, label=u"Адрес получателя")#1 630/1733 2 375/1009
		self.textADRrx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = lines[1])
		
		self.quoteINDrx = wx.StaticText(self, label=u"Индекс получателя")#1 1155  /1968/2306
		self.textINDrx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = lines[2])
		
		self.cbSUM = wx.CheckBox(self, -1, u"Наложенный платежа")#1 209/903
			
		self.quoteSUMrx = wx.StaticText(self, label=u"Сумма наложенного платежа")#1 230/790 1 517/790 (коп) 2 253/773 2 240/870
		#self.quoteSUMrx.Disable()
		self.textSUMrx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = lines[3])	
		#self.textSUMrx.Disable()
		self.quoteSUMWordrx = wx.StaticText(self, label=u"")#1 725/747
		#self.quoteSUMWordrx.Disable()
		
		self.generateButton = wx.Button(self, wx.ID_CLEAR, u"Сгенерировать")
	
		self.Bind(wx.EVT_CHECKBOX, self.ShowSUM, self.cbSUM)
		self.Bind(wx.EVT_BUTTON, self.OnGenerate, self.generateButton)
		self.Bind(wx.EVT_TEXT, self.onSummChanged, self.textSUMrx)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
		self.Bind(wx.EVT_LEFT_UP, self.onClick)
		
		# Use some sizers to see layout options
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.quoteFIOrx, 0, wx.SHAPED)
		self.sizer.Add(self.textFIOrx, 0, wx.EXPAND)
		self.sizer.Add(self.quoteADRrx, 0, wx.SHAPED)
		self.sizer.Add(self.textADRrx, 0, wx.EXPAND)
		self.sizer.Add(self.quoteINDrx, 0, wx.SHAPED)
		self.sizer.Add(self.textINDrx, 0, wx.EXPAND)
		
		self.sizer.Add(self.quoteSUMrx, 0, wx.SHAPED)
		self.sizer.Add(self.textSUMrx, 0, wx.EXPAND)
		self.sizer.Add(self.quoteSUMWordrx, 0, wx.EXPAND)
		self.sizer.Add(self.cbSUM, 0, wx.EXPAND)
		
		self.sizer.Add(self.generateButton, 0, wx.ALIGN_CENTER)
		
		self.backgroundImage = wx.Bitmap("background.jpg")
		#Layout sizers
		self.SetSizer(self.sizer)
		self.SetAutoLayout(1)
		self.sizer.Fit(self)
		self.Show()

	def onClick(self, event):
		url = 'http://popadiv10.ru/'
		# Open URL in a new tab, if a browser window is already open.
		webbrowser.open(url)
		
	def OnEraseBackground(self, evt):
		"""
		Add a picture to the background
		"""
		dc = evt.GetDC()

		if not dc:
			dc = wx.ClientDC(self)
			rect = self.GetUpdateRegion().GetBox()
			dc.SetClippingRect(rect)
		dc.Clear()
		if (self.backgroundImage):
			dc.DrawBitmap(self.backgroundImage, 0, 0)
	
	def onSummChanged(self, event):
		summ_str = self.textSUMrx.GetValue().replace(',','.')
		try:
			float(summ_str)
		except ValueError:
			return
		summ = float(summ_str)
		self.quoteSUMWordrx.SetLabel(numbertoword.WriteSum(summ, 1))
	
	def OnClear(self,event):
		self.textFIOrx.SetValue(u'')
		self.textADRrx.SetValue(u'')
		self.textINDrx.SetValue(u'')
		self.textSUMrx.SetValue(u'')
		lines  = []
		lines.append(u'\n')
		lines.append(u'\n')
		lines.append(u'\n')
		lines.append(u'\n')
		settings_file = open("settings_rx", "w")
		with settings_file as f:
			for s in lines:
				f.write(s)
		settings_file.close()
	
	def OnGenerate(self,event):
		img1=Image.open("blank1.jpg")
		img1new = img1.copy() 
		draw1 = ImageDraw.Draw(img1new)
		
		img2=Image.open("blank2.jpg")
		img2new = img2.copy() 
		draw2 = ImageDraw.Draw(img2new)
		
		imgpck =Image.open("blank_posilka.jpg")
		imgpcknew = imgpck.copy() 
		drawpck = ImageDraw.Draw(imgpcknew)
		
		#draw recipient's name on "blank 1"
		#font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
		#draw1.text((385, 1615), self.textFIOrx.GetValue(), (0,0,0), font = font)
		
		self.DrawTextOnImage(draw1, self.textFIOrx.GetValue(), 35, 385, 1615);
		
		#draw recipient's name on "posilka blank"
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", 25)
		fio = self.textFIOrx.GetValue()
		lines_lens = [30, 40, 0]
		fio_lines = self.SplitString(fio, lines_lens)
		drawpck.text((520, 390), fio_lines[0], (0,0,0), font = font)
		drawpck.text((470, 430), fio_lines[1], (0,0,0), font = font)
		
		#draw recipient's address on "blank 1"
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
		adr = self.textADRrx.GetValue()	
		lines_lens = [70, 60, 0]
		adr_lines = self.SplitString(adr, lines_lens)
		draw1.text((630, 1700), adr_lines[0], (0,0,0), font = font)
		draw1.text((230, 1780), adr_lines[1], (0,0,0), font = font)
		
		#draw recipient's address on "posilka blank"
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", 30)
		lines_lens = [25, 35, 35]
		adr_lines = self.SplitString(adr, lines_lens)
		drawpck.text((530, 467), adr_lines[0], (0,0,0), font = font)
		drawpck.text((480, 505), adr_lines[1], (0,0,0), font = font)
		drawpck.text((480, 540), adr_lines[2], (0,0,0), font = font)
		
		#if "nalojenii platej" put X
		if self.cbSUM.GetValue():
			drawpck.text((546, 172), "x", (0,0,0), font = font)
		
		#draw recipient's index on "blank 1" and "posilka blank"
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", 75)
		font2 = ImageFont.truetype("ttf\DejaVuSans.ttf", 55)
		ind = self.textINDrx.GetValue()
		if (len(ind) == 6):
			for i in range(0, 6):
				draw1.text((1974 + 56 * i, 1748), self.textINDrx.GetValue()[i], (0,0,0), font = font) 
				drawpck.text((90 + 58 * i, 600), self.textINDrx.GetValue()[i], (0,0,0), font = font2) 

		#Open file with sender's information
		settings_file = open("settings_tx", "r")
		with settings_file as f:
			lines = [line.decode('unicode-escape').rstrip(u'\n') for line in f]
		settings_file.close()
		if (len(lines) != 9):
			for index in range(0, 9):
				lines.append(u'Заполните поля')
		else:
			#draw sender's name on "blank 1"
			font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
			whom = lines[0]
			draw1.text((320, 950), whom, (0,0,0), font = font)
			
			#draw sender's name on "posilka blank"
			font = ImageFont.truetype("ttf\DejaVuSans.ttf", 25)
			whom_splitted = whom.split()
			drawpck.text((100, 240), whom_splitted[0] + " " + whom_splitted[1], (0,0,0), font = font)
			drawpck.text((45, 275), whom_splitted[2], (0,0,0), font = font)
			
			#draw sender's address on "blank 1"
			font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
			where = lines[1]
			lines_lens = [80, 60, 0]
			where_lines = self.SplitString(where, lines_lens)
			draw1.text((320, 1030), where_lines[0], (0,0,0), font = font)
			draw1.text((220, 1110), where_lines[1], (0,0,0), font = font)
			
			#draw sender's address on "posilka blank"
			font = ImageFont.truetype("ttf\DejaVuSans.ttf", 25)
			lines_lens = [25, 30, 10]
			where_lines = self.SplitString(where, lines_lens)		
			drawpck.text((85, 321), where_lines[0], (0,0,0), font = font)
			drawpck.text((45, 360), where_lines[1], (0,0,0), font = font)
			drawpck.text((45, 400), where_lines[2], (0,0,0), font = font)
			
			#draw sender's index on "blank 1" and "posilka blank"
			ind = lines[2]
			font = ImageFont.truetype("ttf\DejaVuSans.ttf", 75)
			font2 = ImageFont.truetype("ttf\DejaVuSans.ttf", 40)
			if (len(ind) == 6):
				for i in range(0, 6):
					draw1.text((1974 + 56 * i, 1090), ind[i], (0,0,0), font = font)
					drawpck.text((225 + 34 * i, 388), ind[i], (0,0,0), font = font2)
		
			#if "nalojenii platej" draw sum of cash on delivery
			if self.cbSUM.GetValue():
				#draw X
				font = ImageFont.truetype("ttf\DejaVuSans.ttf", 75)
				draw1.text((212, 822), "X", (0,0,0), font = font)
			
				#Converting sum of cash into words
				summ = float(self.textSUMrx.GetValue().replace(',','.'))
				summ_str = numbertoword.WriteSum(summ, 1)
				
				#draw sum of cash (rubles) with words on "blank 1"
				font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
				draw1.text((725, 700), summ_str, (0,0,0), font = font)
								
				kop, rub = math.modf(float(summ))
				kop = (kop+0.001) * 100
				kop = math.trunc(kop)
				
				#draw sum of cash with digits on "blank 1"
				font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
				draw1.text((230, 755), str(int(rub)), (0,0,0), font = font)
				draw1.text((517, 755), str(kop), (0,0,0), font = font)
				drawpck.text((530, 340), str(int(rub)), (0,0,0), font = font)
			
				#second blank
				#Converting sum of cash into words
				summ_str = numbertoword.WriteSum(summ, 0)
				font = ImageFont.truetype("ttf\DejaVuSans.ttf", 40)
				summ_str = summ_str.rsplit(u'р', 1)[0]
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

				#draw sum of cash (rubles) with words on "blank 2"
				font = ImageFont.truetype("ttf\DejaVuSans.ttf", font_size)
				draw2.text((253, 739), summ_str, (0,0,0), font = font)
				draw2.text((253, 839), summ_str, (0,0,0), font = font)
				
				#draw sum of cash (rubles) with words on "posilka blank"
				font = ImageFont.truetype("ttf\DejaVuSans.ttf", font_size - 10)
				drawpck.text((445, 270), summ_str, (0,0,0), font = font)
				
				#draw sum of cash (rubles) with digits on "blank 2"
				font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)
				draw2.text((450, 2070), str(int(rub)), (0,0,0), font = font)
				draw2.text((1160, 2080), str(int(rub)), (0,0,0), font = font)
			
			#draw recipient's name on "blank 2"
			font = ImageFont.truetype("ttf\DejaVuSans.ttf", 30)
			draw2.text((385, 935), self.textFIOrx.GetValue(), (0,0,0), font = font)#self.textFIOrx.GetValue()
			
			#draw recipient's address "blank 2"
			adr = self.textADRrx.GetValue()
			lines_lens = [30, 35, 25]
			where_lines = self.SplitString(adr, lines_lens)
			draw2.text((400, 985), where_lines[0], (0,0,0), font = font)
			draw2.text((260, 1035), where_lines[1], (0,0,0), font = font)
			draw2.text((260, 1080), where_lines[2], (0,0,0), font = font)
			
			#draw recipient's index "blank 2"
			font = ImageFont.truetype("ttf\DejaVuSans.ttf", 45)
			ind = self.textINDrx.GetValue()
			if (len(ind) == 6):
				for i in range(0, 6):
					draw2.text((653 + 58 * i, 1075), ind[i], (0,0,0), font = font)
			
			#draw sender's name "blank 2"
			font = ImageFont.truetype("ttf\DejaVuSans.ttf", 30)
			draw2.text((450, 1145), whom, (0,0,0), font = font)#whom
			
			#draw sender's address "blank 2"
			adr = lines[1]
			lines_lens = [60, 45, 0]
			where_lines = self.SplitString(adr, lines_lens)
			draw2.text((411, 1203), where_lines[0], (0,0,0), font = font)
			draw2.text((311, 1260), where_lines[1], (0,0,0), font = font)
			
			#draw sender's index "blank 2"
			font = ImageFont.truetype("ttf\DejaVuSans.ttf", 45)
			ind = lines[2]
			if (len(ind) == 6):
				for i in range(0, 6):
					draw2.text((1160 + 58 * i, 1247), ind[i], (0,0,0), font = font)
			
			#draw recipient's information "blank 2"
			font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)	
			id 		= lines[3]
			draw2.text((480, 1425), id, (0,0,0), font = font)
			seria 	= lines[4]
			draw2.text((760, 1430), seria, (0,0,0), font = font)
			numb 	= lines[5]
			draw2.text((905, 1430), numb, (0,0,0), font = font)
			iddata 	= lines[6]
			draw2.text((1250, 1430), iddata, (0,0,0), font = font)
			idyear 	= lines[7]
			draw2.text((1455, 1434), idyear, (0,0,0), font = font)
			idadr 	= lines[8]
			draw2.text((260, 1485), idadr, (0,0,0), font = font)
			
			#draw recipient's Name "blank 2"
			font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)	
			draw2.text((387, 2148), self.textFIOrx.GetValue(), (0,0,0), font = font)
			
			#draw recipient's address "blank 2"
			adr = self.textADRrx.GetValue()
			lines_lens = [55, 35, 0]
			adr_lines = self.SplitString(adr, lines_lens)
			font = ImageFont.truetype("ttf\DejaVuSans.ttf", 35)	
			draw2.text((400, 2208), adr_lines[0], (0,0,0), font = font)
			draw2.text((290, 2270), adr_lines[1], (0,0,0), font = font)
			
			#draw recipient's index "blank 2"
			font = ImageFont.truetype("ttf\DejaVuSans.ttf", 45)
			ind = self.textINDrx.GetValue()
			if (len(ind) == 6):
				for i in range(0, 6):
					draw2.text((1160 + 58 * i, 2275), ind[i], (0,0,0), font = font)
		
		#Save settings recipient
		lines  = []
		lines.append(self.textFIOrx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textADRrx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textINDrx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textSUMrx.GetValue().encode('unicode-escape') + u'\n')
				
		settings_file = open("settings_rx", "w")
		with settings_file as f:
			for s in lines:
				f.write(s)
		settings_file.close()
		
		#Draw and Save blanks
		draw1 = ImageDraw.Draw(img1new)
		draw2 = ImageDraw.Draw(img2new)
		drawpck = ImageDraw.Draw(imgpcknew)
		path = self.saveFile(u" бланк 2")
		if (path):
			img2new.save(path)
		if self.cbSUM.GetValue():
			path = self.saveFile(u" бланк 1")
			if (path):
				img1new.save(path)
		path = self.saveFile(u" бланк посылки")
		if (path):
			imgpcknew.save(path)

	
	def saveFile(self, what_blank):
		saveFileDialog = wx.FileDialog(self, u"Сохранить как" + what_blank, "", what_blank, "Blank files (*.jpg)|*.jpg", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)								   
		saveFileDialog.ShowModal()
		path = saveFileDialog.GetPath()
		saveFileDialog.Destroy()
		return path
	
	def SplitString(self, strToSplit, lines):
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
		
	def ShowSUM(self, event):
		if self.cbSUM.GetValue():
			#self.quoteSUMrx.Enable()
			#self.textSUMrx.Enable()
			#self.quoteSUMWordrx.Enable()
			self.TxPage.Enable()
		else: 
			#self.quoteSUMrx.Disable()
			#self.textSUMrx.Disable()
			#self.quoteSUMWordrx.Disable()
			self.TxPage.Disable()
			
	def DrawTextOnImage(self, image, text, font, x, y):
		font = ImageFont.truetype("ttf\DejaVuSans.ttf", font)
		image.text((x, y), text, (0,0,0), font = font)

#app = wx.App(False)
#frame = MainWindow(None, u"Бланк v1.0")
#app.MainLoop()