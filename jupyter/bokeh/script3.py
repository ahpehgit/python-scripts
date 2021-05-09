from bokeh.plotting import figure, output_file, show
import pandas

df = pandas.read_csv("adbe.csv", parse_dates=["Date"])

p = figure(width=500, height=500, x_axis_type="datetime", sizing_mode="stretch_both")
p.line(df["Date"], df["Close"], color="Orange", alpha=.5)

output_file("Time_series.html")

show(p)