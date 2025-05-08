import os
from ensure import ensure_annotations
from utils.logger import logger

@ensure_annotations
def create_directories(path_to_directories: list, verbose: bool = True):
    """
    Creates directories if they do not exist.

    Args:
        path_to_directories (list): List of directory paths to create.
        verbose (bool): If True, prints the status of directory creation.
    """
    for directory in path_to_directories:
        os.makedirs(directory, exist_ok=True)
        if verbose:
            logger.info("Directory %s created successfully.", directory)
