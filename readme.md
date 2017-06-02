# Fstat [![Build Status](https://travis-ci.org/gluster/fstat.svg?branch=master)](https://travis-ci.org/gluster/fstat)
Fstat tracks the failures from build.gluster.org.

## Installation
- Before you start installation make sure you have working installation of python2
- In your virtualenv run ``` pip install -r requirements.txt ```
- Hurray the installation is done

## Using fstat
- To serve the fstat app on localhost run ``` python manage.py runserver ```
- Use application.cfg to put all your development keys and debug flags
- To fetch failures from build.gluster.org run ``` python manage.py proccess_jobs -n <number_of_days> -j <job_name> ```
- By default fstat reads and writes the data into sqlite but it can be overriden in your application.cfg.
- To run all migration commands run ``` python manange.py db init|migrate|upgrade ```

## Consuming fstat data via rest apis

###  ``` /api/failures ```
This endpoint is used to get list of failures with the number of failure instances. The available filters for this endpoint are as follows:

**Name**|**Description**
:-----:|:-----:
start\_date| The date from which you want to get the failures (format yyyy-mm-dd)
end\_date| The date till which you want to get the failures (format yyyy-mm-dd)
branch| filter for specific branch

### ``` /api/failures/<fid> ```
This endpoint will return the list of failure instances for a particular failureID, this failure id is specific to fstat. The available filters for this endpoint are as follows:

**Name**|**Description**
:-----:|:-----:
start\_date| The date from which you want to get the failures (format yyyy-mm-dd)
end\_date| The date till which you want to get the failures (format yyyy-mm-dd)
branch| filter for specific branch
