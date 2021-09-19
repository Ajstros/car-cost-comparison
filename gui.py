"""GUI for the car comparison.

All cars are set up here with make, model, and initial price. The user's state
is also set up here which determines fuel costs. Once this is all entered,
there is a button to graph the data which will close the GUI and switch to a
matplotlib graph window.
"""

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from pandas.core import frame
from car import Car
from fuel_data import get_electricity_by_state, get_gas_by_state


frm_car_entry_list = []
clicked_make_list = []
clicked_model_list = []
ent_initial_price_list = []

def create_car_entry():
    """Set up the widgets for car entry.
    
    Make - dropdown menu
    Model - dropdown menu
    Initial Price - Entry
    """

    global create_car_entry_row
    current_index = create_car_entry_row - 2
    frm_car_entry_list.append(tk.Frame(master=window, relief=tk.GROOVE, borderwidth=3))
    clicked_make_list.append(tk.StringVar())
    clicked_model_list.append(tk.StringVar())

    make_model_dict = Car.get_make_model_dict()

    sorted_makes = list(make_model_dict.keys())
    sorted_makes.sort()

    drop_make = tk.OptionMenu(frm_car_entry_list[current_index], clicked_make_list[current_index], *sorted_makes)
    drop_model = tk.OptionMenu(frm_car_entry_list[current_index], clicked_model_list[current_index], *make_model_dict[sorted_makes[0]])

    def update_models(*args):
        models = make_model_dict[clicked_make_list[current_index].get()]
        clicked_model_list[current_index].set(models[0])
        menu = drop_model['menu']
        menu.delete(0, 'end')
        for model in models:
            menu.add_command(label=model, command=lambda model=model: clicked_model_list[current_index].set(model))

    clicked_make_list[current_index].trace('w', update_models)
    clicked_make_list[current_index].set(list(make_model_dict.keys())[0])

    ent_initial_price_list.append(tk.Entry(master=frm_car_entry_list[current_index]))
    lbl_initial_price = tk.Label(master=frm_car_entry_list[current_index], text='Initial Price')
    ent_initial_price_list[current_index].insert(0, '0')

    drop_make.grid(row=0, column=0, padx=10, sticky='ew')
    drop_model.grid(row=0, column=1, padx=10, sticky='ew')
    lbl_initial_price.grid(row=0, column=2, padx=10, sticky='ew')
    ent_initial_price_list[current_index].grid(row=0, column=3, padx=10, sticky='ew')
    frm_car_entry_list[current_index].grid(row=create_car_entry_row,
                       column=0, padx=10, sticky='ew')
    create_car_entry_row += 1


def graph():
    frm_graph = tk.Frame(master=window)
    fig = Figure(
        figsize = (5, 5),
        dpi = 100
    )
    ax = fig.add_subplot(1, 2, 1)
    ax.spines['left'].set_position(('axes', 0))
    ax.spines['bottom'].set_position(('axes', 0))
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    cars = []

    miles_per_day = int(ent_miles_per_day.get())

    for i in range(len(clicked_make_list)):
        make = clicked_make_list[i].get()
        model = clicked_model_list[i].get()
        initial_price = int(ent_initial_price_list[i].get())
        car = Car.get_car(make=make, model=model)
        car.initial_price = initial_price
        if car is None:
            continue
        else:
            cars.append(car)

    colors = ['b', 'r', 'g', 'c', 'm', 'y']
    color_index = 0
    x = [i for i in range(3651)] # 10 years
    for car in cars:
        color = colors[color_index]
        if car.type == Car.ELECTRIC:
            fuel_cost = get_electricity_by_state(clicked_state.get())
        else:
            fuel_cost = get_gas_by_state(clicked_state.get())

        y = [car.initial_price + (days * miles_per_day * car.mileage * fuel_cost) for days in x]
        ax.plot(x, y, color, label=car.name)
        color_index += 1
        if color_index > len(colors) - 1:
            color_index = 0

    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    canvas = FigureCanvasTkAgg(fig, master=frm_graph)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=10, rowspan=10)
    frm_toolbar = tk.Frame(master=frm_graph)
    toolbar = NavigationToolbar2Tk(canvas, frm_toolbar)
    toolbar.update()
    canvas.get_tk_widget().grid(row=0, column=1, padx=10)
    frm_toolbar.grid(row=11, column=1, padx=10)
    frm_graph.grid(row=0, column=1, padx=10, sticky='ew', rowspan=20)
    


window = tk.Tk()
window.title('Car Comparison')

frm_state_entry = tk.Frame(master=window)
clicked_state = tk.StringVar()
states = [
    'Alabama',
    'Alaska',
    'Arizona',
    'Arkansas',
    'California',
    'Colorado',
    'Connecticut',
    'Delaware',
    'Florida',
    'Georgia',
    'Hawaii',
    'Idaho',
    'Illinois',
    'Indiana',
    'Iowa',
    'Kansas',
    'Kentucky',
    'Louisiana',
    'Maine',
    'Maryland',
    'Massachusetts',
    'Michigan',
    'Minnesota',
    'Mississippi',
    'Missouri',
    'Montana',
    'Nebraska',
    'Nevada',
    'New Hampshire',
    'New Jersey',
    'New Mexico',
    'New York',
    'North Carolina',
    'North Dakota',
    'Ohio',
    'Oklahoma',
    'Oregon',
    'Pennsylvania',
    'Rhode Island',
    'South Carolina',
    'South Dakota',
    'Tennessee',
    'Texas',
    'Utah',
    'Vermont',
    'Virginia',
    'Washington',
    'West Virginia',
    'Wisconsin',
    'Wyoming'
]
clicked_state.set(states[0])
drop_state = tk.OptionMenu(frm_state_entry, clicked_state, *states)
drop_state.grid(row=0, column=0, padx=10, sticky='ew')


btn_create_car_entry = tk.Button(
    frm_state_entry, text='Add Car', command=create_car_entry)
create_car_entry_row = 2
btn_create_car_entry.grid(row=0, column=1, padx=10, sticky='ew')

btn_graph = tk.Button(frm_state_entry, text='Graph', command=graph)
btn_graph.grid(row=0, column=2, padx=10, sticky='ew')

lbl_miles_per_day = tk.Label(master=frm_state_entry, text='Miles per Day (int)')
ent_miles_per_day = tk.Entry(master=frm_state_entry)
ent_miles_per_day.insert(0, '100')
lbl_miles_per_day.grid(row=0, column=3, padx=10, sticky='ew')
ent_miles_per_day.grid(row=0, column=4, padx=10, sticky='ew')

frm_state_entry.grid(row=0, column=0, padx=10, sticky='ew')


window.mainloop()
