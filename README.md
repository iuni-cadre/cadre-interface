# Cadre RAC Interface

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

## Bundle for AWS Elastic Beanstalk

After you've got everything running properly through flask, you can bundle the app for deployment on elastic beanstalk by running the below command:

```
./bundle_for_beanstalk.sh
```

This command will compile the frontend using `npm run build` and then bundle all the files up into a file called `eb_bundle.zip` which can then be uploaded through the EB console.

Note:  This requires a `/conf/backend.config` file, which is not included in the git repo by default.  All the settings in backend.config will be used for the elastic beanstalk installation.