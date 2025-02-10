# CREDIT: @naderi_yeganeh for the circles equations
# https://www.scientificamerican.com/blog/guest-blog/making-mathematical-art/

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import Slider
from bokeh.plotting import figure
from bokeh.io import export_svg
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import numpy as np

x = []
y = []
r = []

# Créer la figure
plot = figure(width=1200, height=1200, title="Cercles dynamiques", output_backend="svg", background_fill_color=None, border_fill_color=None)

# Créer une liste pour stocker les GlyphRenderers
circles = []

# Fonction pour générer les cercles
def update_circles(attr, old, new):
    # Récupérer la nouvelle valeur de N
    k_max = slider.value

    # Supprimer les cercles existants
    for circle in circles:
        plot.renderers.remove(circle)

    x.clear()
    y.clear()
    r.clear()

    # Créer de nouvelles positions et tailles pour les cercles
    for k in range(1, k_max+1):
        x.append(np.cos(10*np.pi*k/k_max)*(1-np.square((np.cos(16*np.pi*k/k_max)))/2))
        y.append(np.sin(10*np.pi*k/k_max)*(1-np.square((np.cos(16*np.pi*k/k_max)))/2))
        r.append(0.005 + 0.1*np.power(np.sin(52*np.pi*k/k_max), slider2.value))

    # Ajouter les nouveaux cercles au plot et stocker les GlyphRenderers
    new_circles = plot.circle(x, y, radius=r, color="blue", alpha=0.6, fill_color=None, line_width=0.5)
    
    # Circles est maintenant une liste des GlyphRenderers des cercles ajoutés
    circles.clear()  # Vider la liste
    circles.append(new_circles)  # Ajouter les nouveaux cercles

# Créer le slider pour changer la valeur de k_max
slider = Slider(start=1, end=14000, value=1000, step=1000, title="Nombre de cercles")

# Créer le slider pour changer la valeur de la puissance
slider2 = Slider(start=1, end=6, value=4, step=1, title="Puissance")

# Lier le slider à la fonction qui met à jour les cercles
slider.on_change('value', update_circles)
slider2.on_change('value', update_circles)

# Ajouter le slider et le graphique à l'interface
layout = column(slider, slider2, plot)

# Exécuter la fonction initiale pour afficher les cercles au début
update_circles(None, None, slider.value)

# Ajouter le layout au document Bokeh
curdoc().add_root(layout)

export_svg(plot, filename="plot.svg")