python -m venv .venv

.venv/Scripts/activate

.venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser
{
    id = admin
    email = admin@naver.com
    pw = 1111
}
python manage.py runserver


몇시간동안 시도했지만 2x2 패널 오류가 너무 심함
