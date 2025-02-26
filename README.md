# stripe_api
Django + Stripe API

## Запуск API
1. Склонировать репозиторий
` git clone https://github.com/AlexMiller93/stripe_api.git`
` cd stripe_api`

2. Перейти в документацию stripe https://docs.stripe.com/ и создать аккаунт, передать credentials в .env по аналогии с .env.example

3. Выполняем миграции, создаем суперпользователя для создания объектов в админ панели с помощью следующих команд:

`python manage.py migrate`
`python manage.py createsuperuser`

4. Для запуска сервера через докер образ запустить команду
`docker-compose up --build`

* Для запуска сервера запустить команду на порте 8000
`python manage.py runserver 8000`, предварительно установив виртуальное окружение, а также необходимые пакеты из requirements.txt

5. В админ панели создаем несколько объектов items и добавляем их в заказы

6. Переходим по слудующим ссылкам
    -  `http://localhost:8000/item/1` для отображения информации по объекту

    -  `http://localhost:8000/buy/1` для покупки выбранного товара через систему  Stripe

    -  `http://localhost:8000/buy_order/1` для покупки выбранного заказа через систему Stripe

    -  `http://localhost:8000/order/1` для отображения информации о выбранном заказе





