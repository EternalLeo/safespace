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

### There is currently no reason to clone the repo!
### It has the landing page, of which there is a screenshot above.
### You can spy at the code straight from github.
### (if this changes, the readme will be updated)

>Remember!\
>Secure password for the safeauth role, it is responsible for user credentials.\
>Secure sequences for the pepper and secret key as well.
<br>

Clone the repository, run
  ```terminal
  cd repo
  pip install -r requirements.txt
  psql -U user -c "CREATE DATABASE safedb;"
  psql -U user -d safedb -c "CREATE ROLE safeauth WITH LOGIN PASSWORD 'password';"
  psql -U user -d safedb -a -f schema.sql
  ```

Now you're almost set!
Specify the following environment variables:
  ```terminal
  DATABASE_URL=postgresql://user:pass@localhost:5432/safedb
  DATABASE_URL_AUTH=postgresql://safeauth:pass@localhost:5432/safedb
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

🔲 Database schema mostly done\
🔲 Lots of time spent on graphics design and beautiful introduction page\
🔲 Boilerplate for follow-up logic\
⬛ Working registration + log-in\
⬛ App page with 3 tabs:\
⬛ Feed\
⬛ Messages\
⬛ Profile

It would be accurate to say this is only 20% done.\
I've spent spent a lot of the time thinking out the logic.\
I am planning to use this for myself on my own server so I will continue development. (If I'm making something, might as well make something useful)\
For now, in the next month, the goals are:
- Encryption can wait
as fun as thinking out the specifics of sharing encrypted media with key exchanges is... 
- Posting on a global feed
included a search function with simple search parameters (username, date, title, content, media attached)
- Direct messages chat
- Invite people into a group chat
- The profile tab only contains your bio and your public post history, maybe I'll make more customization but that's a later extra
