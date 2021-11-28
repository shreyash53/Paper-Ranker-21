# Paper-Ranker

## Install Mongo
https://docs.mongodb.com/manual/administration/install-on-linux/

## Install virtualenv
https://medium.com/featurepreneur/how-to-install-virtualenv-in-ubuntu-12ddebc992a6

## Create and activate env
`virtualenv env`

`source env/bin/activate`   

*(only for windows - activate env using)*

`.env\Scripts\activate`

if it gives any error, run command

*Set-ExecutionPolicy Unrestricted -Scope Process*

and then activate

## Install required python packages
`pip install flask`

`pip install pymongo`

`pip install beautifulsoup4`

`pip install mongoengine`

*or simply run*

`pip install -r requirements.txt`

## Running the application
`python3 driver.py`
