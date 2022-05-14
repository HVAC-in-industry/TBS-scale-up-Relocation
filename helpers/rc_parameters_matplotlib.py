"""
-------------------------------------------------------------------------------
Name:        rc_parameters_matplotlib
Purpose:     Matplotlib rc parameters declarations for plotting

Author:      Marcus Vogt

Created:     27.11.2021
Copyright:   Chair of Sustainable Manufacturing and Life Cycle Engineering, Institute of Machine Tools and Production Technology, Technische Universität Braunschweig, Langer Kamp 19b, 38106 Braunschweig, Germany
Licence:     CC BY-SA 4.0
-------------------------------------------------------------------------------
"""

import locale
from cycler import cycler

locale.setlocale(locale.LC_NUMERIC, 'english') # or 'english' or "german". Important for axes.formatter
# format the dates according to german language:
locale.setlocale(locale.LC_ALL, "english")

# latex_base = fullpage width
latex_base = {'figure.figsize'   : [7.48,3]    # 6.220,3.5# figure size in inches
                ,'figure.dpi'       : 80      # figure dots per inch
                # Eigenschaften der Achsen
                ,'axes.linewidth'      : 0.5     # edge linewidth
                ,'axes.grid'           : False   # display grid or not
                ,'axes.titlesize'      : 11.0   # fontsize of the axes title
                ,'axes.labelsize'      : 11.0  # fontsize of the x any y labels
                ,'axes.prop_cycle'    : (cycler('color',['#EC635C', '#4B81C4', '#F49961', '#8768B4', '#B45955','#CB74F4','#6EBB96']))  # color cycle for plot lines
                ,'axes.formatter.use_locale': True  # use decimal point or comma depending on locale.setlocale()
                # Eigenschaften der Tick-Marker
                ,'xtick.labelsize'      : 11.0 # fontsize of the tick labels
                ,'ytick.labelsize'      : 11.0 # fontsize of the tick labels
                # Eigenschaften der Linienplots
                ,'lines.linewidth'   : 1     # line width in points
                ,'lines.linestyle'   : '-'       # solid line
                ,'lines.marker'      : None    # the default marker
                ,'lines.markeredgewidth'  : 1     # the line width around the marker symbol
                # Eigenschaften der Flächen
                ,'patch.linewidth'        : 1     # edge width in points
                ,'patch.facecolor'        : '#EC635C'
                ,'patch.edgecolor'        : '#EC635C'
                # Eigenschaften der Legende
                ,'legend.fontsize'      : 11.0
                ,'legend.borderpad'     : 0.5    # border whitespace in fontsize units
                ,'legend.markerscale'   : 1.0    # the relative size of legend markers vs. original
                ,'legend.frameon'       : True   # whether or not to draw a frame around legend
                # Eigenschaften der Schriften
                ,'font.family'         : 'Arial' #'serif'
                ,'font.stretch'        : 'normal'
                ,'font.size'           : 11.0
                ,'font.sans-serif'     : ['Arial', 'Helvetica','sans-serif']
                # Eigenschaften fürs Speichern
                ,'savefig.dpi'         : 600      # figure dots per inch
                ,'savefig.format'      : 'pdf'      # png, ps, pdf, svg
                }

# Create another dictionary from the old one for larger figures.
latex_twocolumn = latex_base.copy() # You need to use the copy method, otherwise you will alter both dictionaries
latex_twocolumn['figure.figsize'] = [3.543, 2]
latex_twocolumn['axes.titlesize'] = 7
latex_twocolumn['axes.labelsize'] = 7
latex_twocolumn['xtick.labelsize'] = 7
latex_twocolumn['ytick.labelsize'] = 7
latex_twocolumn['legend.fontsize'] = 7
latex_twocolumn['font.size'] = 7

# Create another dictionary from the old one for larger figures.
latex_twothird = latex_base.copy() # You need to use the copy method, otherwise you will alter both dictionaries
latex_twothird['figure.figsize'] = [6.220, 5.5]

latex_largeColumn = latex_base.copy() # You need to use the copy method, otherwise you will alter both dictionaries
latex_largeColumn['figure.figsize'] = [6, 3]

# And one for fullsize figures
latex_fullpage = latex_base.copy()
latex_fullpage['figure.figsize'] = [6.220, 7.87]

# And here is one for Powerpoint presentations with fancy colors. Note that the save-format is also changed from pdf (which is
# vecorized and thus great for use in latex) to png because older version of PowerPoint can not handle pdfs
pp_figure = latex_base.copy()
pp_figure['axes.prop_cycle'] = (cycler('color',['#ff33cc', '#79f169', '#F49961', '#8768B4', '#B45955','#CB74F4','#6EBB96']))  # color cycle for plot lines
pp_figure['figure.figsize'] = [10,5.91]    # figure size in inches
pp_figure['axes.linewidth'] = 1     # edge linewidth
pp_figure['axes.titlesize'] =  18.0   # fontsize of the axes title
pp_figure['axes.labelsize'] = 18.0  # fontsize of the x any y labels
pp_figure['xtick.major.size'] = 6      # major tick size in points
pp_figure['xtick.minor.size'] = 3      # minor tick size in points
pp_figure['xtick.major.width'] = 1    # major tick width in points
pp_figure['xtick.minor.width'] = 1    # minor tick width in points
pp_figure['xtick.labelsize'] = 18.0 # fontsize of the tick labels
pp_figure['ytick.major.size'] = 6      # major tick size in points
pp_figure['ytick.minor.size'] = 3      # minor tick size in points
pp_figure['ytick.major.width'] = 1    # major tick width in points
pp_figure['ytick.minor.width'] = 1    # minor tick width in points
pp_figure['ytick.labelsize'] = 18.0 # fontsize of the tick labels
pp_figure['lines.linewidth'] = 2     # line width in points
pp_figure['lines.markeredgewidth'] = 2     # the line width around the marker symbol
pp_figure['lines.markersize'] = 8            # markersize, in points
pp_figure['patch.linewidth'] = 2.0     # edge width in points
pp_figure['legend.fontsize'] = 18.0
pp_figure['font.size'] = 18.0
pp_figure['font.family'] = 'sans-serif'
pp_figure['savefig.dpi'] = 150      # figure dots per inch
pp_figure['savefig.format'] = 'png'      # png, ps, pdf, svg