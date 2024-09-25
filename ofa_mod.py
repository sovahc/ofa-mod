# Oled Friendly Axis mod

def CONFIG(name, default):
	return inifile.find('DISPLAY', name) or default

FULLSCREEN = int( CONFIG('FULLSCREEN', 0) )

SCALE = float( CONFIG('SCALE', 2.0) )

# Randomize window position to avoid burn-in
OLED_SHIFT = int( CONFIG('OLED_SHIFT', 64 * SCALE) )

FONT_NAME = CONFIG('FONT_NAME', 'mono')
FONT_SIZE = int( CONFIG('FONT_SIZE', 10 * SCALE) )

(BG, BG2, FG, SC) = (
	CONFIG('BACKGROUND', 'black'),
	CONFIG('BACKGROUND2', 'grey20'),
	CONFIG('FOREGROUND', 'white'),
	CONFIG('SELECTION', 'blue'))

BUTTON_SIZE = int( CONFIG('BUTTON_SIZE', 64 * SCALE) )

SLIDER_WIDTH = int( CONFIG('SLIDER_WIDTH', 320 * SCALE) )
SLIDER_HEIGHT = int( CONFIG('SLIDER_HEIGHT', 32 * SCALE) )

EXIT_DIALOG = int( CONFIG('EXIT_DIALOG', 0) )

import random
from PIL import ImageTk, Image
import os

def load_icons(filename):
	r = []
	
	me = inifile.find('DISPLAY', 'USER_COMMAND_FILE')
	icons_file = os.path.split(me)[0] + filename
	
	ofa_icons = Image.open(icons_file)
	(w, h) = ofa_icons.size
	count = w // h
	for i in range(0, count):
		icon = ofa_icons.crop((i*h, 0, i*h+h, h))
		
		(iw, ih) = icon.size
		if iw != BUTTON_SIZE or ih != BUTTON_SIZE:
			icon = icon.resize((BUTTON_SIZE, BUTTON_SIZE), resample = Image.Resampling.LANCZOS)
		
		photo = ImageTk.PhotoImage(icon)
		r.append(photo)
	
	return r

# keep reference to images as Tk wants
toolbar_icons = load_icons("/toolbar_icons.png")
message_icons = {}
(message_icons['info'], message_icons['error']) = load_icons("/message_icons.png")

def rC(*args):
	return root_window.tk.call(*args)

if EXIT_DIALOG == 0:
	rC("wm","protocol",".","WM_DELETE_WINDOW","destroy .")

def Bc(name):
	rC(name, "configure", "-background", BG);

def BFc(name):
	rC(name, "configure", "-background", BG, "-fg", FG);

def BFSc(name):
	rC(name, "configure", "-background", BG, '-fg', FG, '-selectcolor', SC);

def TOOLBARc(index, name):
	global next_icon
	rC(name, "configure", "-background", BG2, "-fg", FG);
	rC(name, "configure", '-width', BUTTON_SIZE, '-height', BUTTON_SIZE, '-borderwidth', 0)
	rC(name, "configure", '-image', toolbar_icons[index])

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

if FULLSCREEN != 0:
	root_window.attributes("-fullscreen", True)
elif OLED_SHIFT > 0:
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
TOOLBARc(0, ".toolbar.machine_estop")
TOOLBARc(1, ".toolbar.machine_power")
TOOLBARc(2, ".toolbar.file_open")
TOOLBARc(3, ".toolbar.reload")
TOOLBARc(4, ".toolbar.program_run")
TOOLBARc(5, ".toolbar.program_step")
TOOLBARc(6, ".toolbar.program_pause")
TOOLBARc(7, ".toolbar.program_stop")
TOOLBARc(8, ".toolbar.program_blockdelete")
TOOLBARc(9, ".toolbar.program_optpause")
TOOLBARc(10, ".toolbar.view_zoomin")
TOOLBARc(11, ".toolbar.view_zoomout")
TOOLBARc(12, ".toolbar.view_z")
TOOLBARc(13, ".toolbar.view_z2")
TOOLBARc(14, ".toolbar.view_x")
TOOLBARc(15, ".toolbar.view_y")
TOOLBARc(16, ".toolbar.view_p")
TOOLBARc(17, ".toolbar.rotate")
TOOLBARc(18, ".toolbar.clear_plot")


def VRULE(name):
	rC(name, 'configure', "-background", BG, '-width', int(10 * SCALE),
		'-borderwidth', 0, '-padx', 0, '-pady', 0)

VRULE('.toolbar.rule0')
VRULE('.toolbar.rule4')
VRULE('.toolbar.rule8')
VRULE('.toolbar.rule9')
VRULE('.toolbar.rule12')

# Pane top tabs notebook
Bc('.pane.top')
BFc('.pane.top.tabs')
BFc('.pane.top.right')

def REDO_TEXT(name, item):
	rC(name,'itemconfigure',item,"-background",BG2,"-foreground",FG)
	
	text = rC(name,'itemcget',item,'-text')
	rC(name,'itemconfigure',item,'-text', ' ' + text)

# Redo the text in tabs so they resize for the new default font
REDO_TEXT('.pane.top.tabs', 'manual')
REDO_TEXT('.pane.top.tabs', 'mdi')
REDO_TEXT('.pane.top.right', 'preview')
REDO_TEXT('.pane.top.right', 'numbers')

#### Radio buttons
for ax in 'xyzabcuvw':
	name = ".pane.top.tabs.fmanual.axes.axis" + ax;
	BFSc(name)
	rC(name, "configure", '-width', 4, '-height', 2, '-indicatoron', False, '-anchor', 'center')

BFc(".pane.top.tabs");
Bc(".pane.top.tabs.fmanual");
BFc(".pane.top.tabs.fmanual.axis");

rC('grid', 'forget', ".pane.top.tabs.fmanual.axis")

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

# swapping
rC('grid', ".pane.top.tabs.fmanual.jogf.jog.jogincr", '-column', 1, '-row', 0)
rC('grid', ".pane.top.tabs.fmanual.jogf.jog.jogplus", '-column', 2, '-row', 0)

Bc(".pane.top.tabs.fmanual.jogf.zerohome");

def HOMEc(name):
	BFc(name)
	rC(name, "configure", '-height', 2)

HOMEc(".pane.top.tabs.fmanual.jogf.zerohome.home");
HOMEc(".pane.top.tabs.fmanual.jogf.zerohome.zero");
HOMEc(".pane.top.tabs.fmanual.jogf.zerohome.tooltouch");

### Override limits
BFc(".pane.top.tabs.fmanual.spindlel");
Bc(".pane.top.tabs.fmanual.spindlef");
Bc(".pane.top.tabs.fmanual.spindlef.row1");
Bc(".pane.top.tabs.fmanual.spindlef.row2");

### Spindle radio butons
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
BFc(".pane.top.gcodes")

def TUNE_SLIDER(index, base, scale, a, b, c):
	Bc(base)
	BFc(base + scale)
	BFc(base + a)
	BFc(base + b)
	BFc(base + c)
	
	rC(base + scale, 'configure', '-width', SLIDER_HEIGHT, '-length', SLIDER_WIDTH)

	rC('pack', 'forget', base + scale)
	rC('pack', 'forget', base + a)
	rC('pack', 'forget', base + b)
	rC('pack', 'forget', base + c)
	
	row = 2+index*2
	
	rC('grid', base + a, '-column', 0, '-row', row, '-sticky', 'nw')
	rC('grid', base + b, '-column', 0, '-row', row, '-sticky', 'ne')
	#rC('grid', base + c, '-column', 0, '-row', row, '-sticky', 'n')
		# I think it's ok to hide units
	rC('grid', base + scale, '-column', 0, '-row', row+1, '-sticky', 'n')

rC('grid', '.pane.top.gcodel', '-column', 0, '-row', 12, '-sticky', 'n')
rC('grid', '.pane.top.gcodes', '-column', 0, '-row', 13, '-sticky', 'n')

TUNE_SLIDER(0, '.pane.top.feedoverride', '.foscale', '.l', '.foentry', '.m')
TUNE_SLIDER(1, '.pane.top.rapidoverride', '.foscale', '.l', '.foentry', '.m')
TUNE_SLIDER(2, '.pane.top.spinoverride', '.foscale', '.l', '.foentry', '.m')
TUNE_SLIDER(3, '.pane.top.jogspeed', '.s', '.l0', '.l', '.l1')
TUNE_SLIDER(4, '.pane.top.ajogspeed', '.s', '.l0', '.l', '.l1')
TUNE_SLIDER(5, '.pane.top.maxvel', '.s', '.l0', '.l', '.l1')

### DRO
BFc('.pane.top.right.fnumbers.text')

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
		
		self.place(relx=1, rely=1, y=-20, anchor="se")
		frame = Tkinter.Frame(self)
		button = Tkinter.Button(frame, text=message, wraplength=int(1000*SCALE),
			justify="left", compound="left", image=message_icons[iconname],
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
notifications.add("info", 'test test test')

if SCALE >= 1.5:
	# A bit thicker lines
	glEnable(GL_LINE_SMOOTH)
	glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
