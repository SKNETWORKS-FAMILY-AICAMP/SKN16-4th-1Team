python -m venv .venv

.venv/Scripts/activate

pip install --upgrade pip

pip install -r requiremnets.txt

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser
{
    id = admin
    email = admin@naver.com
    pw = 1111
}
python manage.py runserver
