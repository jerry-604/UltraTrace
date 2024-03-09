# import wx
# from .base import Module
# from .. import util
# from ..util.logging import *
# from ..widgets import CanvasTooltip
# import copy
# import tempfile

# LIBS_INSTALLED = False

# try:
#     from textgrid import TextGrid as TextGridFile, IntervalTier, PointTier, Point # textgrid
#     from textgrid.exceptions import TextGridError
#     LIBS_INSTALLED = True
# except ImportError as e:
#     warn(e)

# ALIGNMENT_TIER_NAMES = [ 'frames', 'all frames', 'dicom frames', 'ultrasound frames' ]

# class TextGrid(Module):
#     '''
#     Manages all the widgets related to TextGrid files, including the tier name
#     and the text content of that tier at a given frame
#     '''
#     def __init__(self, app):
#         '''
#         Keep a reference to the master object for binding the widgets we create
#         '''
#         info(' - initializing module: TextGrid')
#         self.app = app
#         self.frame = self.app.audioTGPanel
#         self.label_padx = 0
#         self.canvas_frame = self.app.audioTGPanel
#         self.TextGrid = None
#         self.selectedTier = ""
#         self.tg_zoom_factor = 1.5
#         self.canvas_width = 800
#         self.canvas_height = 60
#         self.collapse_height = 15
#         self.selectedIntvlFrames = []
#         self.selectedItem = None
#         self.start = 0
#         self.end = 0
#         self.current = 0
#         self.frame_shift = 0.00

#         self.startup()

#         platform = util.get_platform()
#         #bindings
#         if platform == 'Linux':
#             pass
#         # TODO: Add more bindings as needed
#     def setup(self):
#         '''
#         Set up the TextGrid widgets
#         '''
#         # Create the main panel for the TextGrid
#         self.panel = wx.Panel(self.frame)

#         # Create the tier name label
#         self.tierNameLabel = wx.StaticText(self.panel, label="Tier Name:")

#         # Create the tier name entry
#         self.tierNameEntry = wx.TextCtrl(self.panel, size=(200, -1))

#         # Create the text content label
#         self.textContentLabel = wx.StaticText(self.panel, label="Text Content:")

#         # Create the text content entry
#         self.textContentEntry = wx.TextCtrl(self.panel, size=(200, -1))

#         # Create the canvas for the TextGrid
#         self.canvas = wx.Panel(self.panel, size=(self.canvas_width, self.canvas_height))
#         self.canvas.SetBackgroundColour(wx.Colour(255, 255, 255))

#         # TODO: Add more widgets as needed

#         # Set up the layout using sizers
#         self.setup_layout()

#         # Bind events
#         self.bind_events()

#     def bind_events(self):
#         '''
#         Bind events for the TextGrid widgets
#         '''
#         self.tierNameEntry.Bind(wx.EVT_TEXT, self.on_tier_name_change)
#         self.textContentEntry.Bind(wx.EVT_TEXT, self.on_text_content_change)
#         # TODO: Bind more events as needed

#     def setup_layout(self):
#         '''
#         Set up the layout for the TextGrid widgets using sizers
#         '''
#         main_sizer = wx.BoxSizer(wx.VERTICAL)

#         # Tier name layout
#         tier_name_sizer = wx.BoxSizer(wx.HORIZONTAL)
#         tier_name_sizer.Add(self.tierNameLabel, 0, wx.ALL, 5)
#         tier_name_sizer.Add(self.tierNameEntry, 1, wx.ALL | wx.EXPAND, 5)
#         main_sizer.Add(tier_name_sizer, 0, wx.ALL | wx.EXPAND, 5)

#         # Text content layout
#         text_content_sizer = wx.BoxSizer(wx.HORIZONTAL)
#         text_content_sizer.Add(self.textContentLabel, 0, wx.ALL, 5)
#         text_content_sizer.Add(self.textContentEntry, 1, wx.ALL | wx.EXPAND, 5)
#         main_sizer.Add(text_content_sizer, 0, wx.ALL | wx.EXPAND, 5)

#         # Canvas layout
#         main_sizer.Add(self.canvas, 1, wx.ALL | wx.EXPAND, 5)

#         # TODO: Add more sizers as needed

#         self.panel.SetSizer(main_sizer)
#         self.panel.Layout()

import wx

class TextGrid(wx.Panel):
    # Initialization of the TextGrid panel
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL, name="TextGridPanel"):
        # Call the constructor of the wx.Panel class
        super(TextGrid, self).__init__(parent, id, pos, size, style, name)
        
        self.tiers = []  # Holds the tiers data, each tier containing intervals
        self.selectedInterval = None  # Stores the currently selected interval as (tier_index, column_index)
        
        # Set up the sizer for layout management
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        # (Add Tier button code is commented out)
        
        # Drawing panel where the TextGrid will be drawn
        self.drawingPanel = wx.Panel(self, size=wx.Size(800, 200))
        # Bind the paint event to the method that handles drawing
        self.drawingPanel.Bind(wx.EVT_PAINT, self.OnPaintDrawingPanel)
        # Bind the mouse down event to the method that handles interval selection
        self.drawingPanel.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        # Add the drawing panel to the sizer with expansion and border
        self.sizer.Add(self.drawingPanel, 1, wx.EXPAND | wx.ALL, 5)
        
        # Apply the sizer to the panel and lay out the components
        self.SetSizer(self.sizer)
        self.Layout()
        self.Fit()

    # Method called when the left mouse button is pressed
    def OnLeftDown(self, event):
        # Get the position of the mouse click and determine the selected interval
        x, y = event.GetPosition()
        self.selectedInterval = self.GetIntervalAtPosition(x, y)
        # Refresh the drawing panel to update the highlighted interval
        self.drawingPanel.Refresh()

    # Method to get the interval at a given x, y position
    def GetIntervalAtPosition(self, x, y):
        # Calculate the size of the drawing panel
        width, height = self.drawingPanel.GetClientSize()
        # Iterate through tiers to find which interval is clicked
        for tier_index, tier in enumerate(self.tiers):
            tier_height = height // len(self.tiers)
            # Check if y is within the current tier's vertical bounds
            if tier_index * tier_height <= y < (tier_index + 1) * tier_height:
                # Calculate the width of each interval in this tier
                interval_width = width // len(tier)
                # Determine which column has been clicked
                column_index = x // interval_width
                return (tier_index, column_index)
        return None

    # Method called when the drawing panel needs to be redrawn
    def OnPaintDrawingPanel(self, event):
        # Create a device context for drawing operations
        dc = wx.PaintDC(self.drawingPanel)
        # Clear the drawing area before redrawing
        dc.Clear()
        # Call method to draw the TextGrid
        self.DrawTextGrid(dc)

    # Method to draw highlighted columns around the selected interval
    def DrawHighlightedColumn(self, dc, x, y, interval_width, tier_height):
        # Set the pen for the highlighted column
        dc.SetPen(wx.Pen(wx.BLUE, 2))
        # Draw the left and right vertical lines of the selected interval
        dc.DrawLine(x, y, x, y + tier_height)  # Left vertical line
        dc.DrawLine(x + interval_width, y, x + interval_width, y + tier_height)  # Right vertical line

    def DrawTextGrid(self, dc):
        # Get the size of the drawing panel
        width, height = self.drawingPanel.GetClientSize()
        
        # Calculate the number of tiers and the height of each tier
        num_tiers = len(self.tiers)
        tier_height = height // num_tiers
        
        # Initialize the y position for drawing
        y = 0
        
        # Loop through each tier to draw its intervals
        for tier_index, tier in enumerate(self.tiers):
            # Determine the number of intervals in the current tier
            num_intervals = len(tier)
            
            # Calculate the width of each interval in the current tier
            interval_width = width // num_intervals
            
            # Loop through each interval in the current tier
            for i, (start_time, end_time, label) in enumerate(tier):
                # Calculate the x position for the current interval
                x = i * interval_width
                
                # Determine the width of the rectangle to draw for the interval
                rect_width = interval_width if i < num_intervals - 1 else width - x
                
                # Set the drawing color and style for the interval rectangle
                dc.SetPen(wx.Pen(wx.BLACK, 1))
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                
                # Draw the rectangle for the interval
                dc.DrawRectangle(x, y, rect_width, tier_height)
                
                # If the interval is selected, highlight it
                if self.selectedInterval and self.selectedInterval[0] == tier_index and self.selectedInterval[1] == i:
                    self.DrawHighlightedColumn(dc, x, y, interval_width, tier_height)
                
                # Wrap the text to fit within the interval and draw it
                wrapped_text = self.WrapText(dc, label, rect_width - 10)
                dc.DrawLabel(wrapped_text, wx.Rect(x + 5, y + 5, rect_width - 10, tier_height - 10), wx.ALIGN_LEFT | wx.ALIGN_TOP)
            
            # Move the y position to the next tier
            y += tier_height

    def WrapText(self, dc, text, max_width):
        # Initialize a list to hold lines of wrapped text
        wrapped_lines = []
        
        # Split the text into words
        words = text.split()
        
        # Start with the first word
        current_line = words[0]
        
        # Loop through the rest of the words
        for word in words[1:]:
            # Add the word to the current line if it fits
            line_with_word = current_line + ' ' + word if current_line else word
            text_width, text_height = dc.GetTextExtent(line_with_word)
            if text_width <= max_width:
                current_line = line_with_word
            else:
                # Otherwise, add the current line to the list and start a new line
                wrapped_lines.append(current_line)
                current_line = word
        
        # Add the last line to the list
        wrapped_lines.append(current_line)
        
        # Join the wrapped lines with newlines and return the result
        return '\n'.join(wrapped_lines)

    def SetTiers(self, tiers):
        # Update the tiers data and reset the selected interval
        self.tiers = tiers
        self.selectedInterval = None
        
        # Refresh the drawing panel to update the display
        self.Refresh()



# # Example usage
# class MainFrame(wx.Frame):
#     def __init__(self):
#         super(MainFrame, self).__init__(None, title="TextGrid Example")
#         panel = TextGridPanel(self)
        
#         # Example data
#         tiers = [
#             [(0, 1, 'Tier 1'), (1, 2, 'Interval 1'), (2, 3, 'Interval 2')],
#             [(0, 1, 'Tier 2'), (1, 2, 'Interval A'), (2, 3, 'Interval B')],
#         ]
#         panel.SetTiers(tiers)
        
#         self.Show()

# if __name__ == "__main__":
#     app = wx.App(False)
#     frame = MainFrame()
#     app.MainLoop()
