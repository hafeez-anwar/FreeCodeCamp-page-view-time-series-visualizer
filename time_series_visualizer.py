import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',parse_dates=["date"],
                index_col = "date"
                )

# Clean data
df.drop(df[(df['value'] < df['value'].quantile(0.025)) |\
           (df['value'] > df['value'].quantile(0.975))].index, inplace = True)

def draw_line_plot():
    # Draw line plot
    fig, axes = plt.subplots(figsize=(12, 6))
    axes.plot(df.index,df['value'], color='red', linewidth=1)
    axes.set_xlabel('Date')
    axes.set_ylabel('Page Views')
    axes.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")


    # Save image and return fig (don't change this part)
    # Just changes the "FACECOLOR" = WHITE which will save
    # the figure with its backgroud WHITE as shown in the
    # TARGET Image

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png',facecolor='white')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['months'] = df_bar.index.month
    df_bar['year'] = df_bar.index.year
    df_bar = df_bar.groupby(['year','months'], as_index = False)['value'].mean()
    # SOLUTION 1; PLOTTING using Seaborn
    graph = sns.catplot(
                            x='year',
                            y='value',
                            hue='months',
                            kind = 'bar',
                            data=df_bar,
                            legend = False,
                            palette=sns.color_palette("Paired", 12)
                       ).set_axis_labels("Years", "Average Page Views")
    fig = graph.fig
    fig.axes[0].legend(title='Months', loc='upper left',
                        labels=['January', 'February', 'March', 'April', 'May',
                        'June', 'July', 'August', 'September', 'October',
                        'November', 'December'])
    # SOLUTION 2: PLOTTING WITH PANDAS
    # Unstack the resultant grouping; This is important
    # df_cat = df_cat.unstack()
    #fig = df_cat.plot(kind = 'bar',legend = True,figsize = (12,7), xlabel = 'Years', ylabel = 'Average Page Views',rot=0)
    #fig.axes.legend(title='Months', loc='upper left',labels=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig
# This video was very helpful
# https://www.youtube.com/watch?v=KoTHJPzpw0c
def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    # https://forum.freecodecamp.org/t/page-view-time-series-visualizer-sort-months/431025/2
    df_box.sort_values(by=['year','date'],ascending=[False,True],inplace=True)

    # Draw box plots (using Seaborn)

    fig, axes = plt.subplots(1, 2, figsize=(20, 5))
    sns.boxplot(y="value", x= "year", data=df_box,  orient='v' , ax=axes[0]).set(xlabel = 'Year',ylabel = 'Page Views', title='Year-wise Box Plot (Trend)')
    sns.boxplot(y="value", x= "month", data=df_box,  orient='v' , ax=axes[1]).set(xlabel = 'Month',ylabel = 'Page Views', title = 'Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
