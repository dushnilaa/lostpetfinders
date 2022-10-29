import time
import os

import schedule


def job():
    os.system('sudo docker run --rm --name parser_test -p 8080:8080 --network host'
              ' -v /home/work/projects/test/docker:/usr/parser_files/app parser_image')
    time.sleep(2)
    # os.system('password')


schedule.every(6).hour.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
