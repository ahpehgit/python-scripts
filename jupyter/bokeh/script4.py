from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import ColumnDataSource, HoverTool
import pandas

df = pandas.read_csv("Sample_of_the_produced_time_values.csv", parse_dates=["Start", "End"])

# create a new key to this dictionary that converts time value to string
df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d, %H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d, %H:%M:%S")

col_data_source = ColumnDataSource(df)
hover = HoverTool(tooltips=[("In", "@Start_string"), ("Out", "@End_string")])

p = figure(x_axis_type="datetime", height=100, width=500, sizing_mode="scale_both", title="Motion Graph")

p.yaxis.minor_tick_line_color = None
p.ygrid[0].ticker.desired_num_ticks = 1
p.add_tools(hover)

q = p.quad(left="Start", right="End", bottom=0, top=1, color="green", source=col_data_source)

output_file("MotionGraph.html")

show(p)