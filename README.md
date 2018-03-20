# SuggestBot_Crowdsourcing_Preprocessing
Preprocessing pipeline for suggestbot video crowdsouricng. Implemented in Django-app.

How to run the project:

1. go to the project directory -- the same folder as the project's `manage.py` is placed
2. create a virtual environment: `$ virtualenv env`
3. activate the virtual environment: `$ source ./env/bin/activate`
4. upgrade youtube api: `$ pip3 install --upgrade google-api-python-client`
5. migrate project: `python3 manage.py migrate`
6. runserver: ` python3 manage.py runserver 0.0.0.0:8000`
7. visit localhost url: http://127.0.0.1:8000/preprocessing/inspection_test/
