-- Wow you can comment in sql :D

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

-- Auth table, accessible by separate authentication role user
CREATE TABLE userauth (
    id SERIAL PRIMARY KEY,
    username TEXT REFERENCES users(username), 
    passhash TEXT,
    publickey TEXT,
    privatekey TEXT
);

GRANT SELECT, INSERT, UPDATE, DELETE ON userauth TO safeauth;
ALTER TABLE userauth OWNER TO safeauth;

-- All  media 
CREATE TABLE media (
    id SERIAL PRIMARY KEY,
    media_type TEXT, -- image, video, ...  (maybe in the future) -> html, code, text... - default to download
    media_data BYTEA,
    created_at TIMESTAMP
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    groupname TEXT,
    created_at TIMESTAMP
);

CREATE TABLE content (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    category TEXT, -- post, reply, message, groupdm
    parent_id INTEGER REFERENCES content(id), -- replies
    recipient_id INTEGER REFERENCES users(id), -- messages
    group_id INTEGER REFERENCES groups(id), -- group dms
    content TEXT,
    public BOOLEAN,
    created_at TIMESTAMP
);

CREATE TABLE content_media (
    id SERIAL PRIMARY KEY,
    content_id INTEGER REFERENCES content(id),
    media_id INTEGER REFERENCES media(id)
);

-- for post limited visibility
CREATE TABLE content_group (
    id SERIAL PRIMARY KEY,
    content_id INTEGER REFERENCES content(id),
    user_id INTEGER REFERENCES users(id) -- user who can see the content
);

-- only currently intended available for posts and replies
CREATE TABLE content_likes (
    id SERIAL PRIMARY KEY,
    content_id INTEGER REFERENCES content(id),
    liker_id INTEGER REFERENCES users(id)
);

-- only currently intended available for posts and replies
CREATE TABLE content_reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    content_id INTEGER REFERENCES content(id),
    reason TEXT,
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