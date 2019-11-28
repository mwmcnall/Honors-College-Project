from .DataContainer import DataContainer

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.pyplot import figure
plt.rcParams.update({'font.size': 15})
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

class Graph(DataContainer):
    """
    A class that inherits from DataContainer, designed to make graphing with
    DataFrames somewhat more customized for my needs
    """
    def __init__(self, df, figwidth=11, figheight=7, **kwargs):
        super().__init__(df, **kwargs)
        self.figwidth=figwidth
        self.figheight=figheight

        return

    def _create_plot(self, title, xlabel, ylabel):
        """
        Creates a single figure and then labels it
        """
        ax = figure(figsize=(self.figwidth, self.figheight)).subplots(1)

        self._plot_label(ax, title, xlabel, ylabel)

        return ax

    def _plot_label(self, ax, title, xlabel, ylabel):
        """
        Adds labels to the plot
        """
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        return

    def sum_col_barplot(self, cols, title, xlabel, ylabel, names, pos_gap=10):
        """
        Sums the columns sent in and plots them in the order that they were
        given

        :param cols: List of columns, each of which will become a bar on the
            bar graph
        :param names: The names that will appear under each bar in order
        :param pos_gap: The distance between each bar
        :return: Nothing,
        """
        vals = []
        # TODO: Turn to list comprehension
        for col in cols:
            vals.append(self.df[col].sum())

        ax = self._create_plot(title, xlabel, ylabel)

        # Chooses the position of each barplots on the x-axis
        y_pos = [i * pos_gap for i in range(0, len(cols))]
        ax.bar(y_pos, vals, width=30)

        # Create names on the x-axis
        ax.set_xticks(y_pos, names)

        return

    def two_shared_barplot(self, barWidth, col_1, col_2,
                           label_1, label_2, section_labels, title, xlabel,
                           ylabel, col_spacing=3, color1='red', color2='blue'):
        """

        """
        assert len(col_1) == len(col_2), ("Function designed only for columns"
            "with exactly the same length.")
        assert len(col_1) == len(section_labels), ("Length of column 1 and"
            "number of section labels must be same.")

        ax = self._create_plot(title, xlabel, ylabel)

        col_1_data = []
        # Calculates the total of totals
        col_1_tot = self.df[col_1].sum().sum()
        col_2_data = []
        col_2_tot = self.df[col_2].sum().sum()

        # Sums all the columns, this is the height of the bar
        for i in range(0, len(col_1)):
            col_1_data.append(df[col_1[i]].sum() / col_1_tot)
            col_2_data.append(df[col_2[i]].sum() / col_2_tot)

        # Generate location of all bars
        col_1_loc = [*range(1, len(col_1) * col_spacing, col_spacing)]
        col_2_loc = [i + 1 for i in col_1_loc]

        ax.bar(col_1_loc, col_1_data, width=barWidth, color=color1,
                label=label_1)
        ax.bar(col_2_loc, col_2_data, width=barWidth, color=color2,
                label=label_2)

        ax.legend()

        plt.xticks(col_1_loc, section_labels)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=2))

        # plt.show()
        return

    def scatter(self, x_col, y_col, title, xlabel, ylabel, x_bounds=None,
                y_bounds=None, alpha=1, c=None, label_percs = False,
                rev_x = False, rev_y = False, x_low_limit = -9**999,
                x_high_limit=9**999, y_low_limit = -9**999,
                y_high_limit=9**999, reg_line = False):
        """
        Creates a scatterplot of the data given

        :param x_col: Data on the x column
        :param y_col: Data on the y column
        :param x_bounds: Limit or reverse the x-axis data
        :param y_bounds: Limit or reverse the y-axis data
        :param label_percs: Set to True to get percentages to 2-decimal places
            on both axes
        :param rev_x: Reverse x-axis if True
        :param rev_y: Reverse y-axis if True
        :param x_low_limit: Lower-limit for x-axis' data, inclusive
        :param y_low_limit: Lower-limit for y-axis' data, inclusive
        :param x_high_limit: Upper-limit for x-axis' data, inclusive
        :param y_high_limit: Upper-limit for y-axis' data, inclusive
        :return: The scatterplot generated
        """
        #TODO: Come up with a better idea for the default limit sizes
        #TODO: label_percs forces percentages on both axes atm, would be
            # smarter to be able to set either axis

        ax = self._create_plot(title, xlabel, ylabel)

        scatter_data = self.df[(self.df[x_col] >= x_low_limit) &
                        (self.df[x_col] <= x_high_limit) &
                        (self.df[y_col] >= y_low_limit) &
                        (self.df[y_col] <= y_high_limit)]
        x = scatter_data[x_col]
        y = scatter_data[y_col]
        ax.scatter(x, y,
                    alpha=alpha,
                    c=c)
        ax.grid(True)

        if rev_x:
            ax.set_xlim(max(x), min(y))
        elif x_bounds != None:
            ax.set_xlim(x_bounds[0], x_bounds[1])
        if rev_y:
            ax.set_ylim(max(y), min(y))
        elif y_bounds != None:
            ax.set_ylim(y_bounds[0], y_bounds[1])

        if label_percs:
            ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=2))
            ax.xaxis.set_major_formatter(ticker.PercentFormatter(decimals=2))

        if reg_line:
            self.add_regline(x, y)

        del scatter_data

        return plt.show()

    def scatter_two_percs(self, cols, title, reg_line = False):
        self.scatter(x_col=cols[0], y_col=cols[1], title = title,
                     xlabel = cols[0],
                     ylabel = cols[1], alpha = .25, label_percs=True,
                     x_bounds=[-0.025, 1.025],
                     y_bounds=[-0.025,1.025],
                     x_low_limit=0.01,x_high_limit=0.99,
                     y_low_limit=0.01,y_high_limit=0.99, reg_line = reg_line)

        return

    def add_regline(self, x, y):
        # https://stackoverflow.com/questions/19068862/how-to-overplot-a\
        # -line-on-a-scatter-plot-in-python, user: 1"
        plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)),
            c='black')
        return
