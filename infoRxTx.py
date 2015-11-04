# -*- coding: utf-8 -*-
import os

class infoRxTx:
		
	lines_rx = []
	lines_tx = []
	def __init__(self):

		for index in range(0, 6):
			self.lines_rx.append(u'')
		for index in range(0, 9):
			self.lines_tx.append(u'')
		#Open file with recipient's information
		file_rx = open("settings_rx", "r")
		with file_rx as f:
			self.lines_rx = [line.decode('unicode-escape').rstrip(u'\n') for line in f]
		file_rx.close()
		
		#Open file with sender's information
		file_tx = open("settings_tx", "r")
		with file_tx as f:
			self.lines_tx = [line.decode('unicode-escape').rstrip(u'\n') for line in f]
		file_tx.close()	
				
	def GetFioRx(self):
		return self.lines_rx[0]
	
	def GetAddressRx(self):
		return self.lines_rx[1]
		
	def GetIndexRx(self):
		return self.lines_rx[2]
		
	def GetCashSum(self):
		return self.lines_rx[3]
	
	def GetPackNumber(self):
		return self.lines_rx[4]
	
	def GetWeight(self):
		return self.lines_rx[5]
		
	def GetFioTx(self):
		return self.lines_tx[0]
		
	def GetAddressTx(self):
		return self.lines_tx[1]
		
	def GetIndexTx(self):
		return self.lines_tx[2]
		
	def GetPassportIDTx(self):
		return self.lines_tx[3]

	def GetPassportSerialTx(self):
		return self.lines_tx[4]
		
	def GetPassportNumberTx(self):
		return self.lines_tx[5]

	def GetPassportDataTx(self):
		return self.lines_tx[6]
		
	def GetPassportYearTx(self):
		return self.lines_tx[7]
		
	def GetPassportAddressTx(self):
		return self.lines_tx[8]	
		
	def SaveSenderInformation(self, lines):
		settings_file = open("settings_tx", "w")
		with settings_file as f:
			for s in lines:
				f.write(s)
		settings_file.close()
		
		#Open file with sender's information
		file_tx = open("settings_tx", "r")
		with file_tx as f:
			self.lines_tx = [line.decode('unicode-escape').rstrip(u'\n') for line in f]
		file_tx.close()	
		
	def SaveRecipientInformation(self, lines):
		settings_file = open("settings_rx", "w")
		with settings_file as f:
			for s in lines:
				f.write(s)
		settings_file.close()
				
	def SetRecipientInformation(self, lines):
		self.lines_rx = list(lines)
		
	def SetSenderInformation(self, lines):
		self.lines_tx = list(lines)
