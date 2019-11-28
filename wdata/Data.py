from .DataCleaner import DataCleaner
from .Graph import Graph

class Data(Graph, DataCleaner):
    """
    Test
    """
    def __init(self, df, figwidth, figheight, **kwargs):
        super().__init__(df, figwidth, figheight, **kwargs)
