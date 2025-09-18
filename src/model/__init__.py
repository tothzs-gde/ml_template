import random
import numpy as np

from src.utils.settings import settings

RANDOM_SEED = settings.random_seed
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
