from app import app
# I created run.py as runner because there were circular reference issues
# w.r.t to python imports
# https://stackoverflow.com/questions/21766960/operationalerror-no-such-table-in-flask-with-sqlalchemy
app.run(host='0.0.0.0', port=8081, debug=True)
