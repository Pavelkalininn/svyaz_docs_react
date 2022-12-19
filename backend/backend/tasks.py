import os

from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task
def remove_temp_files_task():
    logger.info('Temp file checker just ran.')
    filenames = [
        file for file in os.listdir('media')
        if file.startswith('temp') and file.endswith('.docx')
    ]
    logger.info(f'Temp files in directory: {filenames}.')
    for filename in filenames:
        os.remove(f'media/{filename}')
        logger.info(f'Temp file {filename} removed.')
