# -*- coding: utf-8 -*-
import wx
import os
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import numbertoword
import webbrowser

class TxPage(wx.Panel):

	def __init__(self, parent, DataRxTx):

		self.DataRxTx = DataRxTx
		# A "-1" in the size parameter instructs wxWidgets to use the default size.
		# In this case, we select 200px width and the default height.
		wx.Panel.__init__(self, parent)
		
		self.quoteFIOtx = wx.StaticText(self, label=u"ФИО отправителя")
		self.textFIOtx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = self.DataRxTx.GetFioTx())
		
		self.quoteADRtx = wx.StaticText(self, label=u"Адрес отправителя")
		self.textADRtx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = self.DataRxTx.GetAddressTx())
		
		self.quoteINDtx = wx.StaticText(self, label=u"Индекс отправителя")
		self.textINDtx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = self.DataRxTx.GetIndexTx())
		
		self.quoteIDtx = wx.StaticText(self, label=u"Предъявил ")
		self.textIDtx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = self.DataRxTx.GetPassportIDTx())
		self.quoteSeriatx = wx.StaticText(self, label=u"серия ")
		self.textSeriatx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = self.DataRxTx.GetPassportSerialTx())
		self.quoteNumbertx = wx.StaticText(self, label=u"номер ")
		self.textNumbertx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = self.DataRxTx.GetPassportNumberTx())
		
		self.quoteIDDatatx = wx.StaticText(self, label=u"выдан ")
		self.textIDDatatx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = self.DataRxTx.GetPassportDataTx())
		self.quoteIDYeartx = wx.StaticText(self, label=u"20")
		self.textIDYeartx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = self.DataRxTx.GetPassportYearTx())
		
		self.quoteIDAdrtx = wx.StaticText(self, label=u"Наименование учрежения")
		self.textIDAdrtx = wx.TextCtrl(self, style=wx.TE_RIGHT, value = self.DataRxTx.GetPassportAddressTx())

		self.saveButton = wx.Button(self, wx.ID_CLEAR, u"Сохранить")

		self.Bind(wx.EVT_BUTTON, self.OnSave, self.saveButton)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
		self.Bind(wx.EVT_LEFT_UP, self.onClick)
		
		# Use some sizers to see layout options
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.quoteFIOtx, 0, wx.SHAPED)
		self.sizer.Add(self.textFIOtx, 0, wx.EXPAND)
		self.sizer.Add(self.quoteADRtx, 0, wx.SHAPED)
		self.sizer.Add(self.textADRtx, 0, wx.EXPAND)
		self.sizer.Add(self.quoteINDtx, 0, wx.SHAPED)
		self.sizer.Add(self.textINDtx, 0, wx.EXPAND)
		
		id1_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(id1_sizer, 0, wx.EXPAND | wx.ALIGN_TOP)
		id1_sizer.Add(self.quoteIDtx, 		0, wx.ALIGN_LEFT)
		id1_sizer.Add(self.textIDtx, 		0, wx.ALIGN_LEFT)
		id1_sizer.Add(self.quoteSeriatx, 	0, wx.ALIGN_LEFT)
		id1_sizer.Add(self.textSeriatx, 	0, wx.ALIGN_LEFT)
		id1_sizer.Add(self.quoteNumbertx, 	0, wx.ALIGN_LEFT)
		id1_sizer.Add(self.textNumbertx, 	0, wx.ALIGN_LEFT)
		
		id2_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(id2_sizer, 0, wx.EXPAND | wx.ALIGN_TOP)
		id2_sizer.Add(self.quoteIDDatatx, 	0, wx.ALIGN_LEFT)
		id2_sizer.Add(self.textIDDatatx, 	0, wx.ALIGN_LEFT)
		id2_sizer.Add(self.quoteIDYeartx, 	0, wx.ALIGN_LEFT)
		id2_sizer.Add(self.textIDYeartx, 	0, wx.ALIGN_LEFT)
		
		self.sizer.Add(self.quoteIDAdrtx, 0, wx.SHAPED | wx.ALIGN_LEFT | wx.ALIGN_TOP)
		self.sizer.Add(self.textIDAdrtx, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALIGN_TOP)
		
		self.sizer.Add(self.saveButton, 0, wx.ALIGN_CENTER)
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
			
	#save recipient's information
	def OnSave(self, event):
		lines  = []
		lines.append(self.textFIOtx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textADRtx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textINDtx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textIDtx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textSeriatx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textNumbertx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textIDDatatx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textIDYeartx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textIDAdrtx.GetValue().encode('unicode-escape') + u'\n')
		self.DataRxTx.SaveSenderInformation(lines);