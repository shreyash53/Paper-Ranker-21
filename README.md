## Install Mongo
https://docs.mongodb.com/manual/administration/install-on-linux/

## Install virtualenv
https://medium.com/featurepreneur/how-to-install-virtualenv-in-ubuntu-12ddebc992a6

## Clone the Repo or Download the code into your machine

`Navigate to the project directory in your terminal`

## Create and activate env
`virtualenv env`

`source env/bin/activate`   

*(only for windows - activate env using)*

`.env\Scripts\activate`

if it gives any error, run command

*Set-ExecutionPolicy Unrestricted -Scope Process*

and then activate

## Install required python packages

`pip install -r requirements.txt`

## Running the application
`python3 driver.py`


## Notes

- This will start the Flask server and the application is ready

- Open your Web browser and enter the URL `localhost:5000/paper/search`

- In the Landing page of the application:

- - If you are a student, you can search for any paper by entering any query in the search box and hit enter, you will be shown the fetched results

- - If you are a publisher, you can add papers under your own name to our application for other users to read. You just have to Sign Up with an account and add your paper