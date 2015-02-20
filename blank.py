# -*- coding: utf-8 -*-
import wx
import os
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import numbertoword

class RxPage(wx.Panel):
	def __init__(self, parent):
		self.dirname=''
		
		# A "-1" in the size parameter instructs wxWidgets to use the default size.
		# In this case, we select 200px width and the default height.
		#wx.Frame.__init__(self, parent, title=title, size=(200,-1))
		wx.Panel.__init__(self, parent)
		
		self.quoteFIOrx = wx.StaticText(self, label=u"ФИО получателя")
		self.textFIOrx = wx.TextCtrl(self, style=wx.TE_RIGHT)
		
		self.quoteADRrx = wx.StaticText(self, label=u"Адрес получателя")
		self.textADRrx = wx.TextCtrl(self, style=wx.TE_RIGHT)
		
		self.quoteINDrx = wx.StaticText(self, label=u"Индекс получателя")
		self.textINDrx = wx.TextCtrl(self, style=wx.TE_RIGHT)
		
		self.cbSUM = wx.CheckBox(self, -1, u"Наложенный платежа")
		
		self.quoteSUMrx = wx.StaticText(self, label=u"Сумма наложенного платежа")
		self.quoteSUMrx.Disable()
		self.textSUMrx = wx.TextCtrl(self, style=wx.TE_RIGHT)	
		self.textSUMrx.Disable()
		
		self.generateButton = wx.Button(self, wx.ID_CLEAR, u"Сгенерировать")

		self.Bind(wx.EVT_CHECKBOX, self.ShowSUM, self.cbSUM)
		self.Bind(wx.EVT_BUTTON, self.OnGenerate, self.generateButton)
		
		# Use some sizers to see layout options
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.quoteFIOrx, 0, wx.EXPAND)
		self.sizer.Add(self.textFIOrx, 0, wx.EXPAND)
		self.sizer.Add(self.quoteADRrx, 0, wx.EXPAND)
		self.sizer.Add(self.textADRrx, 0, wx.EXPAND)
		self.sizer.Add(self.quoteINDrx, 0, wx.EXPAND)
		self.sizer.Add(self.textINDrx, 0, wx.EXPAND)
		
		self.sizer.Add(self.cbSUM, 0, wx.EXPAND)
		self.sizer.Add(self.quoteSUMrx, 0, wx.EXPAND)
		self.sizer.Add(self.textSUMrx, 0, wx.EXPAND)
		
		self.sizer.Add(self.generateButton, 0, wx.EXPAND)
		
		#Layout sizers
		self.SetSizer(self.sizer)
		self.SetAutoLayout(1)
		self.sizer.Fit(self)
		self.Show()

	def OnGenerate(self,event):
		img1=Image.open("blank1.jpg")
		img1new = img1.copy() 
		#font = ImageFont.truetype("pathToFont",10)
		draw = ImageDraw.Draw(img1new)
		draw.text((0, 0),"This is a test",(0,0,0))
		draw = ImageDraw.Draw(img1new)
		draw = ImageDraw.Draw(img1new)
		img1new.save("blank1new.jpg")
		
	def ShowSUM(self, event):
		if self.cbSUM.GetValue():
			self.quoteSUMrx.Enable()
			self.textSUMrx.Enable()
		else: 
			self.quoteSUMrx.Disable()
			self.textSUMrx.Disable()

#app = wx.App(False)
#frame = MainWindow(None, u"Бланк v1.0")
#app.MainLoop()