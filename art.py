import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from bokeh.models import Div, RangeSlider, Spinner

k_max = 3000

x = []
y = []
r = []


color1 = "#3366ff"
color2 = "#009900"

def hex_to_RGB(hex_str):
    """ #FFFFFF -> [255,255,255]"""
    #Pass 16 to the integer function for change of base
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def get_color_gradient(c1, c2, n):
    """
    Given two hex colors, returns a color gradient
    with n colors.
    """
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]


for k in range(0, k_max):
    x.append(np.cos(10*np.pi*k/k_max)*(1-0.5*np.square((np.cos(16*np.pi*k/k_max)))))
    y.append(np.sin(10*np.pi*k/k_max)*(1-0.5*np.square((np.cos(16*np.pi*k/k_max)))))
    r.append(1/200 + 0.1*np.sin(52*np.pi*k/k_max))
    

fig, ax = plt.subplots()
plt.rc('text', usetex = True)
plt.rc('font', family = 'serif')
plt.plot(x, y, marker = '.', color = 'k', linestyle = 'None')

for k in range(k_max):
    circle1 = plt.Circle((x[k], y[k]), r[k], color = get_color_gradient(color1, color2, k_max)[k], fill=False)
    ax.add_artist(circle1)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    
plt.show()

div = Div(
    text="""
        <p>Select the circle's size using this control element:</p>
        """,
    width=200,
    height=30,
)

range_slider = RangeSlider(
    title="Adjust x-axis range", # a title to display above the slider
    start=0,  # set the minimum value for the slider
    end=1000,  # set the maximum value for the slider
    step=100,  # increments for the slider
    value=k_max,  # initial values for slider
)

range_slider.js_link("value", k_max)