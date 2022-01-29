
python -m venv venv

call venv\Scripts\activate

python -m pip install --upgrade pip

pip install pandas==1.3.5
pip install yfinance

pip freeze > requirement.txt
