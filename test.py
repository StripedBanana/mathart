# CREDIT: @naderi_yeganeh for the circles equations
# https://www.scientificamerican.com/blog/guest-blog/making-mathematical-art/

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import Slider, Select, ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import export_svg
from bokeh.palettes import all_palettes
from scipy.interpolate import interp1d

from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import numpy as np

x = []
y = []
r = []

# Créer les figures
plot = figure(width=1200, height=1200, title="Cercles dynamiques", output_backend="svg", background_fill_color=None, border_fill_color=None)
plot.xgrid.grid_line_color = None
plot.ygrid.grid_line_color = None
plot.axis.axis_line_color = None

p_palette = figure(
    title="Palette avant interpolation",
    width=800, height=100, x_range=(0, 256),
    toolbar_location=None, tools=""
)

def hex_to_rgb(hex_color):
    """Convertit une couleur hexadécimale en RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    """Convertit une couleur RGB en hexadécimal."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

def generate_sampled_rgb_colors(N):
    """Génère N couleurs échantillonnées uniformément dans l'espace RGB."""
    # Calcul des dimensions de l'échantillon : la racine cubique pour échantillonner l'espace 3D
    num_colors_per_channel = int(round(N ** (1/3)))  # Racine cubique pour répartir dans 3 dimensions
    step = 256 // num_colors_per_channel  # Intervalle pour l'échantillonnage

    colors = []
    for r in range(0, 256, step):
        for g in range(0, 256, step):
            for b in range(0, 256, step):
                colors.append(rgb_to_hex((r, g, b)))
                
    # Si l'on génère plus de couleurs que N, on réduit la liste
    return colors[:N]

def generate_gradient(start_color, end_color, n):
    """
    Génère un gradient de n couleurs entre start_color et end_color.
    start_color et end_color doivent être au format hexadécimal.
    """
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    
    # Création du gradient
    gradient = []
    for i in range(n):
        interpolated_rgb = (
            int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / (n - 1)),
            int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / (n - 1)),
            int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / (n - 1))
        )
        gradient.append(rgb_to_hex(interpolated_rgb))
    
    return gradient

# Exemple d'utilisation
start_color = "#FF0000"  # Rouge
end_color = "#0000FF"    # Bleu




# Créer une liste pour stocker les GlyphRenderers
circles = []
palettes_viz = []

# Fonction pour générer les cercles
def update_circles(attr, old, new):
    # Récupérer la nouvelle valeur de N
    k_max = slider.value

    # Supprimer les plot existants
    for palette_viz in palettes_viz:
        p_palette.renderers.remove(palette_viz)
    for circle in circles:
        plot.renderers.remove(circle)

    x.clear()
    y.clear()
    r.clear()

    # Obtenir la palette avec le maximum de couleurs disponibles
    max_palette_size = max(all_palettes[palette_select.value].keys())
    palette = all_palettes[palette_select.value][max_palette_size]

    
    
    # Étendre la palette : concaténer N fois avec une version inversée
    palette_extended = palette + palette[::-1]
    for i in range(1, slider3.value):
        palette_extended += palette + palette[::-1]

    # Figure pour afficher palette_extended
    palette_length = len(palette_extended)
    x_palette = np.arange(palette_length)
    palette_source = ColumnDataSource(data=dict(x=x_palette, color=palette_extended))


    palette_rect = p_palette.rect(x='x', y=0, width=1, height=1, source=palette_source, color='color', line_color=None)

    # Conversion en RGB
    palette_rgb = np.array([tuple(int(color[i:i+2], 16) for i in (1, 3, 5)) for color in palette_extended])

    # Création des points de référence pour interpolation
    x_palette = np.linspace(0, 1, len(palette_extended))
    x_target = np.linspace(0, 1, k_max)

    # Interpolation cubique pour assurer une transition fluide
    interp_r = interp1d(x_palette, palette_rgb[:, 0], kind='cubic')
    interp_g = interp1d(x_palette, palette_rgb[:, 1], kind='cubic')
    interp_b = interp1d(x_palette, palette_rgb[:, 2], kind='cubic')

    # Générer les couleurs interpolées
    colors_rgb = np.stack([interp_r(x_target), interp_g(x_target), interp_b(x_target)], axis=1).astype(int)

    # Conversion en format hexadécimal pour Bokeh
    colors = ['#%02x%02x%02x' % tuple(rgb) for rgb in colors_rgb]
    #gradient = generate_sampled_rgb_colors(k_max)

    # Créer de nouvelles positions et tailles pour les cercles
    for k in range(1, k_max+1):
        x.append(np.cos(10*np.pi*k/k_max)*(1-np.square((np.cos(16*np.pi*k/k_max)))/2))
        y.append(np.sin(10*np.pi*k/k_max)*(1-np.square((np.cos(16*np.pi*k/k_max)))/2))
        r.append(0.005 + 0.1*np.power(np.sin(52*np.pi*k/k_max), slider2.value))

    # Ajouter les nouveaux cercles au plot et stocker les GlyphRenderers
    new_circles = plot.circle(x, y, radius=r, color="blue", alpha=0.6, fill_color=None, line_color=colors, line_width=0.5)
    #new_dot = plot.circle_dot(x, y, alpha=0.6)
    
    # Circles est maintenant une liste des GlyphRenderers des cercles ajoutés
    circles.clear()  # Vider la liste
    palettes_viz.clear()
    circles.append(new_circles)
    palettes_viz.append(palette_rect)
    #circles.append(new_dot) # Ajouter les nouveaux cercles

# Créer le slider pour changer la valeur de k_max
slider = Slider(start=1, end=14000, value=1000, step=1000, title="Nombre de cercles")

# Créer le slider pour changer la valeur de la puissance
slider2 = Slider(start=1, end=6, value=4, step=1, title="Puissance")

# Créer le slider pour changer la valeur de la puissance
slider3 = Slider(start=1, end=10, value=3, step=1, title="Bouclage de la palette")

# Menu déroulant pour sélectionner la palette
palette_select = Select(title="Choisir une palette", value='Viridis', options=list(all_palettes.keys()))





# Lier le slider à la fonction qui met à jour les cercles
slider.on_change('value', update_circles)
slider2.on_change('value', update_circles)
slider3.on_change('value', update_circles)
palette_select.on_change('value', update_circles)


# Ajouter le slider et le graphique à l'interface
layout = column(slider, slider2, slider3, palette_select, p_palette, plot)

# Exécuter la fonction initiale pour afficher les cercles au début
update_circles(None, None, slider.value)

# Ajouter le layout au document Bokeh
curdoc().add_root(layout)

#export_svg(plot, filename="plot.svg")