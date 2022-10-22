import tkinter as tk
import string
import random
import datetime
import pdb
import math


class Clock(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.canvas_width = 300
        self.canvas_height = 300
        self.second_length = self.canvas_width * 0.7
        self.geometry("500x500")
        self.update()
        self.columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack(expand=True, fill="both")    
        self.current_datetime = datetime.datetime.now()
        self.time_track = 0
        tk.Button(self, text="Set time", command=lambda: TestCode(self)).pack()
        self.cx = self.winfo_width()/2
        self.cy = self.winfo_height()/2
        self.resizable(False, False)
        self.offset_second = 0
        self.offset_minute = 0
        self.offset_hour = 0

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
        hour = now.hour + self.offset_hour
        minute = now.minute + self.offset_minute
        second = now.second + self.offset_second
        return datetime.time(hour=hour, minute=minute, second=second)

    def set_hour(self, hour):
        if hour > 0 and hour < 12:
            self.offset_hour = hour
    
    def set_minute(self, minute):
        if minute > 0 and minute < 60:
            self.offset_minute = minute

    def set_time(self):
        pass

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