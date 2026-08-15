#!/usr/bin/python
import os, sys # don't mess with this line. this is used in the config.
# these are the configs for you to change.

waybar = (28, 0, 0, 0) # waybar size on top, left, right, bottom
fg = "#FFFFFF"
bg = "#181524"

font = ("Jetbrains Mono", 20, "bold")
font_large = ("Jetbrains Mono", 48, "bold")
font_small = ("Jetbrains Mono", 12, "bold")

text_config = [
	(font_large, "{DAYOFWEEK}"),
	(font, "{DAY} {MONTH} {YEAR}"),
	(font_small, "- {HOUR24}:{MINUTE} -")
]
text_margin_y = 128

frame_margin_x_left = lambda w: 96
frame_margin_x_right = lambda w: 96

frame_margin_y_top = lambda h: (h//2)-96 # example for margin y being half of height, minus 96
frame_margin_y_bottom = lambda h: 64
frame_bg = bg # setting the frame background as the same as the window background

btn_bg = "#221e33"
btn_fg = "#ffffff"
btn_bg_hover = "#322c4a"
btn_fg_hover = btn_fg
btn_border = ("white", "white", 0) # default colour, focused colour, and thickness

# defining each buttons, in order.
btns = [
	{
		"font": font,
		"text": "Shut down",
		"width": 192, 
		"height": 192, 
		"x": lambda w: w//2-304, 
		"y": lambda h: 0,
		"command": lambda: os.system("shutdown -h 0")
	}, # first button. then follows, you get the point.
	{
		"font": font,
		"text": "Restart",
		"width": 192, 
		"height": 192,
		"x": lambda w: w//2-96, 
		"y": lambda h: 0,
		"command": lambda: os.system("reboot")
	},
	{
		"font": font,
		"text": "Return to\nHyprland",
		"width": 192, 
		"height": 192,
		"x": lambda w: w//2+112,
		"y": lambda h: 0,
		"command": lambda: sys.exit(0)
	}

]

# it kinda goes against my nature to write code with readable variable names, but there's a small chance someone will actually use this program and configure it themselves in the future.
# it also goes against my nature to write THIS MUCH FUCKING COMMENTS.
# below here is the code. don't mess with it unless you know what the fuck you're doing. and if you think you do, you probably don't. If you think you don't, there is a high chance that you do.

import tkinter as tk
import subprocess
import json
import datetime

monitors = json.loads(subprocess.getoutput("hyprctl -j monitors"))
w, h, x, y = 0, 0, 0, 0
r = 0
for i in monitors:
	if i["focused"] == True:
		w = i["width"]
		h = i["height"]
		#x = i["x"]
		#y = i["y"]
		r = i["refreshRate"]
		break

t = 1000 // r

window = tk.Tk(className="hyprland_widget")
window.overrideredirect(True)
window.geometry(f"{w-waybar[1]-waybar[2]}x{h-waybar[0]-waybar[3]}+{x+waybar[1]}+{y+waybar[0]}")

window.config(bg=bg)
window.bind("<Escape>", lambda event: window.destroy())

tfw = w-frame_margin_x_left(w)-frame_margin_x_right(w)
tfh = h-frame_margin_y_top(h)-frame_margin_y_bottom(h)

f2 = tk.Frame(window, width=tfw, height=frame_margin_y_top(h)-text_margin_y, bg=bg)
f2.place(relx=0.5, y=text_margin_y, anchor="n")
txts = []

time = datetime.datetime.now()
dow = time.strftime("%A")
h12 = time.strftime("%I")
h24 = time.strftime("%H")
ampm = time.strftime("%p")
minute = time.strftime("%M")
second = time.strftime("%S")
year = time.strftime("%Y")
day = time.strftime("%d")
month = time.strftime("%B")

for text in text_config:
	t = text[1].replace("{DAYOFWEEK}", dow)
	t = t.replace("{DAY}", day)
	t = t.replace("{MONTH}", month)
	t = t.replace("{YEAR}", year)
	t = t.replace("{HOUR24}", h24)
	t = t.replace("{MINUTE}", minute)
	t = t.replace("{HOUR12}", h12)
	t = t.replace("{AMPM}", ampm)
	t = t.replace("{SECOND}", second)

	t1 = tk.Label(f2, text=t, bg=bg, fg=fg, font=text[0])
	t1.pack()
	txts.append(t1)

f = tk.Frame(window, width=tfw, height=tfh, bg=frame_bg)
f.place(relx=0.5, y=frame_margin_y_top(h), anchor="n")

buttons = []

for btn in btns:
	b1 = tk.Button(f, text=btn["text"], bg=btn_bg, fg=btn_fg,
			activebackground=btn_bg_hover, activeforeground=btn_fg_hover,
			font=btn["font"], relief="flat", cursor="hand2",
			highlightbackground=btn_border[0], highlightcolor=btn_border[1],
			highlightthickness=btn_border[2], command=btn["command"])

	b1.place(width=btn["width"], height=btn["height"], x=btn["x"](tfw), y=btn["y"](tfh))
	buttons.append(b1)
	b1.bind("<Enter>", lambda e, b=b1: b.config(fg=btn_fg_hover, bg=btn_bg_hover))
	b1.bind("<Leave>", lambda e, b=b1: b.config(fg=btn_fg, bg=btn_bg))

def main():
	time = datetime.datetime.now()
	dow = time.strftime("%A")
	h12 = time.strftime("%I")
	h24 = time.strftime("%H")
	ampm = time.strftime("%p")
	minute = time.strftime("%M")
	year = time.strftime("%Y")
	day = time.strftime("%d")
	month = time.strftime("%B")
	second = time.strftime("%S")

	i = 0
	for text in text_config:
		t = text[1].replace("{DAYOFWEEK}", dow)
		t = t.replace("{DAY}", day)
		t = t.replace("{MONTH}", month)
		t = t.replace("{YEAR}", year)
		t = t.replace("{HOUR24}", h24)
		t = t.replace("{MINUTE}", minute)
		t = t.replace("{HOUR12}", h12)
		t = t.replace("{AMPM}", ampm)
		t = t.replace("{SECOND}", second)

		txts[i].configure(text=t)
		i += 1

	window.after(100, main)

window.after(100, main)

window.mainloop()
