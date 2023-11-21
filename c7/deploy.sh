python3 -m poetry shell
poetry install
python3 manage.py migrate
python3 manage.py collectstatic --no-input
exit
