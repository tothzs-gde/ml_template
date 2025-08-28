from collections import OrderedDict
from typing import Callable

import pandas as pd


class Pipeline:
    """
    Example:
        pipe_1 = Pipeline([
            ("greet", lambda _: print("hello"))
        ])
        pipe_2 = Pipeline([
            ("no_greet", lambda _: print("door"))
        ])
        pipe_collector = Pipeline([
            ("pipe_1", pipe_1),
            ("pipe_2", pipe_2)
        ])
        pipe_collector()
    """

    def __init__(self, steps: list[tuple[str, Callable]], verbose: int = 0):
        self.length = len(steps)
        self.steps = OrderedDict(steps)
        self.verbose = verbose
    
    def __call__(self, df: pd.DataFrame = None, *args, **kwds):
        for name, function in self.steps.items():
            if self.verbose > 0:
                print(f"Processing: {name}")
            df = function(df)
        return df
