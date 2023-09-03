# flask-app


## Project Structure

The `helpmate` directory holds the application logic.

- `db.py` Where all database CRUD patterns are exposed as functions.
- `api/*.py`  Where the web api is exposed to the UI

The main directory holds the following files:
- `run.py` Where the Flask application is initialize and the config is loaded
- `sample_ini` Where the connection URI to MongoDB Atlas is configured
- `requirments.txt` Where the dependencies this project needs to run are located.

## How to set-up

Clone the repository.
```
https://github.com/MalakaRodrigo/helpmate.git
```

Start a python virtual env:
```
# navigate to the helpmate directory
cd helpmate

# create the virtual environment for MFlix
python3 -m venv helpmate-venv

# activate the virtual environment
source helpmate_venv/bin/activate
```

Install dependencies
```
python3 -m pip install -r requirments.txt
```

Rename the `sample_ini` to `.ini`.

[Get your Atlas cluster](https://docs.atlas.mongodb.com/getting-started/) with [sample data](https://docs.atlas.mongodb.com/sample-data/) set [connection string](https://docs.atlas.mongodb.com/connect-to-cluster/) and place in `DB_URI` parameter under `.ini`

Make sure you have IP in the Atlas [access list](https://docs.atlas.mongodb.com/security/add-ip-address-to-list/) and username/password of your Atlas user correctly specified.

## Start the application

```
python ./run.py
```

Open your browser on http://localhost:5000

## Disclaimer 

Use at your own risk; not a supported MongoDB product
