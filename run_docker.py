import time
import os

import schedule


def job():
    os.system('sudo docker run --rm --name lostpetfinders --network host lostpetfinders_image')
    time.sleep(2)
    # os.system('password')

# тест
# schedule.every(1).minutes.do(job)
# запуск каждые 6 часов
# schedule.every(6).hour.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
