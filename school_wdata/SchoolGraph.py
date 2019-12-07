from wdata import Graph

class SchoolGraph(Graph):
    """
    Graphing methods for SchoolData
    """
    def __init__(self, df, **kwargs):
        super().__init__(df,**kwargs)

    def grades_bargraph(self, plot_col, barWidth=1, title=None):
        """
        Creates a bar graph based on the grades offered by the school
        """
        try:
            self.grade_data_list
        except AttributeError:
            self._init_grade_data_list()
        if title == None:
            title = plot_col + ' by Grade'

        return(self.single_barplot_dfs_by_index(barWidth = 1,
            col = [True, plot_col],
            dfs = [grade.df for grade in self.grade_data_list],
            section_labels = ['SE','PK', 'K', '1', '2', '3', '4',
                '5', '6', '7', '8', '9', '10', '11', '12'],
            title = title,
            xlabel = 'Grades at School',
            ylabel = plot_col))

    def dis_bargraph(self, plot_col, dollarticks_y = False):
        """
        Creates a bar graph based on District and the plot column sent in
        """
        try:
            self.dis
        except AttributeError:
            self._init_dis()

        col = [self.dis.df[plot_col][i] for i in range(1,32+1)]

        return self.single_barplot(barWidth = 1.5,
            col = col,
            section_labels = [str(i) for i in range(1,32+1)],
            title = plot_col + ' by District',
            xlabel = 'District',
            ylabel = plot_col,
            dollarticks_y=dollarticks_y)


    def city_bargraph(self, plot_col):
        """
        Creates a bar graph for all the different cities in the dataset
        """
        try:
            self.cit
        except AttributeError:
            self._init_cit()

        col = [self.cit.df[plot_col][city] for city in self.city_names]
        self.single_barplot(col=col, section_labels=self.city_names,
            title=plot_col + ' by City',
            xlabel='Cities', ylabel=plot_col, bar_direction='horizontal',
                text_rotation='horizontal', barWidth=1.5, x_pad=0.1)
        return


    def rating_barplot(self, rating_col, plot_col, ax=None, **kwargs):
        """
        Creates a bar graph based on the rating column sent in
        """
        rig = self.df_groupby(rating_col)
        targets = ['Exceeding Target', 'Meeting Target',
            'Approaching Target', 'Not Meeting Target']
        col = [rig.df[plot_col][target] for target in targets]
        return rig.single_barplot(col=col, section_labels=targets,
            title=rating_col + ' by Target',
            xlabel='Targets', ylabel=plot_col, bar_direction='horizontal',
            text_rotation='horizontal', barWidth=1,
            x_pad=0.1, ax=ax, **kwargs)

    def all_ratings_barplot(self, plot_col, **kwargs):
        """
        Plots all the Ratings by the plot_col sent in
        """

        figwidth, figheight = self._set_multi_figs()

        graph_dict = {
            0: { 'rating_col': 'Trust Rating', 'plot_col': plot_col },
            1: { 'rating_col': 'Rigorous Instruction Rating',
                 'plot_col': plot_col },
            2: { 'rating_col': 'Collaborative Teachers Rating',
                 'plot_col': plot_col },
            3: { 'rating_col': 'Supportive Environment Rating',
                 'plot_col': plot_col },
            4: { 'rating_col': 'Effective School Leadership Rating',
                 'plot_col': plot_col },
            5: { 'rating_col': 'Strong Family-Community Ties Rating',
                 'plot_col': plot_col },
            6: { 'rating_col': 'Student Achievement Rating',
                 'plot_col': plot_col }
        }

        return self.multiplot(graph_dict, 7,1,
            title='All Ratings by ' + plot_col,
            x_labels=['Trust Rating', 'Rigorous Instruction Rating',
                'Collaborative Teachers Rating',
                'Supportive Environment Rating',
                'Effective School Leadership Rating',
                'Strong Family-Community Ties Rating',
                'Student Achievement Rating'
                ],
            y_labels=[plot_col] * 7,
            figwidth=figwidth,
            figheight=figheight,
            graph_fun=SchoolData.rating_barplot, sharex=False,
            top=0.925, hspace=0.2, flip_labels=True, sharey=True,
            overlabel=True)
