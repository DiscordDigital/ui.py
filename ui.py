import curses
import collections
import sys
import os
from time import sleep

# File syntax
#
# When there's not enough space for all elements UI will go into scroll mode
#
# Syntax:
# script.py ui_example.txt
#
# an object is one line, split by ;
# The first part is the Name the second part is the shell action
# Use the sample file to tweak colors.
# Valid colors are: black, red, green, yellow, blue, magenta, cyan, white
# Also valid colors are black2, red2, green2.. those are usually brighter versions
#
# To run an inbuilt function just use an action as followed:
# Show version;function:Show_version
#
# To implement a quit button you can do so:
# Quit menu;quit
#
# For more information check out the github readme: https://github.com/DiscordDigital/ui.py/

def RunInbuiltFunction(function_name):
    if (function_name == "Show_version"):
        print("Running python version " + sys.version)

def generate_sample_file():
    sample_file = open('sample_ui.txt','w')
    sample_file.write(
        """menutext=Sample UI!\nmaxh=3\ntitlecolor=white\nwindow_bg=blue\nobjcolor_text=white\nobjcolor_bg=blue\nobjcolor_sel_text=black\nobjcolor_sel_bg=white\nStart Nano;nano\nShow date;date\nCredits;echo Made by discord.digital\nShow Python version;function:Show_version\nQuit;quit"""
    )
    sample_file.close()

if len(sys.argv) != 2:
    print("Specify ui file")
    print("Get started by typing: " + sys.argv[0] + " sample")
    exit()
elif (sys.argv[1] == "sample"):
    generate_sample_file()
    print("Created sample_ui.txt")
    print("Use it like that: " + sys.argv[0] + " sample_ui.txt")
    exit(0)
else:
    if not os.path.isfile(sys.argv[1]):
        print("File not found!")
        exit()

screen = curses.initscr()
curses.curs_set(0)
curses.noecho()
screen.keypad(1)
curses.start_color()
curses.mousemask(1)

def convert_text_to_color(text):
    textup = text.upper()
    if (textup == "BLACK"):
        return 0
    if (textup == "RED"):
        return 1
    if (textup == "GREEN"):
        return 2
    if (textup == "YELLOW"):
        return 3
    if (textup == "BLUE"):
        return 4
    if (textup == "MAGENTA"):
        return 5
    if (textup == "CYAN"):
        return 6
    if (textup == "WHITE"):
        return 7
    if (textup == "BLACK2"):
        return 8
    if (textup == "RED2"):
        return 9
    if (textup == "GREEN2"):
        return 10
    if (textup == "YELLOW2"):
        return 11
    if (textup == "BLUE2"):
        return 12
    if (textup == "MAGENTA2"):
        return 13
    if (textup == "CYAN2"):
        return 14
    if (textup == "WHITE2"):
        return 15
    
    return 7

objects = collections.defaultdict(dict)
object_i = 0
menutext = "Menu"
maxh = 3
titlecolor = "white"
window_bg = "black"
objcolor_text = "white"
objcolor_bg = "black"
objcolor_sel_text = "black"
objcolor_sel_bg = "white"

fp = open(sys.argv[1])
for _, line in enumerate(fp):
    if line.startswith("menutext="):
        menutext = line.replace('menutext=','').replace('\n','')
    elif line.startswith("maxh="):
        maxh = line.replace('maxh=','').replace('\n','')
    elif line.startswith("titlecolor="):
        titlecolor = line.replace('titlecolor=','').replace('\n','')
    elif line.startswith("window_bg="):
        window_bg = line.replace('window_bg=','').replace('\n','')
    elif line.startswith("objcolor_text="):
        objcolor_text = line.replace('objcolor_text=','').replace('\n','')
    elif line.startswith("objcolor_bg="):
        objcolor_bg = line.replace('objcolor_bg=','').replace('\n','')
    elif line.startswith("objcolor_sel_text="):
        objcolor_sel_text = line.replace('objcolor_sel_text=','').replace('\n','')
    elif line.startswith("objcolor_sel_bg="):
        objcolor_sel_bg = line.replace('objcolor_sel_bg=','').replace('\n','')
    else:
        if (line == '\n'):
            break
        interface = line.split(';')
        objects[object_i]['Label'] = interface[0].replace('\n','')
        objects[object_i]['Action'] = interface[1].replace('\n','')
        object_i = object_i + 1
fp.close()

colorcode = convert_text_to_color(titlecolor)
colorcode_bg = convert_text_to_color(window_bg)
curses.init_pair(2, colorcode, colorcode_bg)
colorcode_text = convert_text_to_color(objcolor_text)
colorcode_bg = convert_text_to_color(objcolor_bg)
curses.init_pair(3, colorcode_text, colorcode_bg)
colorcode_text = convert_text_to_color(objcolor_sel_text)
colorcode_bg = convert_text_to_color(objcolor_sel_bg)
curses.init_pair(4, colorcode_text, colorcode_bg)

maxh = int(maxh)

screen.bkgd(' ', curses.color_pair(2))

_, x = screen.getmaxyx()
titlepad = curses.newpad(1, x-2)
titlepad.addstr(menutext, curses.color_pair(2))
titlepad.bkgd(' ', curses.color_pair(2) | curses.A_BOLD)

infopad = curses.newpad(3, 15)
infopad.addstr("Press q to exit", curses.color_pair(2))

def create_entry(text,startheight):
    _, x = screen.getmaxyx()
    pad = curses.newpad(maxh, x - 2)
    cheight = int(maxh / 2)
    tstart = int((x / 2) - (len(text) / 2))-1
    pad.addstr(cheight,tstart,text)
    pad.bkgd(' ', curses.color_pair(3))
    return pad

def select_entry(pad):
    global parseoffset
    global select
    global refreshlist
    global selectedpad
    global scrolldirection
    global object_i
    global maxfitobj
    global resize
    if (object_i > maxfitobj) or (parseoffset != 0):
        selectpad.erase()
        selectpad.resize(3,len(str(100) + "/") + len(str(object_i)))
        selectpad.addstr(str(select + 1) + "/" + str(object_i), curses.color_pair(2))
        selectpad.refresh(0, 0, 1, 2, 1, x-2)
    if (pad):
        if (selectedpad != None) and not (resize):
            deselect_entry(selectedpad)
        pad['pad'].bkgd(' ', curses.color_pair(4))
        cheight = int(maxh / 2)
        tstart = int((x / 2) - (len(pad['label']) / 2))-1
        pad['pad'].addstr(cheight,tstart,pad['label'])
        y, _ = pad['pad'].getbegyx()
        sy, sx = screen.getmaxyx()
        pad['pad'].refresh(0,0,y,1,sy,sx-2)
        selectedpad = pad
    else:
        scrolldirection = "up"
        parseoffset = parseoffset - 1
        refreshlist = True
        screen.refresh()    

def deselect_entry(pad):
    pad['pad'].bkgd(' ', curses.color_pair(3))
    cheight = int(maxh / 2)
    tstart = int((x / 2) - (len(pad['label']) / 2))-1
    pad['pad'].addstr(cheight,tstart,pad['label'])
    y, _ = pad['pad'].getbegyx()
    sy, sx = screen.getmaxyx()
    pad['pad'].refresh(0,0,y,1,sy,sx-2)
    screen.refresh()

curseLoop = True
pads = False
action = False
select = 0
selectedpad = None
scroll = False
parseoffset = 0
refreshlist = False
scrolldirection = "down"

seltext = "Selecting 0/0"
selectpad = curses.newpad(3, len(seltext))
selectpad.bkgd(' ', curses.color_pair(3))

y, x = screen.getmaxyx()
screensize = y - 4
maxfitobj = int(screensize / maxh)

while curseLoop:
    screen.refresh()
    resize = curses.is_term_resized(y, x)
    if resize is True:
        y, x = screen.getmaxyx()
        screen.clear()
        curses.resizeterm(y, x)
        screensize = y - 4
        maxfitobj = int(screensize / maxh)
        pads = False
        screen.refresh()
    else:
        try:
            titlepad.refresh(0, 0, 2, int((x/2)-(len(menutext)/2)), 2, x-2)
            infopad.refresh(0, 0, 1, x-17, 1, x-2)
        except:
            pass

    j = 4
    
    if (pads == False) or (refreshlist):
        pads = collections.defaultdict(dict)

        if (object_i > maxfitobj):
            parserange = range(0 + parseoffset, maxfitobj + parseoffset)
        else:
            parserange = range(object_i)
        
        for i in parserange:
            pads[i]['pad'] = create_entry(objects[i]['Label'],j)
            try:
                pads[i]['pad'].refresh(0,0,j,1,y,x-2)
            except:
                pass
            pads[i]['action'] = objects[i]['Action']
            pads[i]['label'] = objects[i]['Label']
            pads[i]['range-start'] = j
            pads[i]['range-end'] = j + maxh
            j = j + maxh
        if (refreshlist):
            if (scrolldirection == "down"):
                select = maxfitobj + parseoffset - 1
                select_entry(pads[select])
            if (scrolldirection == "up"):
                select = parseoffset
                select_entry(pads[select])
        else:
            select = 0
            select_entry(pads[select])
        refreshlist = False

    event = screen.getch()
    if event == ord("q"): break
    if event == curses.KEY_MOUSE:
        try:
            _, _, my, _, _ = curses.getmouse()
            if (object_i > maxfitobj):
                parserange = range(0 + parseoffset, maxfitobj + parseoffset)
            else:
                parserange = range(object_i)
            for i in parserange:
                if (my >= pads[i]['range-start']) and (my < pads[i]['range-end']):
                    if (selectedpad != None):
                        deselect_entry(selectedpad)
                    select_entry(pads[i])
                    action = pads[i]['action']
                    y, _ = pads[i]['pad'].getbegyx()
                    sy, sx = screen.getmaxyx()
                    pads[i]['pad'].refresh(0,0,y,1,sy,sx-2)
                    sleep(0.2)
                    curseLoop = False
        except:
            pass
    if event == curses.KEY_UP:
        if (selectedpad == None):
            select = 0
            select_entry(pads[select])
        if (select != 0):
            select = select - 1
            select_entry(pads[select])

    if event == curses.KEY_DOWN:
        if (selectedpad != None):
            if (select != maxfitobj + parseoffset - 1):
                if not (select == object_i - 1):
                    select = select + 1
                    deselect_entry(selectedpad)
                    select_entry(pads[select])
            else:
                if (select == maxfitobj + parseoffset - 1):
                    if (select != object_i - 1):
                        select = select + 1
                        parseoffset = parseoffset + 1
                        scrolldirection = "down"
                        refreshlist = True
        else:
            if (object_i == 1):
                select = 0
                select_entry(pads[select])
            else:
                select = 1
                select_entry(pads[select])
    if event == 10:
        if (selectedpad != None):
            action = objects[select]['Action']
            curseLoop = False
curses.endwin()
sleep(0.1)
if (action):
    if action.startswith("function:"):
        function = action.split(":")[1]
        RunInbuiltFunction(function)
    elif (action == "quit"):
        exit()
    else:
        os.system(action)
