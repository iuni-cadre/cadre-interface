# Cadre Query Interface

## Edit Config Files

```
cd conf
cp example.frontend.config.json frontend.config.json
cp example.backend.config backend.config
```

Update settings as appropriate.  

## Install Frontend

Frontend is built using Vue.js and can be compiled and updated using `npm`

```
cd frontend
npm install
npm run build
```

## Install Backend

The backend is written in Python and uses the Flask microframework.

```
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Start Microserver

When running locally, the flask microservice can be started using the following command.

```
./start.sh
```

In production, the query builder is deployed using AWS's Elastic Beanstalk hosting and does not rely on this start script.  It runs the application directly.

## Bundle for AWS Elastic Beanstalk


After you've got everything running properly through flask, you can bundle the app for deployment on AWS elastic beanstalk by running one of the below commands:

```
./bundle_for_beanstalk.sh
```

or

```
./deploy_to_beanstalk.sh
``

Both of these shell scripts will compile the frontend using `npm run build` and then bundle all the files up into a file called `eb_bundle.zip`.  `bundle_for_beanstalk` will only bundle the files and append a timestamp to the filename.  This file can then be uploaded manually to EBS.  

If configured properly, the `deploy_to_beanstalk` script will also deploy the bundle directly to EBS.  The EBS CLI must be installed and configured in order to use this.

**Note:**  This requires a `/conf/backend.config` file, which is not included in the git repo by default.  All the settings in backend.config will be used for the elastic beanstalk installation.