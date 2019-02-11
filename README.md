# Cadre Query Interface

## Edit Config Files

```
cd conf
cp example.frontend.config.json frontend.config.json
cp example.backend.config backend.config
```

Update settings as appropriate.  

## Install Frontend

```
cd frontend
npm install
npm run build
```

## Install Backend

```
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Start Microserver

```
./start.sh
```