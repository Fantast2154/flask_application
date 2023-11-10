"""
python -m venv [name]

venv/Scripts/activate
deactivate
pip freeze
pip install -r requirements.txt

set FLASK_APP=app.py
set FLASK_DEBUG=1
flask run --host 0.0.0.0 --port 5000

--reload
--no-reload

--debugger
--no-debugger

from app import app
app.url_map
"""