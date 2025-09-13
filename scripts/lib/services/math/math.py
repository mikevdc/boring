from scripts.lib.enums import Operation
from scripts.lib.services.math import logger


def show_all_operations():
    logger.debug("Finding all the operations...")
    operations = {}

    for i, operation in enumerate(Operation):
        operations[i] = f"{operation.name} ({operation.value})"

    if not operations:
        logger.debug("No operations were found.")
        return None
    return operations
