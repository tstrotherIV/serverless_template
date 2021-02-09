# Example Project

This is an example project using Flask and Lambda.

# Local Setup

### Assumptions

- You have a version of Python 3.6 installed as `python3`

    - Verify with `python3 --version`

### Pre-Setup

- Make sure you have an IAM user created with correct permissions in your AWS account

    - Create an Access Key on that user

    - Install awscli `pip install awscli`

    - Add that Access Key with `aws configure`

    - Verify with `aws configure list`

- Create a table for sessions and users in dynamodb on your AWS account for staging and production with id as the primary key

    - The users table will need an index named email_index on the attribute email

- Set the SESSIONS_TABLE and USERS_TABLE names in the staging and production settings files

### Setup

```bash
# create a virtual environment name venv
virtualenv venv --python=python3

# start the virtual environment
source venv/bin/activate

# install all of the requirements into the virtual environment
pip install -r requirements.txt

# install and confgire awscli here - see above
pip install awscli

# run the application with flask
export PYTHONPATH="$(pwd)"
export PYTHONUNBUFFERED=1
export FLASK_DEBUG=1
flask run
```

### Verify

Visit http://127.0.0.1:5000

### Problems

- Wrong version for python3:

    - Try installing `pyenv`, which allows you to manage multiple version of python on one machine

        - ```
          # intall thbe
          brew install openssl readline sqlite3 xz zlib

          # install pyenv
          curl https://pyenv.run | bash

          # add these next three lines to your bash_profile (assuming you use bash)
          export PATH="$HOME/.pyenv/bin:$PATH"
          eval "$(pyenv init -)"
          eval "$(pyenv virtualenv-init -)"

          # install python 3.6.10
          pyenv install 3.6.10

          # get the path to python 3.6.10 to be used when creating the virtual environment
          which ~/.pyenv/versions/3.6.10/bin/python
          ```
