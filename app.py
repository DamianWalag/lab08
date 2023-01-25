import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import Slider

from scipy.integrate import odeint
from functools import partial


B = 0.8
G = 0.2
S0 = 0.99
I0 = 0.01
R0 = 0

def func(y, t, B=0.8, G=0.2):
    S, I, R = y
    return -B * S * I, B * S * I - G * I, G * I
# zrobilem wszystko w jednym callbacku
def callback(attr, old, new):
    B_new = s1.value
    G_new = s2.value
    ts = np.linspace(0, s3.value, 1000)
    res = odeint(func, (S0,I0,R0), ts, args = (B_new, G_new))
    
    a.data_source.data = {'x': ts, 
                        'y': res[:,0]}
    b.data_source.data = {'x': ts, 
                        'y': res[:,1]}
    c.data_source.data = {'x': ts, 
                        'y': res[:,2]}
    


ts = np.linspace(0, 50, 1000)
res = odeint(func, (S0,I0,R0), ts)



fig = figure(x_axis_label = 't',
             y_axis_label = 'Fraction of population',
             width = 500,
             aspect_ratio = 1)
fig.toolbar.logo = None
fig.toolbar.autohide = True
fig.grid.grid_line_dash = (5, 5)
a = fig.line(ts, res[:,0], color = 'blue', line_width = 3, legend_label = 'Susceptible')
b = fig.line(ts, res[:,1], color = 'red', line_width = 3, legend_label = 'Infected')
c = fig.line(ts, res[:,2], color = 'green', line_width = 3, legend_label = 'Recovered')
s1 = Slider(start = 0, end = 1, step = 0.01, value = 0.8, title = 'beta', sizing_mode = 'stretch_width')
s2 = Slider(start = 0, end = 1, step = 0.01, value = 0.1, title = 'gamma', sizing_mode = 'stretch_width')
s3 = Slider(start = 1, end = 500, step = 1, value = 50, title = 'time', sizing_mode = 'stretch_width')
# w sumie opcja 'value' i ciągła zmiana wykresu mi sie podoba
s1.on_change('value', callback)
s2.on_change('value', callback)
s3.on_change('value', callback)


curdoc().add_root(row(column(s1, s2, s3, width = 200), fig))
print(fig.x_range)

#poetry run bokeh serve --show app.py