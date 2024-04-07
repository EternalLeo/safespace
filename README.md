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

Clone the repository, run
  ```terminal
  cd repo
  pip install -r requirements.txt
  psql -U user -d safeauth -a -f authtable.sql
  psql -U user -d safedb -a -f schema.sql
  ```

Now you're almost set!
Specify the following environment variables:
  ```terminal
  DATABASE_URL=postgresql://user:pass@localhost:5432/safeauth
  DATABASE_URL_AUTH=postgresql://user:pass@localhost:5432/safedb
  DATABASE_PEPPER=secretstring
  SECRET_KEY=secretstring
  ```

Run the website with
  ```terminal
  flask --app backend.py run
  ```

## Features
- User auth
Stores password hashes with salt and pepper!
- Posts, profiles
- Shared media (native support and sorting), dms
- Global posts like-counter
- Report feature
- Group chats and dms - all non global media is encrypted

## Current progress and to-do
- Database schema finished
- Comprehensive plan for rest of webapp

To implement...
- Frontend and backend functionality to-do.
- Versioning
- Full encryption of all media
