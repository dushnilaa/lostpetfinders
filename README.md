# Настройка и запуск парсера

1. Создать таблицу mysql, если не создана
2. Настроить config.yaml
3. Собрать образ: sudo docker build -t lostpetfinders_image . 
4. Запустить образ: sudo docker run --rm --name lostpetfinders --network host lostpetfinders_image
