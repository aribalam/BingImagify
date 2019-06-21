import os
import getpass
from CronTab import crontab

INSTALL_DIR = os.getcwd()
COMMENT = 'BingImagify'

cron = CronTab(user=getpass.getuser())

# Scheduling the changing of wallpapers
job1 = cron.new(command=INSTALL_DIR + '/run.sh', comment=COMMENT)
job1.minute.every(30)

# Scheduling the download of new wallpapers
job2 = cron.new(command='python3 ' + INSTALL_DIR + '/image_downloader.py', comment=COMMENT)
job2.every_reboot()

cron.write()
