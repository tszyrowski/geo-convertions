import numpy as np
import pandas as pd
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, HoverTool, Span
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot

output_file('interactive_path_sig.html', title="interactive path")

class InteractivePath():
    def __init__(self):
        x = np.arange(0, 1000, 0.5)
        self.df = pd.DataFrame({"x": x,
                                "y": np.sin(x),
                                "z": np.cos(x)})
        self.source = ColumnDataSource(self.df)

    def plot_path(self):
        plt = figure(title = "Sensor Path")
        plt.scatter(x="x", y="y",source=self.source, 
                    line_color=None, size = 6)
        # TODO implement interaction instead of hard coded index
        index=500    # this is where I think I need to create working callback
        print("x={}, y={}".format(self.df['x'][index], self.df['y'][index]))
        plt.circle(x=self.df['x'][index], y=self.df['y'][index], 
                   fill_color="red", size=15)
        hover = HoverTool()
        hover.tooltips=[("index", "@index"), ("senosr","@z")]
        plt.add_tools(hover)
        return plt

    def plot_signal(self):
        plt = figure(x_range=(450, 550), title="Signal Amplitude")
        plt.line(x="index", y="z", source=self.source, line_color="black", line_width=2)
        # TODO implement interaction instead of hard coded index
        index = 500  # I think this needs emit some singal to other plot
        vline = Span(location=index, dimension='height', line_color='red', line_width=3)
        plt.renderers.extend([vline])
        return plt

    def get_grid(self):
        """ place visualisation in a grid and display"""
        grid = gridplot([[self.plot_path()], [self.plot_signal()]], 
                 sizing_mode='stretch_both',)
        return grid

    def vis_main(self):
        """ use all visualisations"""
        show(self.get_grid())

if __name__=="__main__":
    vis = InteractivePath()
    vis.vis_main()