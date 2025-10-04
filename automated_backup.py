import os
import subprocess
import datetime
import logging
import boto3   # Only needed if using AWS S3

# ----------------------------
# Configuration
# ----------------------------
SOURCE_DIR = "/path/to/local/directory"   # Local directory to backup

# Option 1: Remote server via rsync/ssh
REMOTE_USER = "username"
REMOTE_HOST = "192.168.1.100"
REMOTE_PATH = "/path/to/remote/backup"

# Option 2: AWS S3 bucket
USE_S3 = False
S3_BUCKET = "my-backup-bucket"
S3_PREFIX = "backups/"

# Logging setup
LOG_FILE = "backup_report.log"
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# ----------------------------
# Backup Functions
# ----------------------------
def backup_to_remote():
    """Backup directory to remote server using rsync"""
    try:
        cmd = [
            "rsync", "-avz", "--delete",
            SOURCE_DIR,
            f"{REMOTE_USER}@{REMOTE_HOST}:{REMOTE_PATH}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            logging.info(" Backup to remote server completed successfully.")
            print(" Backup to remote server completed successfully.")
        else:
            logging.error(f" Backup failed: {result.stderr}")
            print(f" Backup failed: {result.stderr}")

    except Exception as e:
        logging.error(f" Backup error: {str(e)}")
        print(f" Backup error: {str(e)}")


def backup_to_s3():
    """Backup directory to AWS S3"""
    try:
        s3 = boto3.client("s3")
        for root, dirs, files in os.walk(SOURCE_DIR):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, SOURCE_DIR)
                s3_key = os.path.join(S3_PREFIX, relative_path)

                s3.upload_file(local_path, S3_BUCKET, s3_key)
                logging.info(f"Uploaded {local_path} to s3://{S3_BUCKET}/{s3_key}")

        logging.info(" Backup to AWS S3 completed successfully.")
        print(" Backup to AWS S3 completed successfully.")

    except Exception as e:
        logging.error(f" S3 Backup error: {str(e)}")
        print(f" S3 Backup error: {str(e)}")


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    print(" Starting Backup Process...")

    if USE_S3:
        backup_to_s3()
    else:
        backup_to_remote()

    print("📜 Backup report saved to:", LOG_FILE)
