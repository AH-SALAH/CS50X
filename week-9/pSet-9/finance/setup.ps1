# Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

./venv/Scripts/activate
$env:FLASK_APP="application.py"
$env:FLASK_ENV="development"
$env:APP_SETTINGS="config.cfg"
$env:API_KEY="pk_7e955635c0c04c8993150cf40ab82c36"
flask run