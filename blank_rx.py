# -*- coding: utf-8 -*-
import wx
import os
import blankDrawer
import numbertoword
import webbrowser
from PIL import Image
from PIL import ImageDraw

class RxPage(wx.Panel):
	def __init__(self, parent, TxPage, DataRxTx):
		# A "-1" in the size parameter instructs wxWidgets to use the default size.
		# In this case, we select 200px width and the default height.
		#wx.Frame.__init__(self, parent, title=title, size=(200,-1))
		wx.Panel.__init__(self, parent)
		
		self.TxPage = TxPage
		self.DataRxTx = DataRxTx
		self.quoteFIOrx = wx.StaticText(self, label=u"ФИО получателя")#1 385/1655 2 367/959 
		self.textFIOrx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = self.DataRxTx.GetFioRx())
		
		self.quoteADRrx = wx.StaticText(self, label=u"Адрес получателя")#1 630/1733 2 375/1009
		self.textADRrx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = self.DataRxTx.GetAddressRx())
		
		self.quoteINDrx = wx.StaticText(self, label=u"Индекс получателя")#1 1155  /1968/2306
		self.textINDrx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = self.DataRxTx.GetIndexRx())
		
		self.cbSUM = wx.CheckBox(self, -1, u"Наложенный платежа")#1 209/903
			
		self.quoteSUMrx = wx.StaticText(self, label=u"Сумма наложенного платежа")#1 230/790 1 517/790 (коп) 2 253/773 2 240/870
		#self.quoteSUMrx.Disable()
		self.textSUMrx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = self.DataRxTx.GetCashSum())	
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
		DataRxTx.SaveRecipientInformation(lines);
	
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
		
		blankDrawer.DrawBlank1(draw1, self.DataRxTx, self.cbSUM.GetValue())
		blankDrawer.DrawBlank2(draw2, self.DataRxTx, self.cbSUM.GetValue())
		blankDrawer.DrawBlank3(drawpck, self.DataRxTx, self.cbSUM.GetValue())
			
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
			
		self.saveRecipientInfo()
	
	def saveRecipientInfo(self):
		#Save settings recipient
		lines  = []
		lines.append(self.textFIOrx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textADRrx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textINDrx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textSUMrx.GetValue().encode('unicode-escape') + u'\n')
		DataRxTx.SaveRecipientInformation(lines);
	
	def saveFile(self, what_blank):
		saveFileDialog = wx.FileDialog(self, u"Сохранить как" + what_blank, "", what_blank, "Blank files (*.jpg)|*.jpg", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)								   
		saveFileDialog.ShowModal()
		path = saveFileDialog.GetPath()
		saveFileDialog.Destroy()
		return path
	
	def ShowSUM(self, event):
		if self.cbSUM.GetValue():
			self.TxPage.Enable()
		else: 
			self.TxPage.Disable()