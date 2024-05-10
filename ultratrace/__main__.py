#!/usr/bin/env python3

#import modules
from . import modules
from . import util
import parselmouth
from .util.logging import *
from .widgets import Header
from ultratrace.modules.textgrid import TextGrid

import argparse
import os
import PIL

import wx

class Frame(wx.Frame):
	
	#def __init__(self, parent, title):
	#	super(Frame, self).__init__(parent, title=title)
	def __init__(self, *a, **k):
		wx.Frame.__init__(self, *a, **k, )


		self.SetSize((200, 600))  # Set the initial size of the main frame
		# self.Centre(wx.BOTH)  # Center on screen
		# self.Show()

		info( 'initialising UltraTrace' )
		self.preinitialise()

		info( ' - initialising interface' )
		self.setWidgetDefaults()
		modules.panels.Panel_root(self)
		# self.buildWidgetSkeleton()
		
		info( ' - initialising modules' )
		self.initialiserest()
		self.CentreOnScreen()

	def preinitialise(self):

		# check if we were passed a command line argument
		parser = argparse.ArgumentParser(prog='UltraTrace')
		parser.add_argument('path', help='path (unique to a participant) where subdirectories contain raw data', default=None, nargs='?')

		args = parser.parse_args()

		# initialize data module
		self.Data = modules.Metadata( self, args.path )

		# initialize the main app widgets
		# self.setWidgetDefaults()
		# self.buildWidgetSkeleton()

	def initialiserest(self):
		# initialize other modules
		# self.Control = modules.Control(self)
		self.snd = parselmouth.Sound("/Users/jeremiah/Documents/ultrasound-data-example/20150629171639.flac")

		self.Trace = modules.Trace(self)
		# self.Dicom = modules.Dicom(self)
		# self.Audio = modules.Playback(self)
		# self.TextGrid = modules.TextGrid(self)
		# self.TextGrid = modules.TextGrid(self)
		self.TextGrid = TextGrid(self)
		self.Spectrogram = modules.Spectrogram(self)

        
		# tiers = [
		# 	# First tier with sentences
		# 	[(0, 1, "A quick brown fox jumps over the lazy dog near the riverbank."),
		# 	(1, 2, "Bright vixens jump; dozy fowl quack."),
		# 	(2, 3, "Quick zephyrs blow, vexing daft Jim."),
		# 	(3, 4, "Sphinx of black quartz, judge my vow.")],

		# 	# Second tier with words from each sentence
		# 	[(0, 0.2, "A"), (0.2, 0.4, "quick"), (0.4, 0.6, "brown"), (0.6, 0.8, "fox"), (0.8, 1, "jumps"),
		# 	(1, 1.125, "over"), (1.125, 1.25, "the"), (1.25, 1.375, "lazy"), (1.375, 1.5, "dog"), (1.5, 1.625, "near"), (1.625, 1.75, "the"), (1.75, 1.875, "riverbank"),
		# 	(2, 2.1, "Bright"), (2.1, 2.2, "vixens"), (2.2, 2.3, "jump;"), (2.3, 2.4, "dozy"), (2.4, 2.5, "fowl"), (2.5, 2.6, "quack"),
		# 	(3, 3.1, "Quick"), (3.1, 3.2, "zephyrs"), (3.2, 3.3, "blow,"), (3.3, 3.4, "vexing"), (3.4, 3.5, "daft"), (3.5, 3.6, "Jim"),
		# 	(4, 4.1, "Sphinx"), (4.1, 4.2, "of"), (4.2, 4.3, "black"), (4.3, 4.4, "quartz,"), (4.4, 4.5, "judge"), (4.5, 4.6, "my"), (4.6, 4.7, "vow")],

		# 	# Third tier with vowels from each word
		# 	[(0, 0.05, "A"), (0.2, 0.25, "ui"), (0.4, 0.45, "o"), (0.6, 0.65, "o"), (0.8, 0.85, "u"),
		# 	(1, 1.06, "o"), (1.125, 1.18, "e"), (1.25, 1.3, "a"), (1.375, 1.43, "o"), (1.5, 1.56, "ea"), (1.625, 1.68, "e"), (1.75, 1.8, "iea"),
		# 	(2, 2.05, "i"), (2.1, 2.15, "ie"), (2.2, 2.25, "u;"), (2.3, 2.35, "o"), (2.4, 2.45, "o"), (2.5, 2.55, "ua"),
		# 	(3, 3.05, "ui"), (3.1, 3.15, "e"), (3.2, 3.25, "o,"), (3.3, 3.35, "ei"), (3.4, 3.45, "a"), (3.5, 3.55, "i"),
		# 	(4, 4.05, "i"), (4.1, 4.15, "o"), (4.2, 4.25, "a"), (4.3, 4.35, "ua,"), (4.4, 4.45, "ue"), (4.5, 4.55, "y"), (4.6, 4.65, "o")]
		# ]



		
		# self.TextGrid.SetTiers(tiers)
		self.TextGrid.LoadTextGrid("/Users/jeremiah/Documents/ultrasound-data-example/20150629171639.TextGrid")
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer.AddSpacer(350)  # Space from the top of the frame to the Spectrogram

        # Create a horizontal sizer for the Spectrogram to add padding
		spectrogram_sizer = wx.BoxSizer(wx.HORIZONTAL)
		spectrogram_sizer.AddSpacer(300)  # Left padding for the Spectrogram
		spectrogram_sizer.Add(self.Spectrogram, proportion=1, flag=wx.EXPAND | wx.ALL, border=2)
		spectrogram_sizer.AddSpacer(1)  # Right padding for the Spectrogram

        # Add the spectrogram_sizer to the mainSizer
		mainSizer.Add(spectrogram_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=2)

        # Create a horizontal sizer for the TextGrid to add padding
		horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
		horizontal_sizer.AddSpacer(403)  # Left padding for the TextGrid
		horizontal_sizer.Add(self.TextGrid, proportion=1, flag=wx.EXPAND | wx.ALL, border=2)
		horizontal_sizer.AddSpacer(1)  # Right padding for the TextGrid

        # Add the horizontal_sizer to the mainSizer
		mainSizer.Add(horizontal_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=2)
		mainSizer.AddSpacer(50)  # Space at the bottom of the frame

		self.SetSizer(mainSizer)

		# self.Spectrogram = modules.Spectrogram(self)
		# self.Search = modules.Search(self)

		info( ' - loading widgets' )

		#self.filesUpdate()

		# to deal with resize handler being called multiple times
		# in a single window resize
		self.isResizing = False

		#self.oldwidth = self.winfo_width()

		#self.after(300,self.afterstartup)

	def setWidgetDefaults(self):
		'''
		Need to set up some defaults here before building Tk widgets (this is specifically
		true w/r/t the StringVars)
		'''
		self.currentFID = 0 	# file index w/in list of sorted files
		self.frame = 0			# current frame of dicom file
		self.isClicked = False	# used in handling of canvas click events
		self.isDragging = False # used in handling of canvas click events
		# self.resized = False 	#for changing widgets after window resize
		self.selectBoxX = False
		self.selectBoxY = False

		# some styling
		#self.fontStyle = Style()
		#if util.get_platform() == 'Darwin':
		#	self.fontStyle.configure('symbol.TButton', font=('DejaVu Serif', 26))
		#else:
		#	self.fontStyle.configure('symbol.TButton', font=('DejaVu Serif', 19))

		# declare string variables
		#self.currentFileSV = StringVar(self)
		#self.frameSV = StringVar(self)

		# initialize string variables
		self.currentFileSV = self.Data.files[ self.currentFID ]
		self.frameSV = '1'

	def buildWidgetSkeleton(self):
		'''
		Builds the basic skeleton of our app widgets.
			- items marked with (*) are built directly in this function
			- items marked with (~) are built by the individual modules
			# WARNING: out of date diagram
		.________________________________________.
		|	ROOT 						         |
		| .____________________________________. |
		| |          TOP*                      | |
		| | ._______________. .______________. | |
		| | |   LEFT*       | |   RIGHT*     | | |
		| | |   - file nav* | |   - dicom~   | | |
		| | |   - frame nav*| |              | | |
		| | |   - traces~   | |              | | |
		| | |   - undo~     | |              | | |
		| | \_______________/ \______________/ | |
		| \____________________________________/ |
		|	    							     |
		| .____________________________________. |
		| |           BOTTOM*                  | |
		| |           - spectrogram~           | |
		| |           - textgrid~              | |
		| \____________________________________/ |
		\________________________________________/
		'''
		# main Frame skeleton
		self.panel = wx.Panel(self)
		self.hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.grid = wx.FlexGridSizer(2, 2, 2, 2)
		
		#self.TOP = wx.Panel(self)
		#self.TOP = Frame(self)
		#self.TOP.columnconfigure(1,weight=1, minsize=320)
		#self.TOP.rowconfigure(0,weight=1, minsize=240)
		#self.LEFT = Frame(self.TOP)
		## self.LEFT.rowconfigure(0,weight=1)
		## self.LEFT.columnconfigure(0,weight=1)
		#self.RIGHT = Frame(self.TOP)
		#self.RIGHT.rowconfigure(0,weight=1)
		#self.RIGHT.columnconfigure(0,weight=1)
		#self.BOTTOM = Frame(self)
		## self.BOTTOM.columnconfigure(0,weight=1)
		#self.BOTTOM.columnconfigure(1,weight=1)
		## self.BOTTOM.rowconfigure(0,weight=1)
		## self.TOP.grid(    row=0, column=0, sticky='nw')
		## self.LEFT.grid(   row=0, sticky='n' )
		## self.RIGHT.grid(  row=0, column=1)
		## self.BOTTOM.grid( row=1, column=0, sticky='e')
		#self.TOP.grid(    row=0, column=0, sticky='nesw')
		#self.LEFT.grid(   row=0, sticky='nesw' )
		#self.RIGHT.grid(  row=0, column=1, sticky='nesw')
		#self.BOTTOM.grid( row=1, column=0, sticky='nesw')
		#self.pady=3
		#self.columnconfigure(0,weight=1)
		#self.rowconfigure(0,weight=1)
		#text1 = wx.StaticText(panel, label="controls here")
		text2 = wx.StaticText(self.panel, label="US here")
		text3 = wx.StaticText(self.panel, label="labels here")
		text4 = wx.StaticText(self.panel, label="audio and textgrids here")

		self.audioTGBox = wx.BoxSizer(wx.VERTICAL)
		self.audioTGBox.Add(text4)

		self.ultrasoundBox = wx.BoxSizer(wx.VERTICAL)
		self.ultrasoundBox.Add(text2)

		self.controlBox = wx.BoxSizer(wx.VERTICAL)
		####  Buttons
		####  FileSelectorBox
		##### FileControlBox
		self.fileControlBox = wx.BoxSizer(wx.HORIZONTAL)
		self.fileSelectorOpen = wx.Button(self, id=wx.ID_OPEN)#, style=wx.BU_NOTEXT)
		self.fileControlBox.Add(self.fileSelectorOpen)

		self.fileSelectorBox = wx.StaticBoxSizer(wx.VERTICAL, self, label="Files")
		self.fileSelectorBox.Add(self.fileControlBox)
		self.fileSelector = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
		self.fileSelector.InsertColumn(0, 'name', width=200)
		self.fileSelector.InsertColumn(1, 'annotated', wx.LIST_FORMAT_RIGHT, width=50)
		#self.fileSelector.InsertItem(0, 'test')
		for filedata in self.Data.files:
			self.fileSelector.InsertItem(self.fileSelector.GetItemCount(), filedata)

		self.fileSelectorBox.Add(self.fileSelector, 1, wx.EXPAND)

		####  FrameSelectorBox
		self.frameSelectorBox = wx.StaticBoxSizer(wx.HORIZONTAL, self, label="Frames")
		self.frameSelectorPrev = wx.Button(self, label="<", style=wx.BU_EXACTFIT)
		self.frameSelectorText = wx.TextCtrl(self, style=wx.TE_RIGHT, value=self.frameSV)
		self.frameSelectorNext = wx.Button(self, label=">", style=wx.BU_EXACTFIT)
		self.buttonPlayPause = wx.Button(self, label="⏯")# style=wx.BU_EXACTFIT)
		self.setCharSize(self.frameSelectorNext, 1)
		self.setCharSize(self.frameSelectorText, 5)
		self.setCharSize(self.frameSelectorPrev, 1)
		self.setCharSize(self.buttonPlayPause, 3)

		#self.frameSelectorBox.AddMany([(self.frameSelectorPrev),(self.frameSelectorText),(self.frameSelectorNext),(self.buttonPlayPause)])
		self.frameSelectorBox.Add(self.frameSelectorPrev, flag=wx.LEFT, border=10)
		self.frameSelectorBox.Add(self.frameSelectorText)
		self.frameSelectorBox.Add(self.frameSelectorNext, flag=wx.RIGHT, border=10)
		self.frameSelectorBox.Add(self.buttonPlayPause, border=10)

		####  AnnotationsBox
		self.annotationsBox = wx.StaticBoxSizer(wx.HORIZONTAL, self, label="Annotations")
		self.buttonSelectAll = self.newIconButton(wx.ID_SELECTALL, "gtk-select-all")
		self.buttonCopy = self.newIconButton(wx.ID_COPY, wx.ART_COPY)
		#self.buttonCopy = wx.Button(self, id=wx.ID_COPY, style=wx.BU_NOTEXT | wx.BU_EXACTFIT)
		#self.buttonCopy = wx.BitmapButton(self, id=wx.ID_COPY, bitmap=wx.ArtProvider.GetBitmap(wx.ART_COPY), size=(32,32))
		self.buttonPaste = self.newIconButton(wx.ID_PASTE, wx.ART_PASTE) #wx.Button(self, id=wx.ID_PASTE, style=wx.BU_NOTEXT | wx.BU_EXACTFIT)
		#self.buttonPaste = wx.BitmapButton(self, id=wx.ID_PASTE, bitmap=wx.ArtProvider.GetBitmap(wx.ART_PASTE), size=(32,32))
		self.buttonDelete = self.newIconButton(wx.ID_DELETE, wx.ART_DELETE) #wx.Button(self, id=wx.ID_DELETE, style=wx.BU_NOTEXT | wx.BU_EXACTFIT)
		self.buttonZoomIn = self.newIconButton(wx.ID_ZOOM_IN, "gtk-zoom-in") #wx.Button(self, id=wx.ID_ZOOM_IN, style=wx.BU_NOTEXT | wx.BU_EXACTFIT)
		self.buttonZoomOut = self.newIconButton(wx.ID_ZOOM_OUT, "gtk-zoom-out") #wx.Button(self, id=wx.ID_ZOOM_OUT, style=wx.BU_NOTEXT | wx.BU_EXACTFIT)
		self.buttonZoomFit = self.newIconButton(wx.ID_ZOOM_FIT, "gtk-zoom-fit") #wx.Button(self, id=wx.ID_ZOOM_FIT, style=wx.BU_NOTEXT | wx.BU_EXACTFIT)
		self.buttonUndo = self.newIconButton(wx.ID_UNDO, wx.ART_UNDO)
		self.buttonRedo = self.newIconButton(wx.ID_REDO, wx.ART_REDO)

		#self.annotationsBox.AddMany([(self.buttonSelectAll),(self.buttonCopy),(self.buttonPaste),(self.buttonDelete)])
		self.annotationsBox.Add(self.buttonSelectAll, flag=wx.LEFT, border=10)
		self.annotationsBox.Add(self.buttonCopy, flag=wx.BOTTOM, border=10)
		self.annotationsBox.Add(self.buttonPaste)
		self.annotationsBox.Add(self.buttonDelete)
		self.annotationsBox.Add((20,0))
		self.annotationsBox.Add(self.buttonUndo)
		self.annotationsBox.Add(self.buttonRedo, flag=wx.RIGHT, border=10)


		####  ViewBox
		self.viewBox = wx.StaticBoxSizer(wx.HORIZONTAL, self, label="View")
		self.viewBox.Add(self.buttonZoomIn, flag=wx.LEFT, border=10)
		self.viewBox.Add(self.buttonZoomOut, flag=wx.BOTTOM, border=10)
		self.viewBox.Add(self.buttonZoomFit, flag=wx.RIGHT, border=10)

		####  LayersBox
		#self.layersBox = wx.StaticBoxSizer(wx.VERTICAL, self, label="Layers")

		## add all sections to the control box
		self.controlBox.AddMany([(self.fileSelectorBox, 1, wx.EXPAND), ((0,10)), (self.frameSelectorBox,0,wx.EXPAND), ((0,10)), (self.annotationsBox, 0, wx.EXPAND), ((0,10)), (self.viewBox,0,wx.EXPAND), ((0,10)) ])#(self.layersBox,0,wx.EXPAND)])

		self.grid.AddMany([(self.controlBox, 1, wx.EXPAND), (self.ultrasoundBox, 1, wx.EXPAND), (text3), (self.audioTGBox)])

		self.grid.AddGrowableRow(0,1)
		self.grid.AddGrowableCol(0,1)

		self.hbox.Add(self.grid, proportion=1, flag=wx.ALL|wx.EXPAND, border=2)
		self.panel.SetSizer(self.hbox)
		self.panel.Fit()
		## navigate between all available filenames in this directory
		#self.filesFrame = Frame(self.LEFT)#, pady=7)
		#self.filesPrevBtn = Button(self.filesFrame, text='<', command=self.filesPrev, takefocus=0, width="1.5")
		#self.filesJumpToMenu = OptionMenu(self.filesFrame, self.currentFileSV, self.Data.files[0], *self.Data.files, command=self.filesJumpTo)
		#self.filesNextBtn= Button(self.filesFrame, text='>', command=self.filesNext, takefocus=0, width="1.5")
		#self.filesFrame.grid( row=1 )
		#self.filesPrevBtn.grid( row=1, column=0 )
		#self.filesJumpToMenu.grid( row=1, column=1 )
		#self.filesNextBtn.grid(row=1, column=2 )
		#Header(self.filesFrame, text="Recording").grid( row=0, column=0, columnspan=3 )

		## navigate between frames
		#self.framesFrame = Frame(self.LEFT)#, pady=7)
		#self.framesSubframe = Frame(self.framesFrame)
		#self.framesPrevBtn = Button(self.framesSubframe, text='<', command=self.framesPrev, takefocus=0, width="1.5")
		#self.framesEntryText = Entry(self.framesSubframe, width=5, textvariable=self.frameSV)
		#self.framesEntryBtn = Button(self.framesSubframe, text='Go', command=self.framesJumpTo, takefocus=0, width="3")
		#self.framesNextBtn= Button(self.framesSubframe, text='>', command=self.framesNext, takefocus=0, width="1.5")
		#self.framesHeader = Header(self.framesFrame, text="Frame")
		#self.framesFrame.grid( row=3 )
		#self.framesSubframe.grid( row=1 )

		## non-module-specific bindings
		#if util.get_platform() == 'Linux':
		#	self.bind('<Control-Left>', self.filesPrev )
		#	self.bind('<Control-Right>', self.filesNext )
		#else:
		#	self.bind('<Option-Left>', self.filesPrev )
		#	self.bind('<Option-Right>', self.filesNext )
		#self.bind('<Left>', self.framesPrev )
		#self.bind('<Right>', self.framesNext )
		#self.bind('<BackSpace>', self.onBackspace )
		#self.bind('<Button-1>', self.getWinSize)
		#self.bind('<ButtonRelease-1>', self.onRelease)
		#self.bind('<Double-Button-1>', self.onDoubleClick)
		#self.bind('<Escape>', self.onEscape )
		## self.count = 0

		#self.framesEntryText.bind('<Return>', self.unfocusAndJump)
		#self.framesEntryText.bind('<Escape>', lambda ev: self.framesFrame.focus())

		# force window to front
		#self.lift()

	def setCharSize(self, obj, sizeInChar):
		size = obj.GetSizeFromTextSize(obj.GetTextExtent('9'*sizeInChar))
		obj.SetInitialSize(size)
		obj.SetSize(size)

	def newIconButton(self, wxId, wxBmp):
		#button = wx.Button(self, id=wxId, style=wx.BU_NOTEXT | wx.BU_EXACTFIT)
		#button.SetBitmapLabel(wx.ArtProvider.GetBitmap(wxBmp,wx.ART_MENU))
		button = wx.BitmapButton(self, id=wxId, bitmap=wx.ArtProvider.GetBitmap(wxBmp), size=(32,32))
		return button

	def lift(self):
		'''
		Bring window to front (doesn't shift focus to window)
		'''
		self.attributes('-topmost', 1)
		self.attributes('-topmost', 0)

	def update(self):
		pass

	def geometry(self):
		pass



if __name__=='__main__':
	# app.mainloop()
	app = wx.App()
	mainFrame = Frame(None, title='UltraTrace')
	mainFrame.Show()
	while True:
		try:
			app.MainLoop()
			break
		except:
			print("crashed")
		#except UnicodeDecodeError as e:
		#	error(e)
