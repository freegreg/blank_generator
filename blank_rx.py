# -*- coding: utf-8 -*-
import wx
import os
import blankDrawer
import numbertoword
import webbrowser
from PIL import Image
from PIL import ImageDraw
from xlrd import open_workbook, XLRDError

class RxPage(wx.Panel):
	def __init__(self, parent, DataRxTx):
		# A "-1" in the size parameter instructs wxWidgets to use the default size.
		# In this case, we select 200px width and the default height.
		#wx.Frame.__init__(self, parent, title=title, size=(200,-1))
		wx.Panel.__init__(self, parent)
		
		self.PathToExcelFile = '';
		self.PathToBlanksFolder = '';
		
		settings_file = open("settings_paths", "r")
		with settings_file as f:
			lines_paths = [line.decode('unicode-escape').rstrip(u'\n') for line in f]
		settings_file.close()
		if (len(lines_paths) == 2):
			self.PathToExcelFile = lines_paths[0]
			self.PathToBlanksFolder = lines_paths[1]
		
		self.cbFromExcel = wx.CheckBox(self, -1, u"Из Excel файла")
		#self.quoteSUMrx.Disable()
		self.textPathToExcelFile = wx.TextCtrl(self, style=wx.TE_RIGHT, value = u"Путь к Excel файлу")
		self.textPathToExcelFile.Disable()
		self.openExcelFileButton = wx.Button(self, wx.ID_CLEAR, u"Открыть Excel файл")
		self.openExcelFileButton.Disable()
		
		self.textPathToBlankFolder = wx.TextCtrl(self, style=wx.TE_RIGHT, value = u"Путь к папке для сохранения бланков")
		self.textPathToBlankFolder.Disable()
		self.openBlankFolderButton = wx.Button(self, wx.ID_CLEAR, u"Открыть папку")
		self.openBlankFolderButton.Disable()
		
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
	
		self.Bind(wx.EVT_BUTTON, self.ButtonHandler, self.openExcelFileButton)
		self.Bind(wx.EVT_BUTTON, self.ButtonHandler, self.openBlankFolderButton)
		self.Bind(wx.EVT_BUTTON, self.ButtonHandler, self.generateButton)
		self.Bind(wx.EVT_TEXT, self.onTextChanged, self.textSUMrx)
		self.Bind(wx.EVT_TEXT, self.onTextChanged, self.textPathToExcelFile)
		self.Bind(wx.EVT_TEXT, self.onTextChanged, self.textPathToBlankFolder)
		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
		self.Bind(wx.EVT_LEFT_UP, self.onClick)
		self.Bind(wx.EVT_CHECKBOX, self.FromExcel, self.cbFromExcel)
		
		# Use some sizers to see layout options
		self.sizer = wx.BoxSizer(wx.VERTICAL)
			
		self.sizer.Add(self.cbFromExcel, 		0, wx.EXPAND)
		
		id1_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(id1_sizer, 0, wx.EXPAND)
		id1_sizer.Add(self.textPathToExcelFile, 2, wx.EXPAND)
		id1_sizer.Add(self.openExcelFileButton, 0, wx.SHAPED | wx.ALIGN_RIGHT)
		
		id2_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(id2_sizer, 0, wx.EXPAND)
		id2_sizer.Add(self.textPathToBlankFolder, 2, wx.EXPAND)
		id2_sizer.Add(self.openBlankFolderButton, 0, wx.SHAPED | wx.ALIGN_RIGHT)
		
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
	
	def onTextChanged(self, event):
		textField = event.GetEventObject()
		if (textField == self.textSUMrx):
			summ_str = self.textSUMrx.GetValue().replace(',','.')
			try:
				float(summ_str)
			except ValueError:
				return
			summ = float(summ_str)
			self.quoteSUMWordrx.SetLabel(numbertoword.WriteSum(summ, 1))
		elif (textField == self.textPathToExcelFile):
			self.PathToExcelFile = self.textPathToExcelFile.GetValue()
		elif (textField == self.textPathToBlankFolder):
			self.PathToBlanksFolder = self.textPathToBlankFolder.GetValue()
	
	def OnClear(self, event):
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
		
	def Warn(self, message, caption = 'Warning!'):
		dlg = wx.MessageDialog(self, message, caption, wx.OK | wx.ICON_WARNING)
		dlg.ShowModal()
		dlg.Destroy()
		
	def TestExcelBook(self, filename):
		try:
			open_workbook(filename)
		except XLRDError:
			return False
		else:
			return True
	def OnGenerate(self):

		img1=Image.open("blank1.jpg")
		img1new = img1.copy()
		draw1 = ImageDraw.Draw(img1new)
		
		img2=Image.open("blank2.jpg")
		img2new = img2.copy() 
		draw2 = ImageDraw.Draw(img2new)
		
		imgpck =Image.open("blank_posilka.jpg")
		imgpcknew = imgpck.copy() 
		drawpck = ImageDraw.Draw(imgpcknew)
					
		if self.cbFromExcel.GetValue():
			if (not os.path.exists(self.PathToBlanksFolder)):
				self.Warn(u"Папка не существует!")
				return
			if (not os.path.isfile(self.PathToExcelFile)):
				self.Warn(u"Файл не существует!")
				return
			try:
				wb = open_workbook(self.PathToExcelFile)
			except XLRDError:
				self.Warn(u"Неверный формат Excel!")
				return
			index_row = 0
			for s in wb.sheets():
				print 'Sheet:',s.name
				if (s.ncols < 4):
					self.Warn(u"Неверное количество столбцов!")
					return
				progressMax = 300
				dialog = wx.ProgressDialog(u"Обработка", u"Подождите", progressMax, style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
				delta_count = progressMax/s.nrows/3
				count = 0
				for row in range(s.nrows):
					if (index_row > 0): 
						values = []
						for col in range(s.ncols):
							values.append(s.cell(row,col).value)
						list_from_excel = list(str(v) if not isinstance(v, unicode) else v for v in values)
						list_from_excel[0] = str(values[0]) if not isinstance(values[0], unicode) else values[0]
						list_from_excel[1] = str(values[2]) if not isinstance(values[2], unicode) else values[2]
						list_from_excel[2] = str(int(values[3])) if not isinstance(values[3], unicode) else values[3]
						list_from_excel[3] = str(values[1]) if not isinstance(values[1], unicode) else values[1]
						#list_from_excel.append(list_from_excel[1])
						#del list_from_excel[1]
						self.DataRxTx.SetRecipientInformation(list_from_excel)
						img1new = img1.copy() 
						draw1 = ImageDraw.Draw(img1new)
						img2new = img2.copy() 
						draw2 = ImageDraw.Draw(img2new)
						imgpcknew = imgpck.copy() 
						drawpck = ImageDraw.Draw(imgpcknew)
						if (values[1] > 0):
							blankDrawer.DrawBlank1(draw1, self.DataRxTx, values[1] > 0)
							count = count + delta_count
							dialog.Update(count)
						blankDrawer.DrawBlank2(draw2, self.DataRxTx, values[1] > 0)
						count = count + delta_count
						dialog.Update(count)
						blankDrawer.DrawBlank3(drawpck, self.DataRxTx, values[1] > 0)
						count = count + delta_count
						dialog.Update(count)
						if (self.PathToBlanksFolder):
							img2new.save(self.PathToBlanksFolder + u"\бланк_" + str(index_row) + u".jpg")
							if (values[1] > 0):
								img1new.save(self.PathToBlanksFolder + u"\бланк_наложенного_" + str(index_row) + u".jpg")
							imgpcknew.save(self.PathToBlanksFolder + u"\бланк_адресной_" + str(index_row) + u".jpg")
						#print u','.join(list_from_excel)
					index_row = index_row + 1
			dialog.Destroy()
			
		else:
			blankDrawer.DrawBlank1(draw1, self.DataRxTx, self.cbSUM.GetValue())
			blankDrawer.DrawBlank2(draw2, self.DataRxTx, self.cbSUM.GetValue())
			blankDrawer.DrawBlank3(drawpck, self.DataRxTx, self.cbSUM.GetValue())
				
			#Draw and Save blanks
			draw1 = ImageDraw.Draw(img1new)
			draw2 = ImageDraw.Draw(img2new)
			drawpck = ImageDraw.Draw(imgpcknew)
			path = self.saveFile(u" бланк ")
			if (path):
				img2new.save(path)
			if self.cbSUM.GetValue():
				path = self.saveFile(u" бланк наложенного")
				if (path):
					img1new.save(path)
			path = self.saveFile(u" бланк адресной")
			if (path):
				imgpcknew.save(path)
				
			self.saveRecipientInfo()
		settings_file = open("settings_paths", "w")
		settings_file.write(self.PathToExcelFile.encode('unicode-escape') + u'\n')
		settings_file.write(self.PathToBlanksFolder.encode('unicode-escape')+ u'\n')
		settings_file.close()
		
	def saveRecipientInfo(self):
		#Save settings recipient
		lines  = []
		lines.append(self.textFIOrx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textADRrx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textINDrx.GetValue().encode('unicode-escape') + u'\n')
		lines.append(self.textSUMrx.GetValue().encode('unicode-escape') + u'\n')
		self.DataRxTx.SaveRecipientInformation(lines);
	
	def saveFile(self, what_blank):
		saveFileDialog = wx.FileDialog(self, u"Сохранить как" + what_blank, "", what_blank, "Blank files (*.jpg)|*.jpg", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)								   
		saveFileDialog.ShowModal()
		path = saveFileDialog.GetPath()
		saveFileDialog.Destroy()
		return path
		
	def openExcelFile(self):
		"""
		Show the FileDialog and print the user's choice to stdout
		"""
		dlg = wx.FileDialog(self, u"Выберите Excel файл:", "", "", "Excel files (*.xls, *.xlsx)|*.xls; *.xlsx", wx.FD_OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.PathToExcelFile = dlg.GetPath()
			self.textPathToExcelFile.SetValue(self.PathToExcelFile)
		dlg.Destroy()
	
	def openBlankFolder(self):
		dlg = wx.DirDialog(self, u"Выберите папку для сохранения бланков:", "", style=wx.DD_DEFAULT_STYLE)
		if dlg.ShowModal() == wx.ID_OK:
			self.PathToBlanksFolder = dlg.GetPath()
			self.textPathToBlankFolder.SetValue(self.PathToBlanksFolder)
		dlg.Destroy()	
		
	def ButtonHandler(self, event):
		button = event.GetEventObject()
		if (button == self.generateButton):
			self.OnGenerate()
		elif (button == self.openExcelFileButton):
			self.openExcelFile()
		elif (button == self.openBlankFolderButton):
			self.openBlankFolder()
		
	def FromExcel(self, event):
		if self.cbFromExcel.GetValue():
			self.textFIOrx.Disable()
			self.textADRrx.Disable()
			self.textINDrx.Disable()
			self.textSUMrx.Disable()
			self.cbSUM.Disable()
			self.quoteFIOrx.Disable()
			self.quoteADRrx.Disable()
			self.quoteINDrx.Disable()
			self.quoteSUMrx.Disable()
			self.textPathToExcelFile.Enable()
			self.openExcelFileButton.Enable()
			self.textPathToBlankFolder.Enable()
			self.openBlankFolderButton.Enable()
			if (len(self.PathToExcelFile) < 5):
				self.openExcelFile()
			else: 
				self.textPathToExcelFile.SetValue(self.PathToExcelFile)
			if (len(self.PathToBlanksFolder) < 5):
				self.openBlankFolder()
			else:
				self.textPathToBlankFolder.SetValue(self.PathToBlanksFolder)

		else: 
			self.textFIOrx.Enable()
			self.textADRrx.Enable()
			self.textINDrx.Enable()
			self.textSUMrx.Enable()
			self.cbSUM.Enable()
			self.quoteFIOrx.Enable()
			self.quoteADRrx.Enable()
			self.quoteINDrx.Enable()
			self.quoteSUMrx.Enable()
			self.textPathToExcelFile.Disable()
			self.openExcelFileButton.Disable()
			self.textPathToBlankFolder.Disable()
			self.openBlankFolderButton.Disable()
			
