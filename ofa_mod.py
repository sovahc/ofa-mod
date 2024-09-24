# Oled Friendly Axis mod

def CONFIG(name, default):
	return inifile.find('DISPLAY', name) or default

SCALE = float(CONFIG('SCALE', 2.0))

# Randomize window position to avoid burn-in
OLED_SHIFT = int( CONFIG('OLED_SHIFT', 64 * SCALE) )
OLED_SHIFT = 0 ###############################333

FONT_NAME = CONFIG('FONT_NAME', 'mono')
FONT_SIZE = int( CONFIG('FONT_SIZE', 10 * SCALE) )
#GCODE_FONT_SIZE = int( CONFIG('GCODE_FONT_SIZE', 8 * SCALE) )
(BG, BG2, FG, SC) = (
	CONFIG('BACKGROUND', 'black'),
	CONFIG('BACKGROUND2', 'grey20'),
	CONFIG('FOREGROUND', 'white'),
	CONFIG('SELECTION', 'blue'))

BUTTON_SIZE = int( CONFIG('BUTTON_SIZE', 64 * SCALE) )

SLIDER_WIDTH = int( CONFIG('SLIDER_WIDTH', 200 * SCALE) )
SLIDER_HEIGHT = int( CONFIG('SLIDER_HEIGHT', 24 * SCALE) )

EXIT_DIALOG = int( CONFIG('EXIT_DIALOG', 0) )

import random
from PIL import ImageTk, Image
import os

def load_icons():
	r = []
	
	me = inifile.find('DISPLAY', 'USER_COMMAND_FILE')
	icons_file = os.path.split(me)[0] + "/ofa_icons.png"
	
	ofa_icons = Image.open(icons_file)
	(w, h) = ofa_icons.size
	count = w // h
	for i in range(0, count+1):
		icon = ofa_icons.crop((i*h, 0, i*h+h, h))
		photo = ImageTk.PhotoImage(icon)
		r.append(photo)
	
	return r

icons = load_icons() # keep reference to images as Tk wants

def rC(*args):
	root_window.tk.call(*args)

if EXIT_DIALOG == 0:
	rC("wm","protocol",".","WM_DELETE_WINDOW","destroy .")

def Bc(name):
	rC(name, "configure", "-background", BG);

def BFc(name):
	rC(name, "configure", "-background", BG, "-fg", FG);

def BFSc(name):
	rC(name, "configure", "-background", BG, '-fg', FG, '-selectcolor', SC);

next_icon = 1

def TOOLBARc(name):
	global next_icon
	rC(name, "configure", "-background", BG2, "-fg", FG);
	rC(name, "configure", '-width', BUTTON_SIZE, '-height', BUTTON_SIZE, '-borderwidth', 0)
	rC(name, "configure", '-image', icons[next_icon])
	next_icon += 1

# Workaround to get the size of the current screen in a multi-screen setup.
def get_curr_screen_geometry():
	root = Tkinter.Tk()
	root.update_idletasks()
	root.attributes('-fullscreen', True)
	root.state('iconic')
	geometry = root.winfo_geometry()
	root.destroy()
	
	geometry = geometry.replace('+', 'x').split('x')
	return [int(n) for n in geometry]

if OLED_SHIFT > 0:
	(w, h, x, y) = get_curr_screen_geometry()
	w -= OLED_SHIFT * 2
	h -= OLED_SHIFT * 2
	
	x += random.randint(0, OLED_SHIFT)
	y += random.randint(0, OLED_SHIFT)
	
	ng = '%dx%d+%d+%d' % (w, h, x, y)
	print('New window geometry', ng)
	root_window.tk.call("wm", "geometry", ".", ng)
else:
	root_window.attributes("-zoomed", 1)

rC('tk', 'scaling', SCALE)
rC('font','configure','TkDefaultFont','-family', FONT_NAME, '-size', FONT_SIZE)

# G-code font
rC('.pane.bottom.t.text', 'configure', '-foreground', 'blue', '-font', FONT_NAME)
rC('.pane.top.gcodes', 'configure', '-foreground', 'blue', '-font', FONT_NAME)

### Menu

BFc(".menu")
BFc(".menu.file")
BFc(".menu.file.recent")
BFc(".menu.machine")
BFc(".menu.machine.home")
BFc(".menu.machine.unhome")
BFc(".menu.view")
BFc(".menu.help")
BFc(".menu.machine.touchoff")
BFc(".menu.machine.clearoffset")

### Toolbar

Bc('.toolbar')
TOOLBARc(".toolbar.machine_estop")
TOOLBARc(".toolbar.machine_power")
TOOLBARc(".toolbar.file_open")
TOOLBARc(".toolbar.reload")
TOOLBARc(".toolbar.program_run")
TOOLBARc(".toolbar.program_step")
TOOLBARc(".toolbar.program_pause")
TOOLBARc(".toolbar.program_stop")
TOOLBARc(".toolbar.program_blockdelete")
TOOLBARc(".toolbar.program_optpause")
TOOLBARc(".toolbar.view_zoomin")
TOOLBARc(".toolbar.view_zoomout")
TOOLBARc(".toolbar.view_z")
TOOLBARc(".toolbar.view_z2")
TOOLBARc(".toolbar.view_x")
TOOLBARc(".toolbar.view_y")
TOOLBARc(".toolbar.view_p")
TOOLBARc(".toolbar.rotate")
TOOLBARc(".toolbar.clear_plot")

# Pane top tabs notebook
Bc('.pane.top')
BFc('.pane.top.tabs')
BFc('.pane.top.right')

rC('.pane.top.tabs','itemconfigure','manual',"-background",BG2,"-foreground",FG)
rC('.pane.top.tabs','itemconfigure','mdi',"-background",BG2,"-foreground",FG)
rC('.pane.top.right','itemconfigure','numbers',"-background",BG2,"-foreground",FG)
rC('.pane.top.right','itemconfigure','preview',"-background",BG2,"-foreground",FG)

#root_window.option_get(name, classname)

# Redo the text in tabs so they resize for the new default font
rC('.pane.top.tabs','itemconfigure','manual','-text',' Manual - F3 ')
rC('.pane.top.tabs','itemconfigure','mdi','-text',' MDI - F5 ')
rC('.pane.top.right','itemconfigure','preview','-text',' Preview ')
rC('.pane.top.right','itemconfigure','numbers','-text',' DRO ')

#### Radio buttons
def RADIOc(name):
	BFSc(name)
	rC(name, "configure", '-width', 2, '-height', 2)
	
RADIOc(".pane.top.tabs.fmanual.axes.axisx");
RADIOc(".pane.top.tabs.fmanual.axes.axisy");
RADIOc(".pane.top.tabs.fmanual.axes.axisz");

BFc(".pane.top.tabs");
Bc(".pane.top.tabs.fmanual");
BFc(".pane.top.tabs.fmanual.axis");

# XXX How to completely remove this label?
rC(".pane.top.tabs.fmanual.axis", 'configure', '-width', 1)
rC(".pane.top.tabs.fmanual.axis", "configure", "-background", BG, "-fg", BG);

Bc(".pane.top.tabs.fmanual.axes");
Bc(".pane.top.tabs.fmdi");

Bc(".pane.top.tabs.fmanual.joints");

## Jog buttons
Bc(".pane.top.tabs.fmanual.jogf");
Bc(".pane.top.tabs.fmanual.jogf.jog");

def JOGc(name):
	BFc(name)
	rC(name, "configure", '-width', 4, '-height', 2)

JOGc(".pane.top.tabs.fmanual.jogf.jog.jogminus");
JOGc(".pane.top.tabs.fmanual.jogf.jog.jogplus");
BFc(".pane.top.tabs.fmanual.jogf.jog.jogincr");

Bc(".pane.top.tabs.fmanual.jogf.zerohome");
BFc(".pane.top.tabs.fmanual.jogf.zerohome.home");
BFc(".pane.top.tabs.fmanual.jogf.zerohome.zero");
BFc(".pane.top.tabs.fmanual.jogf.zerohome.tooltouch");

### Override limits
BFc(".pane.top.tabs.fmanual.spindlel");
Bc(".pane.top.tabs.fmanual.spindlef");
Bc(".pane.top.tabs.fmanual.spindlef.row1");
Bc(".pane.top.tabs.fmanual.spindlef.row2");

### Spindle radio buton ccw

### Spindle radio buton cw
BFSc(".pane.top.tabs.fmanual.spindlef.ccw");
BFSc(".pane.top.tabs.fmanual.spindlef.cw");

BFc(".pane.top.tabs.fmanual.spindlef.spindleminus");
BFc(".pane.top.tabs.fmanual.spindlef.spindleplus");
BFc(".pane.top.tabs.fmanual.spindlef.brake");

BFc(".pane.top.tabs.fmanual.coolant");
BFSc(".pane.top.tabs.fmanual.mist");
BFSc(".pane.top.tabs.fmanual.flood");


BFc(".pane.top.tabs.fmdi.historyl");
BFc(".pane.top.tabs.fmdi.history");
Bc(".pane.top.tabs.fmdi.history.sby");

BFc(".pane.top.tabs.fmdi.commandl");
BFc(".pane.top.tabs.fmdi.go");

### Number tab
Bc(".info")
BFc(".info.task_state")
BFc(".info.tool")
BFc(".info.position")

Bc(".pane.bottom")
Bc(".pane.bottom.t")
BFc(".pane.bottom.t.text")
Bc(".pane.bottom.t.sb")

BFc(".pane.top.gcodel")
rC(".pane.top.gcodel", 'configure', '-text', "GCodes:")
BFc(".pane.top.gcodes")

Bc(".pane.top.ajogspeed")
BFc(".pane.top.ajogspeed.l0")
BFc(".pane.top.ajogspeed.l1")
BFc(".pane.top.ajogspeed.l")
BFc(".pane.top.ajogspeed.s")

Bc(".pane.top.jogspeed")
BFc(".pane.top.jogspeed.l0")
rC(".pane.top.jogspeed.l0", 'configure', '-text', "Jog:")
BFc(".pane.top.jogspeed.l1")
BFc(".pane.top.jogspeed.l")
BFc(".pane.top.jogspeed.s")

Bc(".pane.top.maxvel")
BFc(".pane.top.maxvel.l0")
rC(".pane.top.maxvel.l0", 'configure', '-text', "Speed:")
BFc(".pane.top.maxvel.l1")
BFc(".pane.top.maxvel.l")
BFc(".pane.top.maxvel.s")

Bc(".pane.top.spinoverride")
BFc(".pane.top.spinoverride.foscale")
BFc(".pane.top.spinoverride.foentry")
BFc(".pane.top.spinoverride.l")
BFc(".pane.top.spinoverride.m")

Bc(".pane.top.feedoverride")
BFc(".pane.top.feedoverride.foscale")
BFc(".pane.top.feedoverride.foentry")
BFc(".pane.top.feedoverride.l")
rC(".pane.top.feedoverride.l", 'configure', '-text', "Feed:")
BFc(".pane.top.feedoverride.m")

Bc(".pane.top.rapidoverride")
BFc(".pane.top.rapidoverride.foscale")
BFc(".pane.top.rapidoverride.foentry")
BFc(".pane.top.rapidoverride.l")
rC(".pane.top.rapidoverride.l", 'configure', '-text', "Rapid:")
BFc(".pane.top.rapidoverride.m")

def SCALEconfig(name):
	rC(name, 'configure', '-width', SLIDER_HEIGHT, '-length', SLIDER_WIDTH)

SCALEconfig('.pane.top.spinoverride.foscale')
SCALEconfig('.pane.top.feedoverride.foscale')
SCALEconfig('.pane.top.rapidoverride.foscale')
SCALEconfig('.pane.top.maxvel.s')
SCALEconfig('.pane.top.jogspeed.s')

### DRO
BFc('.pane.top.right.fnumbers.text')

"""
# Change plotter colors
try:
	live_plotter.logger.set_colors( # RGBA
		(255,0,0,255),     # jog
		(0,255,0,255),     # rapid
		(0,0,255,255),     # feed
		(255,255,0,255),   # arc
		(255,255,255,255), # toolchange
		(0,255,255,255))   # probe
except Exception as e:
	print(e)
"""
#rC('destroy', ".pane.top.tabs.fmanual.jogf.zerohome.tooltouch")
"""
from gi.repository import GObject
from gi.repository import Notify

class MyNotification(GObject.Object):
	def __init__(self):
		super(MyNotification, self).__init__()
		Notify.init("ofa_mod")

	def clear(self, iconname = None):
		print("->>> clear")

	def clear_one(self):
		print("->>> clear_one")

	def add(self, iconname, message):
		file_path_to_icon = ""
		n = Notify.Notification.new("NNNN", message, file_path_to_icon).show()

	def remove(self, widgets):
		print("->>> remove")

notifications = MyNotification()
"""

class MyNotification(Tkinter.Frame):
	def __init__(self, master):
		self.widgets = []
		Tkinter.Frame.__init__(self, master)
		
		self.configure(background=BG2)

	def clear(self, iconname = None):
		while self.widgets:
			self.remove(self.widgets[0])

	def clear_one(self):
		if self.widgets:
			self.remove(self.widgets[0])

	def add(self, iconname, message):
		message = message.rstrip()
		#print('MyNotification', iconname, message)
		
		self.place(relx=1, rely=1, y=-20, anchor="se")
		frame = Tkinter.Frame(self)
		button = Tkinter.Button(frame, text=message, wraplength=int(1000*SCALE),
			justify="left", compound="left", image=icons[0],
			background=BG2, fg=FG)
		
		wi = frame, button
		button.pack(side="left")
		button.configure(command=lambda: self.remove(wi))
		frame.pack(side="top", anchor="e")
		self.widgets.append(wi)

	def remove(self, widgets):
		widgets[0].destroy()
		
		self.widgets.remove(widgets)
		
		if len(self.widgets) == 0:
			self.place_forget()

notifications = MyNotification(root_window)
