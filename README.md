# Harnis Registration App

## Prerequisites

To install:
```sh
git clone https://github.com/anantoj/harnis_registration_app.git
cd harnis_registration_app
pip install -r requirements.txt
```

Also make sure to set the `APP_EMAIL` and `APP_PASSWORD` environment variables with your email and corresponding app password respectively. 
In windows, you can do so by:
```sh
setx APP_EMAIL "<your-email>"
setx APP_PASSWORD "<your-app-password>"
```

Or in UNIX-based systems:
```sh
export APP_EMAIL="<your-email>"
export APP_PASSWORD="<your-app-password>"
```

## Usage

To run the app:
```sh
python harnis_registration_app.py
```