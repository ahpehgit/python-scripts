#importing bokeh and pandas
from bokeh.plotting import figure, output_file, show
import pandas

#prepare some data

df = pandas.read_excel("http://pythonhow.com/data/verlegenhuken.xlsx", sheet_name=0)
pressures = df["Pressure"]/10
temperatures = df["Temperature"]/10

#prepare the output file
output_file("Weather_data.html")

#create a figure object
p=figure(plot_width=800, plot_height=700, tools='pan')

p.title.text="Temperature and Air Pressure"
p.title.text_color="Black"
p.title.text_font="times"
p.title.text_font_style="bold"
p.xaxis.minor_tick_line_color=None
p.yaxis.minor_tick_line_color=None
p.xaxis.axis_label="Temperature (Celsius)"
p.yaxis.axis_label="Pressure (hPa)"

#create line plot
p.triangle(temperatures, pressures)

#write the plot in the figure object
show(p)