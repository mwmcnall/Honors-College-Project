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
from math import ceil

class Graph(DataContainer):
    """
    A class that inherits from DataContainer, designed to make graphing with
    DataFrames somewhat more customized for my needs
    """
    def __init__(self, df, figwidth=11, figheight=7, **kwargs):
        """
        Constructor method for Graph
        """
        super().__init__(df, **kwargs)
        self.figwidth=figwidth
        self.figheight=figheight
        if 'font_size' in kwargs:
            plt.rcParams.update({'font.size': kwargs['font_size']})
        return

    def _create_plot(self, title, xlabel, ylabel, ax=None,
        orientation='vertical'):
        """
        Creates a single figure for matplotlib plots and then labels it
        """
        if ax == None:
            ax = figure(figsize=(self.figwidth, self.figheight)).subplots(1)

        ax = self._plot_label(ax, title, xlabel, ylabel, orientation)

        return ax

    def _plot_label(self, ax, title, xlabel, ylabel, orientation ='vertical'):
        """
        Adds labels to the given plot and returns it
        """
        ax.set_title(title)
        if orientation=='vertical':
            ax.set_xlabel(xlabel)
        else:
            ax.set_ylabel(xlabel)
        if orientation=='vertical':
            ax.set_ylabel(ylabel)
        else:
            ax.set_xlabel(ylabel)
        return ax

    def _multiplot_label(self, ax, title, xlabel, ylabel,
        x_label_yes, y_label_yes):
        """
        Labels an x by y multiplot setup and returns the axes
        """
        if x_label_yes:
            ax.set_xlabel(xlabel)
        if y_label_yes:
            ax.set_ylabel(ylabel)
        return ax

    def sum_col_barplot(self, cols, title, xlabel, ylabel, names, pos_gap=10,
        sub_plot = False, c=None, prop_plot = False,
        partial_cols=None):
        """
        For each column sent in, sums each column and plots them in the order
        in which they were provided

        :param cols: List of columns, each of which will become a bar on the
            bar graph
        :param names: The names that will appear under each bar in order
        :param pos_gap: The distance between each bar
        :return: axes object
        """
        bar_vals = []
        # TODO: Turn to list comprehension
        if not prop_plot:
            for col in cols:
                bar_vals.append(self.df[col].sum())
        else:
            for index, col in enumerate(cols):
                bar_vals.append( self.df[partial_cols[index]].sum() /\
                    self.df[col].sum())

        ax = self._create_plot(title, xlabel, ylabel)

        # Chooses the position of each barplots on the x-axis
        y_pos = [num * pos_gap for num in range(0, len(cols))]
        ax.bar(y_pos, bar_vals, width=30, color=c,zorder=3,
               linewidth=1.2,edgecolor='black')
        # Sets grid behind bars
        ax.grid(True,zorder=0)

        # Create names on the x-axis
        ax.set_xticks(y_pos)
        ax.set_xticklabels(names)

        if sub_plot:
            return ax

        return plt.show()

    def single_barplot_dfs_by_index(self, barWidth, col, dfs,
                           section_labels, title, xlabel, ylabel, col_spacing=3,
                           label = '', c='red', sub_plot = False, **kwargs):
        """
        Creates a collection of barplots for a dataframe with a multi-index.
        Needs to take in multiple DataFrames with the same setup

        :param barWidth: The width of the bars
        :param col: The multi-index list selection in a [column, index] setup
        :param dfs: A list of dataframes that will be plotted from left to right
        :param section_labels: Labels each bar
        :param title: Title of the graph
        :param xlabel: x-axis label
        :param ylabel: y-axis label
        :param col_spacing: Space between the columns
        :param label: Legend-like label
        :param c: Color for the bars
        :return: Nothing
        """
        return self.single_barplot(col=col, section_labels=section_labels,
            title=title, xlabel=xlabel, ylabel=ylabel, col_spacing=3,
            barWidth=barWidth, label='', dfs=dfs, c='red',
            sub_plot=False, **kwargs)

    def single_barplot(self, col,
                       section_labels, title, xlabel, ylabel, col_spacing=3,
                       ax=None, barWidth=1, label = '', c='red',
                       text_rotation='horizontal', bar_direction='vertical',
                       **kwargs):
        """
        Creates a collection of barplots for a dataframe with a multi-index.

        :param barWidth: The width of the bars
        :param col: The collection of data to plot on the bars in a list format
        :param section_labels: Labels each bar
        :param title: Title of the graph
        :param xlabel: x-axis label
        :param ylabel: y-axis label
        :param col_spacing: Space between the columns
        :param label: Legend-like label
        :param c: Color for the bars
        :return: Nothing
        """
        if ax == None:
            ax = self._create_plot(title, xlabel, ylabel,
                                   orientation=bar_direction)

        # Generate location of all bars
        if 'dfs' in kwargs:
            col_loc = [*range(1, len(kwargs['dfs']) * col_spacing, col_spacing)]
            # Selects the information for each bar by multi-index selection
            col = [df[col[1]][col[0]] for df in kwargs['dfs']]
        else:
            col_loc = [*range(1, len(col) * col_spacing, col_spacing)]

        if bar_direction == 'vertical':
            ax.bar(col_loc, col, width=barWidth, color=c, label=label)
            # Label bars
            plt.xticks(col_loc, section_labels, rotation=text_rotation)
        # orientation == horizontal
        else:
            ax.barh(col_loc, col,height=barWidth, color=c, label=label)
            plt.yticks(col_loc, section_labels, rotation=text_rotation)
            plt.gca().invert_yaxis()
        if label != '':
            ax.legend()

        try:
            if kwargs['dollarticks_y']:
                formatter = ticker.FormatStrFormatter('$%1.2f')
                ax.yaxis.set_major_formatter(formatter)
        except:
            pass

        try:
            kwargs['sub_plot']
            plt.tight_layout(h_pad=kwargs['x_pad'], pad=0)
            return ax
        except:
            pass

        plt.tight_layout()

        return plt.show()

    def two_shared_barplot(self, barWidth, col_1, col_2,
                           label_1, label_2, section_labels, title, xlabel,
                           ylabel, col_spacing=3, color1='tab:blue',
                           color2='tab:orange'):
        """
        Takes in two separate lists of columns and creates a side-by-side bar
        plot setup in the order provided. Both lists of columns must be the same
        length, currently does not support mis-matched column lengths or bars
        of no height

        :param barWidth: The width of the bars
        :param col_1: Collection of column names stored in a list that will
            select information from the self.df
        :param col_2: Collection of column names stored in a list that will
            select information from the self.df
        :param label_1: Labels for col_1
        :param label_2: Labels for col_2
        :param section_labels: Labels each bar
        :param title: Title of the graph
        :param xlabel: x-axis label
        :param ylabel: y-axis label
        :param col_spacing: Space between the columns
        :param label: Legend-like label
        :param color1: Color for the first bars
        :param color2: Color for the second bars
        :return: Nothing
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

        # TODO: Can make this more efficient using numpy arrays
        # Sums all the columns, this is the height of the bar
        # col_1_data = self.df[col_1].values / col_1_tot
        # col_2_data = self.df[col_2].values / col_2_tot
        for i in range(0, len(col_1)):
            col_1_data.append(self.df[col_1[i]].sum() / col_1_tot)
            col_2_data.append(self.df[col_2[i]].sum() / col_2_tot)

        # Generate location of all bars
        col_1_loc = [*range(1, len(col_1) * col_spacing, col_spacing)]
        col_2_loc = [i + 1 for i in col_1_loc]

        # Grid behind bars
        ax.grid(True, zorder=0)
        ax.bar(col_1_loc, col_1_data, width=barWidth, color=color1,
                label=label_1, linewidth=1.2, edgecolor='#292828',
                zorder=3)
        ax.bar(col_2_loc, col_2_data, width=barWidth, color=color2,
                label=label_2, linewidth=1.2, edgecolor='#292828',
                zorder=3)

        ax.legend()

        plt.xticks(col_1_loc, section_labels)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=2))

        return plt.show()

    def scatter(self, x_col, y_col, xlabel, ylabel, title='', x_bounds=None,
                y_bounds=None, alpha=1, c=None, label_percs = False,
                rev_x = False, rev_y = False,
                reg_line = False, ax = None, **kwargs):
        """
        Creates a scatterplot of the data given

        :param x_col: Data on the x column
        :param y_col: Data on the y column
        :param x_bounds: Limit or reverse the x-axis data
        :param y_bounds: Limit or reverse the y-axis data
        :param label_percs: Set to True to get percentages to 1-decimal places
            on both axes
        :param rev_x: Reverse x-axis if True
        :param rev_y: Reverse y-axis if True
        :param x_low_limit: Lower-limit for x-axis' data, inclusive
        :param y_low_limit: Lower-limit for y-axis' data, inclusive
        :param x_high_limit: Upper-limit for x-axis' data, inclusive
        :param y_high_limit: Upper-limit for y-axis' data, inclusive
        :return: The scatterplot generated
        """
        #TODO: label_percs forces percentages on both axes atm, would be
            # smarter to be able to set either axis
        if ax == None:
            ax = self._create_plot(title, xlabel, ylabel)

        scatter_data = self._df_graph_limits(x_col, y_col, kwargs)
        x = scatter_data[x_col]
        y = scatter_data[y_col]
        ax.scatter(x, y, alpha=alpha, c=c)
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
            ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=1))
            ax.xaxis.set_major_formatter(ticker.PercentFormatter(decimals=1))

        if reg_line:
            ax = self.add_regline(x, y, ax)

        del scatter_data

        try:
            kwargs['sub_plot']
            return ax
        except:
            pass

        return plt.show()

    def _df_graph_limits(self, x_col, y_col, kwargs):
        """
        Sets x and y limits if supplied and returns the DataFrame that fits
        to those set limits

        :param x_col: String name of the x column
        :param y_col: String name of the y column
        :param x_low_limit: Inclusive numeric low-limit for the x column
        :param x_high_limit: Inclusive numeric upper-limit for the x column
        :param y_low_limit: Inclusive numeric low-limit for the y column
        :param y_high_limit: Inclusive numeric upper-limit for the y column
        :return: Dataframe that fits to the limits provided
        """
        if 'x_low_limit' in kwargs:
            x_low_limit = kwargs['x_low_limit']
        else:
            x_low_limit = self.df[x_col].min()
        if 'y_low_limit' in kwargs:
            y_low_limit = kwargs['y_low_limit']
        else:
            y_low_limit = self.df[y_col].min()
        if 'x_high_limit' in kwargs:
            x_high_limit = kwargs['x_high_limit']
        else:
            x_high_limit = self.df[x_col].max()
        if 'y_high_limit' in kwargs:
            y_high_limit = kwargs['y_high_limit']
        else:
            y_high_limit = self.df[y_col].max()

        return self.df[
            (self.df[x_col] >= x_low_limit) &
            (self.df[x_col] <= x_high_limit) &
            (self.df[y_col] >= y_low_limit) &
            (self.df[y_col] <= y_high_limit)
        ]

    def simple_scatter(self, cols, title='', reg_line = False, bound_mod=0.05,
        x_bounds = None, y_bounds = None, ax=None, **kwargs):
        """
        A simple scatter plot function that only requires an x and y column
        stored as a list to plot. Sets automatic bounds with a (default) 5%
        leeway at highest and lowest value on each column

        :param cols: x and y columns stored as [x,y] list
        :param title: Title for plot
        :param reg_line: Set to True for a regression line
        :param bound_mod: A % modifier for the x and y bounds. Set to 0 to
            ignore
        :param x_bounds: Hard inclusive bounds for x-axis
        :param y_bounds: Hard inclusive bounds for y-axis
        :param ax: Axes object, send in axes object if you want to add to a
            subplot
        :return: Returns axes object with scatterplot graphed
        """
        # TODO: Allow a single bound to be sent in
        # Configure bounds
        if x_bounds is None:
            x_min = self.df[cols[0]].min()

            x_max = self.df[cols[0]].max()

            x_bound_shift = (x_max - x_min) * bound_mod
            x_bounds = [x_min - x_bound_shift, x_max + x_bound_shift]
        if y_bounds is None:
            y_min = self.df[cols[1]].min()
            y_max = self.df[cols[1]].max()
            y_bound_shift = (y_max - y_min) * bound_mod
            y_bounds = [y_min - y_bound_shift, y_max + y_bound_shift]

        return self.scatter(x_col=cols[0], y_col=cols[1], title = title,
                     xlabel = cols[0],
                     ylabel = cols[1],
                     alpha = .25,
                     x_bounds=x_bounds,
                     y_bounds=y_bounds,
                     reg_line = reg_line,
                     ax=ax, **kwargs)

    def scatter_two_percs(self, cols, title='', reg_line = False, ax=None,
        **kwargs):
        """
        A simple scatterplot function designed for two percentage style columns

        :param cols: [x,y] list column setup
        :param title: Title for plot
        :param reg_line: Set to True for a regression line
        :param ax: Axes object, send in axes object if you want to add to a
            subplot
        :return: Returns axes object with scatterplot graphed
        """
        return self.scatter(x_col=cols[0], y_col=cols[1], title = title,
                     xlabel = cols[0],
                     ylabel = cols[1], alpha = .25, label_percs=True,
                     x_bounds=[-0.025, 1.025],
                     y_bounds=[-0.025,1.025],
                     x_low_limit=0.01,x_high_limit=0.99,
                     y_low_limit=0.01,y_high_limit=0.99, reg_line = reg_line,
                     ax=ax, **kwargs)

    def add_regline(self, x, y, ax):
        """
        Adds a regression line to an axes object

        :param x: x column information
        :param y: y column information
        :param ax: Axes object to add reg line too
        :return: Axes object with regression line included
        """
        # https://stackoverflow.com/questions/19068862/how-to-overplot-a\
        # -line-on-a-scatter-plot-in-python, user: 1"
        ax.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)),
            c='black')
        return ax

    def _multi_prep(self, sub_rows, sub_cols, graph_dict, sharey,sharex,
        x_labels, y_labels, title, **kwargs):
        """
        Conducts asserts for multiplot style functions and sets up subplots

        :param sub_rows: The number of subplot rows
        :param sub_cols: The number of subplot columns
        :param graph_dict: Nested-dictionary of graphing parameters
        :param sharex: Bool that signifies x-axes share bounds
        :param sharey: Bool that signifies y-axes share bounds
        :param x_labels: x-axis labels for an x by y style subplots
        :param y_labels: y-axis labels for an x by y style subplots
        :return: Return figure object, axes object, and a dictionary to update
            parameters to multiplot graphing methods
        """
        assert (sub_rows * sub_cols) == len(graph_dict), ("Number of rows and "
            "columns provided do not match the amount of graphs asked to graph")
        assert len(x_labels) == (sub_cols * sub_rows), ("Must have enough"
            "x_labels for every graph")
        assert len(y_labels) == sub_rows, ("Must have enough y_labels for"
            "every graph")
        figwidth, figheight = self._set_multi_figs(**kwargs)
        fig, axs = plt.subplots(sub_rows, sub_cols, sharey=sharey,
            sharex=sharex,
            figsize=(figwidth,figheight))

        # If axs multi-dimensional, convert to 1d list
        try:
            len(axs[0])
            axs = [i for sub in axs for i in sub]
        except TypeError:
            pass

        fig.suptitle(title)

        share_dict = self._share_dict_init(sharex, sharey)
        return fig, axs, share_dict

    def multiplot(self, graph_dict, sub_rows, sub_cols, title, graph_fun,
        x_labels, y_labels, sharey=False, sharex=False, top=None,
        hspace=None, wspace=None,
        flip_labels=False, overlabel = False, **kwargs):
        """
        Constructs an x by y multiplot using a single type of graphing function
        based on the nested parameters in a nested dictionary

        :param graph_dict: Nested-dictionary of graphing parameters
        :param sub_rows: The number of subplot rows
        :param sub_cols: The number of subplot columns
        :param title: Title for graph
        :param graph_fun: Function to graph
        :param x_labels: x-axis labels for an x by y style subplots
        :param y_labels: y-axis labels for an x by y style subplots
        :param sharex: Bool that signifies x-axes share bounds
        :param sharey: Bool that signifies y-axes share bounds
        :return: Return figure object, axes object, and a dictionary to update
            parameters to multiplot graphing methods
        """
        fig, axs, share_dict = self._multi_prep(sub_rows, sub_cols, graph_dict,
            sharey, sharex, x_labels, y_labels, title, **kwargs)

        for i in range(sub_rows * sub_cols):
            # Set correct subplot to update
            share_dict['ax'] = axs[i]
            # Add axes information to graph
            graph_dict[i].update(share_dict)
            # Graph to set subplot
            axs[i] = graph_fun(self, **graph_dict[i])

        self._multiplot_labeling(axs, x_labels, y_labels, sub_cols, sub_rows,
            flip_labels, overlabel)

        # TODO: Test with other multiplots to see if it still looks good with them!s
        plt.tight_layout()
        plt.subplots_adjust(top=top, hspace=hspace,wspace=wspace)

        return plt.show()

    def multiplot_multicol(self, graph_dict, sub_rows, sub_cols, title,
        graph_fun, x_labels, y_labels,
        top=None, hspace=None, wspace=None,
        sharey=False, sharex=False, **kwargs):
        """
        Constructs an x by y multiplot using a single type of graphing function
        based on the nested parameters in a nested dictionary. Designed to plot
        multiple x columns based on a single y-column

        Designed to only work with multiple columns on x-axis

        :param graph_dict: Nested-dictionary of graphing parameters
        :param sub_rows: The number of subplot rows
        :param sub_cols: The number of subplot columns
        :param title: Title for graph
        :param graph_fun: Function to graph
        :param x_labels: x-axis labels for an x by y style subplots
        :param y_labels: y-axis labels for an x by y style subplots
        :param sharex: Bool that signifies x-axes share bounds
        :param sharey: Bool that signifies y-axes share bounds
        :return: Return figure object, axes object, and a dictionary to update
            parameters to multiplot graphing methods
        """
        # TODO: with _multiplot_labeling does share_dict matter anymore?
        fig, axs, share_dict = self._multi_prep(sub_rows, sub_cols, graph_dict,
            sharey,sharex, x_labels, y_labels, title, **kwargs)

        # Actual graphing! Loops through the objects
        for i in range(sub_rows * sub_cols):
            # Set correct sub plot to update
            share_dict['ax'] = axs[i]
            # Add axes information to graph
            graph_dict[i].update(share_dict)
            # If x-axis has more than one dimension
            if type(graph_dict[i]['cols'][1]) == list:
                # Graph each separate x-axis within the same sub plot
                for k in range(len(graph_dict[i]['cols'][1])):
                    temp_dict = graph_dict[i].copy()
                    # This .copy() is necessary or else the next line will
                    # overwrite the original dictionary
                    temp_dict['cols'] = graph_dict[i]['cols'].copy()
                    temp_dict['cols'][1] = graph_dict[i]['cols'][1][k]
                    axs[i] = graph_fun(self, **temp_dict)
            else:
                graph_dict[i].update(share_dict)
                axs[i] = graph_fun(self, **graph_dict[i])

        self._multiplot_labeling(axs, x_labels, y_labels, sub_cols, sub_rows)

        # TODO: Test with other multiplots to see if it still looks good with them!s
        plt.tight_layout()
        plt.subplots_adjust(top=top, hspace=hspace,wspace=wspace)

        return plt.show()

    def _multiplot_labeling(self, axs, x_labels, y_labels, sub_cols, sub_rows,
        flip_labels=False, overlabel=False):
        """
        Labels multiplot style functions

        :param axs: List of axes objects
        :param x_labels: Labels x-axes of multiplot graphs
        :param y_labels: Labels y-axes of multiplot graphs
        :sub_cols: Number of columns in subplots
        :sub_rows: Number of rows in subplots
        :return: Nothing
        """
        # Prevents over-labeling
        if not overlabel:
            for ax in axs:
                ax.label_outer()

        if not flip_labels:
            for index, label in enumerate(x_labels):
                axs[index].set_xlabel(label)
            for index, label_index in enumerate(range(0,
                    ((sub_cols * sub_rows) - sub_cols) + 1,
                    sub_cols)):
                axs[label_index].set_ylabel(y_labels[index])
        else: # Flip labels
            for index, label in enumerate(y_labels):
                axs[index].set_xlabel(label)
            for index, label_index in enumerate(range(0,
                    ((sub_cols * sub_rows) - sub_cols) + 1,
                    sub_cols)):
                axs[label_index].set_ylabel(x_labels[index])
        return

    def _share_dict_init(self, sharex, sharey):
        """
        Creates a dictionary of parameters to send in to graphing methods based
        on whether or not to label certain axes
        """
        share_dict = {}
        if sharex:
            share_dict['x_label_yes'] = False
        else:
            share_dict['x_label_yes'] = True
        if sharey:
            share_dict['y_label_yes'] = False
        else:
            share_dict['y_label_yes'] = True
        share_dict['sub_plot'] = True
        return share_dict

    def _set_multi_figs(self, **kwargs):
        """
        Sets figwidth and figheight for multiplot style methods
        """
        if 'figwidth' not in kwargs:
            figwidth=self.figwidth
        else:
            figwidth=kwargs['figwidth']
        if 'figheight' not in kwargs:
            figheight=self.figheight
        else:
            figheight=kwargs['figheight']
        return figwidth, figheight
