
python -m venv venv

call venv\Scripts\activate

python -m pip install --upgrade pip

pip install selenium
pip install BeautifulSoup4
pip install firebase-admin
pip install feedparser

pip freeze > requirement.txt
