import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

df = df[
    (df["value"] >= df["value"].quantile(0.025))
    & (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():

  df_bar = df.copy()

 
  fig, ax = plt.subplots(figsize=(15, 5))
  ax.plot(df_bar.index, df_bar["value"], color="red", linewidth=1)

  ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
  ax.set_xlabel("Date")
  ax.set_ylabel("Page Views")

  
  fig.savefig("line_plot.png")
  return fig


def draw_bar_plot():

  df_bar = df.copy()
  df_bar["Year"] = df_bar.index.year
  df_bar["Month"] = df_bar.index.strftime("%B")

 
  df_grouped = (
      df_bar.groupby(["Year", "Month"])["value"].mean().unstack(level=1)
  )


  months_order = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
  ]
  df_grouped = df_grouped.reindex(columns=months_order)


  fig = df_grouped.plot(kind="bar", figsize=(15, 8), legend=True).figure
  plt.xlabel("Years")
  plt.ylabel("Average Page Views")
  plt.legend(title="Months", labels=months_order)
  plt.xticks(rotation=0)

  fig.savefig("bar_plot.png")
  return fig


def draw_box_plot():
  
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box["year"] = df_box["date"].dt.year
  df_box["month"] = df_box["date"].dt.strftime("%b")
  df_box["month_num"] = df_box["date"].dt.month
  df_box = df_box.sort_values("month_num")

  # Draw Seaborn box plots
  fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(20, 7))

  # Year-wise Box Plot (Trend)
  sns.boxplot(x="year", y="value", data=df_box, ax=ax1)
  ax1.set_title("Year-wise Box Plot (Trend)")
  ax1.set_xlabel("Year")
  ax1.set_ylabel("Page Views")

  
  months_short_order = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
  ]
  sns.boxplot(
      x="month", y="value", data=df_box, order=months_short_order, ax=ax2
  )
  ax2.set_title("Month-wise Box Plot (Seasonality)")
  ax2.set_xlabel("Month")
  ax2.set_ylabel("Page Views")

 
  fig.savefig("box_plot.png")
  return fig
