<div align="center">
  
# Safespace
A Python Flask and Postgresql social media site to share p2p encrypted media

<img src="https://github.com/EternalLeo/safespace/blob/main/static/safelogo.png" alt="cat in box logo" width="200"/>

### What is this?

Safespace is a social media site to post publicly or share encrypted media,\
audio, video, images, text, with your friends.\
<br>

<img src="https://github.com/EternalLeo/safespace/blob/main/static/preview.png" alt="drawing" width="600"/>
</div>
<br>

## Installation
Requirements:
- compatible python version (latest)
- postgresql

>Remember!\
>Enter your own values for "user" (your postgresql username) and "pass" (various passwords)\
>Use secure passwords for the safeauth role, pepper, and secret key.
<br>

Clone the repository, run
  ```terminal
  git clone https://github.com/EternalLeo/safespace.git
  cd safespace
  pip install -r requirements.txt
  psql -U user -c "CREATE DATABASE safedb;"
  psql -U user -d safedb -c "CREATE ROLE safeauth WITH LOGIN PASSWORD 'pass';"
  psql -U user -d safedb -a -f schema.sql
  ```

Now you're almost set!
Specify the following environment variables:
  ```terminal
  DATABASE_URL=postgresql://user:pass@localhost:5432/safedb
  DATABASE_URL_AUTH=postgresql://safeauth:pass@localhost:5432/safedb
  DATABASE_PEPPER=pass
  SECRET_KEY=pass
  ```

Run the website with
  ```terminal
  flask --app backend.py run
  ```

## Core Features
- User authentication
  - Stores password hashes with salt and pepper!
- Posts, profiles
- Messaging and shared media
- Groups
- Global posts heart-counter

## Current progress and to-do

🔲 Ready boilerplate code\
🔲 Database schema\
🔲 Modern website design\
🔲 Working authentication\
🔲 Layout finished\
🔲 Home feed\
⬛ Messages (informative placeholders)\
⬛ Groups (potential merge with messages)\
🔲 Profiles

Long-term goals:\
⬛ Full encrypted privacy\
as fun as thinking about the specifics of sharing encrypted media with key exchanges is...\
⬛ More customization\
⬛ Refined look\
⬛ Potential moderation\
The python code is relatively straightforward and thus modularising it can come later.
