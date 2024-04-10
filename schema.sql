CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    permission INTEGER,
    displayname TEXT,
    bio TEXT,
    age INTEGER,
    pfp BYTEA,
    created_at TIMESTAMP
);

CREATE TABLE userauth (
    id SERIAL PRIMARY KEY,
    username TEXT REFERENCES users(username), 
    passhash TEXT,
    publickey TEXT,
    privatekey TEXT
);

GRANT SELECT, INSERT, UPDATE, DELETE ON userauth TO safedbauth;
ALTER TABLE userauth OWNER TO safedbauth;

CREATE TABLE media (
    id SERIAL PRIMARY KEY,
    media_type TEXT,
    media_data BYTEA,
    created_at TIMESTAMP
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    groupname TEXT,
    created_at TIMESTAMP
);

CREATE TABLE group_members (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES groups(id),
    user_id INTEGER REFERENCES users(id),
    joined_at TIMESTAMP
);

CREATE TABLE group_invites (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES groups(id),
    invited_id INTEGER REFERENCES users(id),
    inviter_id INTEGER REFERENCES users(id),
    sent_at TIMESTAMP
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    content TEXT,
    public BOOLEAN,
    created_at TIMESTAMP
);

CREATE TABLE post_media (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id),
    media_id INTEGER REFERENCES media(id)
);

CREATE TABLE post_likes (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id),
    liker_id INTEGER REFERENCES users(id),
);

CREATE TABLE post_reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    post_id INTEGER REFERENCES posts(id),
    reason TEXT,
    created_at TIMESTAMP
);

CREATE TABLE replies (
    id SERIAL PRIMARY KEY,
    reply_id INTEGER REFERENCES messages(id),
    post_id INTEGER REFERENCES messages(id),
    content TEXT,
    created_at TIMESTAMP
);

CREATE TABLE reply_media (
    id SERIAL PRIMARY KEY,
    reply_id INTEGER REFERENCES replies(id),
    media_id INTEGER REFERENCES media(id)
);

CREATE TABLE reply_likes (
    id SERIAL PRIMARY KEY,
    reply_id INTEGER REFERENCES replies(id),
    liker_id INTEGER REFERENCES users(id),
);

CREATE TABLE reply_reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    reply_id INTEGER REFERENCES replies(id),
    reason TEXT,
    created_at TIMESTAMP
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES users(id),
    recipient_id INTEGER REFERENCES users(id),
    content TEXT,
    created_at TIMESTAMP
);

CREATE TABLE message_media (
    id SERIAL PRIMARY KEY,
    message_id INTEGER REFERENCES messages(id),
    media_id INTEGER REFERENCES media(id)
);

CREATE TABLE group_dms (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES users(id),
    group_id INTEGER REFERENCES groups(id),
    content TEXT,
    created_at TIMESTAMP
);

CREATE TABLE group_dm_media (
    id SERIAL PRIMARY KEY,
    dm_id INTEGER REFERENCES group_dms(id),
    media_id INTEGER REFERENCES media(id)
);

