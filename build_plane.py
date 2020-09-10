from tkinter import *

NUMBER_OF_POINTS = 3
DECIMAL_ERROR_TOLERANCE = 0.000001
ROUND_TO = 5
BACKGROUND = "#373832"
BUTTON = "#C1C4B3"
TEXT_AGAINST_BACKGROUND = 'white'
BUTTON_TEXT_COLOR = 'black'
ENTRY_FOREGROUND = 'black'
ENTRY_BACKGROUND = 'white'
# TEXT_INPUT = 

class Vector(object):
    def __init__(self,x=0,y=0,z=0, marked=False):
        self.marked = marked
        if x % 1 <= DECIMAL_ERROR_TOLERANCE:
            self.x = int(x)
        else:
            self.x = x

        if y % 1 <= DECIMAL_ERROR_TOLERANCE:
            self.y = int(y)
        else:
            self.y = y

        if z % 1 <= DECIMAL_ERROR_TOLERANCE:
            self.z = int(z)
        else:
            self.z = z

    def sub(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def to(self, other):
        return self.sub(other)
    
    def cross(self, other):
        return Vector(((self.y*other.z)-(other.y*self.z)),((self.x*other.z)-(other.x*self.z))*-1,((self.x*other.y)-(other.x*self.y)))

    def __str__(self):
        return '<{0}, {1}, {2}>'.format(self.x, self.y, self.z)
    
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __ne__(self, other):
        return not self.__eq__(other)

def can_be_int(number):
    return number % 1 <= DECIMAL_ERROR_TOLERANCE

def negative_format(number):
    build = (' - ' if number > 0 else " + ")
    if number % 1 <= DECIMAL_ERROR_TOLERANCE:
        return build + str(int(abs(number)))
    return build + str(round(abs(number), ROUND_TO))

def get_variable_portion(var, number):
    if number != 0:
        return "({0}{1})".format(var, negative_format(number))

def get_cof_portion(cof, first):
    build = ""
    build += ("" if first else " + ") if (cof > 0) else ('-' if first else " - ")
    if abs(cof) != 1:
        if cof % 1 <= DECIMAL_ERROR_TOLERANCE:
            return build + str(int(abs(cof)))
        return build + str(round(abs(cof), ROUND_TO))
    return build

def get_full_portion(cof, var, number, first):
    if cof == 0:
        return ""
    return get_cof_portion(cof, first) + get_variable_portion(var, number)

def get_full_equation(cofs, point):
    build = "0" if cofs.x == 0 and cofs.y == 0 and cofs.z == 0 else ""
    build += get_full_portion(cofs.x, 'x', point.x, True)
    build += (get_full_portion(cofs.y, 'y', point.y, cofs.x == 0))
    build += (get_full_portion(cofs.z, 'z', point.z, cofs.x == 0 and cofs.y == 0) + " = 0")
    return build

def get_plane_data(pts):
    if len(pts) != 3:
        raise Exception("3 point were not input. Cannot form plane...")
    vector1 = pts[1].to(pts[0])
    vector2 = pts[2].to(pts[0])
    build = "PQ = " + str(vector1) + "\n"
    build += "PR = " + str(vector2) + "\n"
    return build + "Cross Product (PQ x PR) = " + str(vector1.cross(vector2))

def get_plane(pts):
    if len(pts) != 3:
        raise Exception("3 point were not input. Cannot form plane...")
    vector1 = pts[1].to(pts[0])
    vector2 = pts[2].to(pts[0])
    return get_full_equation(vector1.cross(vector2), pts[0])

def has_number(input_string):
    return any(char.isdigit() for char in input_string)

def make_vector(some_input):
    if not(has_number(some_input)):
        return Vector(0, 0, 0, True)
    pts = list(map(str.strip, some_input.replace('(','').replace(')','').split(',' if ',' in some_input else ' ')))
    for n in range(len(pts), NUMBER_OF_POINTS):
        pts.append(0)
    return Vector(float(pts[0]), float(pts[1]), float(pts[2]))

frame = Tk()
frame.config(background=BACKGROUND)
frame.title('Plane Calculator From 3 Points')

labels = []
stringvars = []
entries = []
point_names = ["P", "Q", "R"]
for i in range(NUMBER_OF_POINTS):
    current = "Point " + str(i + 1) + " ({})".format(point_names[i])
    labels.append(Label(frame, text=current))
    labels[i].config(font=("Courier New", 15), foreground=TEXT_AGAINST_BACKGROUND, background=BACKGROUND)
    labels[i].grid(row=i, column=0, padx=(5, 10), pady=10)
    
    stringvars.append(StringVar())
    entries.append(Entry(frame, textvariable=stringvars[i], width=15))
    entries[i].config(font=("Courier New", 15), foreground=ENTRY_FOREGROUND, background=ENTRY_BACKGROUND)
    entries[i].grid(row=i, column=1, padx=(0, 10), pady=10)

plane_data = Label(frame, text="Enter 3 Valid Points", height=5)
plane_data.config(font=("Courier New", 12), foreground=TEXT_AGAINST_BACKGROUND, background=BACKGROUND)
plane_data.grid(row=3, column=0, rowspan=2, columnspan=3, pady=(50, 0))

plane_equation = Label(frame, text="click 'create plane'\nafter you enter data".title(), height=5)
plane_equation.config(font=("courier New", 20, 'bold'), foreground=TEXT_AGAINST_BACKGROUND, background=BACKGROUND)
plane_equation.grid(row=5, column=0, columnspan=3, rowspan=4)

def submit():
    try:
        vector_list = []
        should_raise = False
        for i in range(NUMBER_OF_POINTS):
            vector_list.append(make_vector(stringvars[i].get()))
            stringvars[i].set(str(vector_list[i]).replace('<', '(').replace('>', ")"))
            if not(should_raise) and vector_list[i].marked:
                should_raise = True
        plane_data['text'] = get_plane_data(vector_list)
        plane_equation['text'] = get_plane(vector_list)
        if should_raise:
            raise Exception("u fool")
    except:
        plane_data['text'] = "Something went wrong...\nTry seperating your values\n with commas or spaces"

submit_button = Button(frame, text="Create Plane", command=submit, width=30, height=6)
submit_button.config(font=("Courier New", 12), foreground=BUTTON_TEXT_COLOR, background=BUTTON)
submit_button.grid(row=0, column=2, rowspan=3, padx=(0, 10), pady=10)

def clear():
    plane_data['text'] = "Enter 3 Valid Points"
    plane_equation['text'] = "click 'create plane'\nafter you enter data".title()
    for i in stringvars:
        i.set("")

clear_button = Button(frame, text="Clear", command=clear, width=80, height=2)
clear_button.config(font=("Courier New", 10), foreground=BUTTON_TEXT_COLOR, background=BUTTON)
clear_button.grid(row=10, column=0, rowspan=2, columnspan=3, padx=5, pady=(0, 5))

exit_button = Button(frame, text="Quit", command=frame.destroy, width=80, height=2)
exit_button.config(font=("Courier New", 10, 'bold', 'italic'), foreground='red', background=BUTTON)
exit_button.grid(row=12, column=0, columnspan=3, padx=5, pady=(0, 5))

frame.mainloop()