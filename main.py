# these are the configs for you to change.

waybar = (24, 0, 0, 0) # waybar size on top, left, right, bottom
bg = "#181524"
font = ("Jetbrains Mono", 20, "bold")

frame_margin_x = lambda w: 96
frame_margin_y = lambda h: (h//2)-96 # example for margin y being half of height minus 64
frame_bg = bg # setting the frame background as the same as the window background

btn_bg = "#221e33"
btn_fg = "#ffffff"
btn_bg_hover = "#322c4a"
btn_fg_hover = btn_fg
btn_border = ("white", "white", 0) # default colour, focused colour, and thickness

# defining each buttons, in order.
btns = [
	{
		"text": "Shut down",
		"width": 192, 
		"height": 192, 
		"x": 0, 
		"y": 0,
		"command": lambda: None
	} # first button. then follows, you get the point.
]

# it kinda goes against my nature to write code with readable variable names, but there's a small chance someone will actually use this program and configure it themselves in the future.
# it also goes against my nature to write THIS MUCH FUCKING COMMENTS.
# below here is the code. don't mess with it unless you know what the fuck you're doing. and if you think you do, you probably don't. If you think you don't, there is a high chance that you do.

import tkinter as tk
import subprocess
import json

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

f = tk.Frame(window, width=w-2*frame_margin_x(w), height=h-2*frame_margin_y(h), bg=frame_bg)
f.place(x=frame_margin_x(w), y=frame_margin_y(h))
tfw = w-2*frame_margin_x(w)
tfh = h-2*frame_margin_y(h)

buttons = []

for btn in btns:
	b1 = tk.Button(f, text=btn["text"], bg=btn_bg, fg=btn_fg,
			activebackground=btn_bg_hover, activeforeground=btn_fg_hover,
			font=font, relief="flat", cursor="hand2",
			highlightbackground=btn_border[0], highlightcolor=btn_border[1],
			highlightthickness=btn_border[2], command=btn["command"])
	b1.place(width=btn["width"], height=btn["height"], x=btn["x"], y=btn["y"])
	b1.bind("<Enter>", lambda e: b1.config(fg=btn_fg_hover, bg=btn_bg_hover))
	b1.bind("<Leave>", lambda e: b1.config(fg=btn_fg, bg=btn_bg))
	buttons.append(b1)

window.mainloop()

