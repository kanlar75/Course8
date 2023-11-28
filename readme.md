Курсовая работа.

Уважаемый пользователь!

В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена 
приобретению новых полезных привычек и искоренению старых плохих привычек. 
В рамках курсовой работы была реализована бэкенд-часть веб-приложения трекера 
полезных привычек.

Важно указывать актуальный и правильный chat id при регистрации пользователя. 
Узнать его можно у бота https://t.me/getmyid_bot. 
Если не указать chat_id, то напоминания не будут отправляться.

ЗАПУСК ПРОЕКТА ЛОКАЛЬНО.

Клонируйте проект. Активируйте виртуальное окружение командой: poetry shell. 
Установите зависимости командой: poetry install.
Установите Redis (используется для периодических задач celer).

Создайте Базу данных PostgreSQL командами:
1. psql -U <имя пользователя>
2. CREATE DATABASE <имя базы данных>;
3. \q 

Пропишите переменные окружения в файл .env. 
Используемые в проекте переменные окружения записаны в файле .env.sample.
Для локального запуска установите ENV_TYPE='local'

Для миграции в базу данных используйте команду: python manage.py migrate

Для создания суперпользователя и пользователей используйте команду: python manage.py create_users

Выполните команду: python manage.py runserver

В адресной стоке браузера введите адрес http://127.0.0.1:8000/admin
Пароль и логин для суперпользователя:
login: admin@test.com password: 12345

Для всех пользователей (user1@test.com, user2@test.com, staff@test.com) password: 12345.
Откройте два терминала.
Для запуска планировщика celery используйте команду: 
python.exe -m celery -A config beat --loglevel=info. 
Остановка планировщика: ctrl + break.
Для запуска worker используйте команду: 
python.exe -m celery -A config worker -l INFO -P eventlet. 
Остановка worker: ctrl + break.

ЗАПУСК ПРОЕКТА В DOCKER.

Клонируйте проект.
Установите DOCKER и при необходимости docker-compose.
Пропишите переменные окружения в файл .env. 

Создайте образ командой docker-compose build

Используемые в проекте переменные окружения записаны в файле .env.sample.
Для запуска в docker установите ENV_TYPE='docker'

Запустите контейнеры командой docker-compose up

В адресной стоке браузера введите адрес http://127.0.0.1:8001/admin
Пароль и логин для суперпользователя:
login: admin@test.com password: 12345

Для всех пользователей (user1@test.com, user2@test.com, staff@test.com) password: 12345.

DEPLOY (DOCKER).

Подключитесь к удаленному серверу.
Обновите пакеты командой: sudo apt update
Установите пакеты: 
sudo apt install python3-poetry postgresql postgresql-contrib nginx docker docker-compose
Перейдите в директорию nginx: 
cd /var/www/html/
Вы можете использовать другой путь, но тогда необходимо отредактировать файл nginx_docker 
(замените /var/www/html/ на свой путь к проекту)
Скопируйте Django-проект на сервер (например, через git clone)

Выполните команды: 
sudo cp -f pg_hba.conf /etc/postgresql/14/main/pg_hba.conf
sudo systemctl restart postgresql
Создайте БД командами:
docker-compose exec db psql -U <имя пользователя>
CREATE DATABASE <имя базы данных>;
\q 

Пропишите переменные окружения в файл .env. 
Используемые в проекте переменные окружения записаны в файле .env.sample.
Для запуска в docker на удаленном сервере установите ENV_TYPE='docker_deploy'.

Скопируйте файл с настройками nginx командой:
sudo cp nginx_docker /etc/nginx/sites-available/habits
Выполните команду: 
sudo ln -s /etc/nginx/sites-available/habits /etc/nginx/sites-enabled
Запустите проект командой: 
sudo docker-compose up --build

В адресной стоке браузера введите адрес http://xxx.xxx.xxx.xx/admin
где xxx.xxx.xxx.xx ip ВМ
Пароль и логин для суперпользователя:
login: admin@test.com password: 12345
Для всех пользователей (user1@test.com, user2@test.com, staff@test.com) password: 12345.

Если сайт отображается не корректно, выполните команды:
poetry shell
python3 manage.py collectstatic
exit
sudo systemctl restart nginx

DEPLOY (GUNICORN).

Подключитесь к удаленному серверу.
Обновите пакеты командой: 
sudo apt update
Установите пакеты: 
sudo apt install python3-poetry postgresql postgresql-contrib nginx
Перейдите в директорию nginx: 
cd /var/www/html/ 
Вы можете использовать другой путь, но тогда необходимо отредактировать файлы 
nginx_gunicorn и habits.service 
(замените /var/www/html/ на свой путь к проекту, а также укажите путь к пакету gunicorn)
Скопируйте Django-проект на сервер (например, через git clone)

Выполните команды: 
sudo cp -f pg_hba.conf /etc/postgresql/14/main/pg_hba.conf
sudo systemctl restart postgresql
Создайте БД командами:
docker-compose exec db psql -U <имя пользователя>
CREATE DATABASE <имя базы данных>;
\q 

Пропишите переменные окружения в файл .env. 
Используемые в проекте переменные окружения записаны в файле .env.sample.
Для запуска в docker на удаленном сервере установите ENV_TYPE='no_local'.

Скопируйте файл с настройками daemon gunicorn командой:
sudo cp habits.service /etc/systemd/system/habits
Скопируйте файл с настройками nginx gunicorn командой:
sudo cp nginx_gunicorn /etc/nginx/sites-available/habits
Выполните команды: 
sudo ln -s /etc/nginx/sites-available/habits /etc/nginx/sites-enabled
systemctl restart habits
systemctl restart nginx
poetry config virtualenvs.in-project true
poetry init
poetry shell
poetry install
python3 manage.py migrate
python3 manage.py create_users
systemctl start habits

В адресной стоке браузера введите адрес http://xxx.xxx.xxx.xxx/admin
где xxx.xxx.xxx.xxx ip ВМ
Пароль и логин для суперпользователя:
login: admin@test.com password: 12345
Для всех пользователей (user1@test.com, user2@test.com, staff@test.com) password: 12345.

Если у вас возникли вопросы или проблемы при использовании проекта, 
свяжитесь со мной по электронной почте kls75@yandex.ru или оставьте комментарий 
в Issues проекта на GitHub https://github.com/kanlar75/course7/issues.
