""" Run the main function."""
from scripts.model_evaluation import model_evaluation

from src.logger import get_logger

def run():
    """Run the main function."""
    logger = get_logger(__name__)
    logger.info('Main Function')

    model_evaluation()

if __name__ == '__main__':
    run()
