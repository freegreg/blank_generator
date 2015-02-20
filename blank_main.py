# -*- coding: utf-8 -*-
import wx
import blank_rx
import blank_tx

import os.path
import sys
class MainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title= u"Интерет Магазин Пневматики Popadiv10.ru", pos=(150,150), size=(830,670))

		self.CreateStatusBar()
		# A Statusbar in the bottom of the window
		#self.statusbar = self.CreateStatusBar(style=0)
		self.SetStatusText('autor:Gutu Grigori Grigori')
		
		# Setting up the menu.
		filemenu= wx.Menu()
		menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
		menuExit = filemenu.Append(wx.ID_EXIT, "&Exit"," Terminate the program")
		
		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar

		self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
		
		# Events.
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

		# finally, put the notebook in a sizer for the panel to manage
		# the layout
		
		# Here we create a panel and a notebook on the panel
		panel = wx.Panel(self)
		nb = wx.Notebook(panel)
		
		# create the page windows as children of the notebook
		TxPage = blank_tx.TxPage(nb)
		RxPage = blank_rx.RxPage(nb, TxPage)
		
		TxPage.Disable()
		# add the pages to the notebook with the label to show on the tab
		nb.AddPage(RxPage, u"Бланк 1 - Данные получателя")
		nb.AddPage(TxPage, u"Бланк 2 - Данные отправителя")

		sizer = wx.BoxSizer()
		sizer.Add(nb, 1, wx.ALL|wx.EXPAND, 5)
		panel.SetSizer(sizer)
		
	def OnAbout(self,e):
		# Create a message dialog box
		dlg = wx.MessageDialog(self, " gggrinea@gmail.com", "About Blank Generator", wx.OK)
		dlg.ShowModal() # Shows it
		dlg.Destroy() # finally destroy it when finished.

	def OnExit(self,e):
		self.Close(True)  # Close the frame.

if __name__ == "__main__":
	app = wx.App()
	MainFrame().Show()
	app.MainLoop()