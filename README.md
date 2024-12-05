# Favourite Question - Bluesky bot

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)

What is your favourite question?

A Bluesky bot that posts a new question daily.

A recreation of an old Twitter bot from the good old days...


## Requirements

- Python 3
- PostgreSQL
- A Bluesky account


## Set up

### Bluesky

Set up a new Bluesky account, make a note of the handle and password.

Even better, create a new application password just for this app.


### Database

#### DB access

If necessary, create a new database and user within PostgreSQL:

```sql
CREATE DATABASE favouritequestiondb;
\c favouritequestiondb;
CREATE USER favouritequestionuser WITH PASSWORD 'favouritequestionpw';
GRANT ALL PRIVILEGES ON DATABASE favouritequestiondb TO favouritequestionuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public to favouritequestionuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to favouritequestionuser;
```

#### DB population

Run the SQL commands in `db.sql` to create and populate the database with questions.


### Script

Clone this repo somewhere...

Set up a new virtual env:

```sh
python -m venv env
source env/bin/activate
```

Install dependencies:

```sh
pip install -r requirements.txt
```

Copy the `.env.example` file to `.env` and populate the relevant details:

```sh
cp .env.example .env
```

You may need to make the cron script executable:

```sh
chmod +x cron.sh
```

Set up a cron to run this daily:

```sh
crontab -e
```

Edit cron to run script daily, e.g. at 8:42am:

```sh
42 8 * * * /path/to/cron.sh >> /path/to/cron.log 2>&1
```


---

 DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
