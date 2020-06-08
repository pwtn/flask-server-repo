from .pl_cibles_mediametrie import create_cibles
from .pl_regies_chaines import create_regies
from .utils import drop_collections

def run():
    drop_collections()
    create_regies()
    # create_chaines()
    create_cibles()
