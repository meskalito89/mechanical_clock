import tkinter as tk
import tkinter
import string
import random
import datetime
import pdb
import math


class Clock(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title = 'Hurry up!!!'
        self.canvas_width = 300
        self.canvas_height = 300
        self.second_length = self.canvas_width * 0.7
        self.geometry("500x600")
        self.update()
        self.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()
        self.canvas.pack(expand=True, fill="both", side='top')    
        frame2 = tk.Frame(self).pack()
        hour_label = tk.Label(self, text='Hour').pack(frame2, side=tkinter.LEFT)
        frame = tk.Frame(self).pack(side=tkinter.BOTTOM)

        self.my_hour = tk.IntVar(value=0)
        self.hour = tk.Spinbox(self,
                                from_=0,
                                to=11,
                                width=4,
                                increment=1,
                                textvariable=self.my_hour,
                                wrap=True).pack(frame, side=tkinter.LEFT)
        minute_label = tk.Label(self, text='Min').pack(frame2, side=tkinter.LEFT)

        self.my_minute = tk.IntVar(value=0)
        self.minute = tk.Spinbox(self,
                                from_=0,
                                to=59,width=4,
                                increment=1,
                                textvariable=self.my_minute,
                                wrap=True).pack(frame, side=tkinter.LEFT)

        self.current_datetime = datetime.datetime.now()
        self.offset_datetime = 0
        self.time_track = 0
        self.button = tk.Button(self, text="Set time", command=self.set_time).pack(frame, side=tkinter.LEFT)

        self.cx = self.winfo_width()/2
        self.cy = self.winfo_height()/2 - 80
        self.resizable(False, False)
        self.offset_second = 0
        self.offset_hour = 0
        self.offset_minute = 0

    def draw_line(self, length, angle, *args, **kwargs):
        part = angle - math.pi/2
        x2 = self.cx + math.cos(part) * length
        y2 = self.cy + math.sin(part) * length
        self.canvas.create_line(self.cx, self.cy, x2, y2, *args, **kwargs)

    def draw_second(self, second):
        length = self.winfo_width()/2*0.7
        angle = math.pi/30 * second 
        self.draw_line( length , angle)
    
    def draw_minute(self, minutes):
        length = self.winfo_width()/2*0.6
        angle = math.pi/30 * minutes
        self.draw_line(length, angle, width=3)

    def draw_hour(self, hour):
        length = self.winfo_width()/2 * 0.4
        angle = math.pi/6 * hour
        self.draw_line(length, angle, width=4)

    def draw_ticks(self):
        hours = 12
        radius = self.winfo_width()/2 * 0.7
        radius_for_digits = radius * 1.1
        for i in range(60):
            length = 8
            widht = 1

            x1 = self.cx + math.sin(math.pi/30*i + math.pi)*(radius - length)
            y1 = self.cy + math.cos(math.pi/30*i + math.pi)*(radius - length)
            x2 = self.cx + math.sin(math.pi/30*i + math.pi)*radius
            y2 = self.cy + math.cos(math.pi/30*i + math.pi)*radius
            x3 = self.cx + math.sin(math.pi/30*i + math.pi)*radius_for_digits
            y3 = self.cy + math.cos(math.pi/30*i + math.pi)*radius_for_digits

            if i % 5 == 0:
                length = 20
                width = 4
                self.canvas.create_text(x3, y3, text=str(hours))
                hours -=1


            self.canvas.create_line(x1, y1, x2, y2, width=width)

    def get_time(self):
        now = datetime.datetime.now()
        hour = now.hour - self.offset_hour
        minute = now.minute - self.offset_minute
        second = now.second
        try:
            date = datetime.time(hour=hour, minute=minute, second=second)
        except ValueError:
            hour = now.hour
            minute = now.minute
        return datetime.time(hour=hour, minute=minute, second=second)

    def set_time(self):
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute

        try:
            set_hour=self.my_hour.get()
            set_minute=self.my_minute.get()
        except tk.TclError:
            self.offset_hour = 0
            self.offset_minute = 0
            return

        self.offset_hour = hour - set_hour
        self.offset_minute = minute - set_minute

    def update_per_sec(self):

        self.canvas.delete('all')
        date = self.get_time()
        hour = date.hour
        minute = date.minute
        second = date.second

        self.draw_second(second)
        self.draw_minute(minute)
        self.draw_hour(hour)
        self.draw_ticks()
        self.after(1000, self.update_per_sec)


b = Clock()
b.update_per_sec()
b.mainloop()