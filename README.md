# bot_assistent

### Bot assistent in Telegram messenger. Help you to organise your day, play with or even send you funny gifs

## Run

``
python bot.py
``

## Deployment, using Heroku

#####Install the Heroku CLI

Download and install the Heroku CLI.

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.

``
$ heroku login
``

Clone the repository

Use Git to clone {poject name} source code to your local machine.

``
$ heroku git:clone -a {poject name}
$ cd {poject name}
``

Deploy your changes

Make some changes to the code you just cloned and deploy them to Heroku using Git.

``
$ git add .
$ git commit -am "make it better"
$ git push heroku master
``