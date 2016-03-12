DROP TABLE IF EXISTS reading;
CREATE TABLE reading
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(40) NOT NULL,
    creation_time timestamp,
    text CHAR(500) NOT NULL,
    BG_passage_reference CHAR(40) NOT NULL,
    CONSTRAINT author_id_fk FOREIGN KEY (id) REFERENCES user (id)
);
CREATE UNIQUE INDEX reading_id_uindex ON reading (id);

DROP TABLE IF EXISTS content;
CREATE TABLE content
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(40) NOT NULL,
    creation_time timestamp,
    approved BOOLEAN DEFAULT FALSE,
    content CHAR(1000) NOT NULL,
    CONSTRAINT content_id_fk FOREIGN KEY (id) REFERENCES content_type (id),
    CONSTRAINT author_id_fk FOREIGN KEY (id) REFERENCES user (id)
);
CREATE UNIQUE INDEX content_id_uindex ON content (id);

DROP TABLE IF EXISTS reading_content;
CREATE TABLE reading_content
(
    reading_id INTEGER,
    content_id INTEGER,
    PRIMARY KEY (reading_id,content_id)
);

DROP TABLE IF EXISTS content_type;
CREATE TABLE content_type
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(40) NOT NULL
);
CREATE UNIQUE INDEX content_type_id_uindex ON content_type (id);

DROP TABLE IF EXISTS user;
CREATE TABLE user
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username CHAR(100) NOT NULL,
    password CHAR(100) NOT NULL,
    email_address CHAR(100) NOT NULL,
    first_name CHAR(100) NOT NULL,
    last_name CHAR(100) NOT NULL,
    active BOOLEAN DEFAULT TRUE
);
CREATE UNIQUE INDEX user_id_uindex ON user (id);

DROP TABLE IF EXISTS group;
CREATE TABLE group
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(100) NOT NULL,
    public BOOLEAN NOT NULL,
    creation_time timestamp,
    description CHAR(500) NOT NULL
);
CREATE UNIQUE INDEX group_id_uindex ON group (id);

DROP TABLE IF EXISTS group_invitation;
CREATE TABLE group_invitation
(
    user_id INTEGER,
    group_id INTEGER,
    creation_time timestamp,
    PRIMARY KEY (user_id, group_id)
);