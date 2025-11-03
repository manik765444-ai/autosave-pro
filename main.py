import os
import shutil
import logging
import argparse
from datetime import datetime
import tarfile

# Configure logging
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_backup_directory(backup_dir):
    """
    Creates the backup directory if it does not exist.

    Args:
        backup_dir (str): The path to the backup directory.
    """
    try:
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            logging.info(f'Backup directory {backup_dir} created')
    except OSError as e:
        logging.error(f'Error creating backup directory: {e}')

def get_files_to_backup(source_dir):
    """
    Gets a list of files to backup from the source directory.

    Args:
        source_dir (str): The path to the source directory.

    Returns:
        list: A list of files to backup.
    """
    try:
        return [os.path.join(source_dir, f) for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
    except OSError as e:
        logging.error(f'Error getting files to backup: {e}')
        return []

def backup_files(files_to_backup, backup_dir):
    """
    Backs up the files to the backup directory.

    Args:
        files_to_backup (list): A list of files to backup.
        backup_dir (str): The path to the backup directory.
    """
    try:
        for file in files_to_backup:
            filename = os.path.basename(file)
            backup_file = os.path.join(backup_dir, filename)
            shutil.copy2(file, backup_file)
            logging.info(f'File {file} backed up to {backup_file}')
    except OSError as e:
        logging.error(f'Error backing up files: {e}')

def create_tarball(backup_dir, tarball_file):
    """
    Creates a tarball of the backup directory.

    Args:
        backup_dir (str): The path to the backup directory.
        tarball_file (str): The path to the tarball file.
    """
    try:
        with tarfile.open(tarball_file, 'w:gz') as tar:
            tar.add(backup_dir)
        logging.info(f'Tarball {tarball_file} created')
    except tarfile.TarError as e:
        logging.error(f'Error creating tarball: {e}')

def main():
    parser = argparse.ArgumentParser(description='Backup automation script')
    parser.add_argument('-s', '--source', help='Source directory', required=True)
    parser.add_argument('-b', '--backup', help='Backup directory', required=True)
    parser.add_argument('-t', '--tarball', help='Tarball file', required=True)
    args = parser.parse_args()

    source_dir = args.source
    backup_dir = args.backup
    tarball_file = args.tarball

    create_backup_directory(backup_dir)
    files_to_backup = get_files_to_backup(source_dir)
    backup_files(files_to_backup, backup_dir)
    create_tarball(backup_dir, tarball_file)

if __name__ == '__main__':
    main()