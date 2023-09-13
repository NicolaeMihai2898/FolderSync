import os, shutil
import logging.handlers
import logging
import time
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("sourse_folder")
parser.add_argument("destination_folder")
parser.add_argument("log_file", default = "history.log")
parser.add_argument("--synchronize_interval",type=int, default=5)

args = parser.parse_args()

source_folder = args.sourse_folder
destination_folder = args.destination_folder
log_file = args.log_file

handler = logging.handlers.WatchedFileHandler(args.log_file)

# define format of the log, in this case just a date & time with the log message
formatter = logging.Formatter("%(asctime)s;%(message)s")

# attach new formatter
handler.setFormatter(formatter)

# get logger instance and update its settings
logger = logging.getLogger()
logger.setLevel("INFO")
logger.addHandler(handler)

#Creating + Deleting folders
def copy_folder(source_folder, destination_folder):
    shutil.copytree(source_folder, destination_folder)
    logger.info(f"Folder copied: {source_folder}")

def remove_folder(folder_path):
    shutil.rmtree(folder_path)
    logger.info(f"Folder removed: {folder_path}")
while True:
    files_to_be_deleted = os.listdir(destination_folder)
    for file_name in files_to_be_deleted:
        source = source_folder + "/" + file_name
        destination = destination_folder + "/" + file_name
        # deleted files
        if os.path.exists(source) == False:
            if os.path.exists(destination):
                print('deleted', file_name)
                logging.info(f"File deleted: {file_name}")
                try:
                    os.remove(destination)
                except:
                    os.rmdir(destination)

    files =os.listdir(source_folder)
    for file_name in files:
        # construct full file path
        source = source_folder + "/" + file_name
        destination = destination_folder + "/" + file_name
        # created files
        if os.path.exists(source):
            if os.path.exists(destination) == False:
                logging.info(f"File created: {file_name}")
                print('created', file_name)
                # copy files
                try:
                    copy_folder(source, destination)
                except:
                    shutil.copy(source, destination)
                logging.info(f"File copied: {file_name}")
                print('copied', file_name)

        # remove folder
        if os.path.exists(source) == False:
            if os.path.exists(destination):
                remove_folder(destination_folder)
                logger.info(f"Folder removed: {destination_folder}")
    time.sleep(args.synchronize_interval)


