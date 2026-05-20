-- sqlite3 board.sqlite < init_database.sql

DROP TABLE iF EXISTS board;

CREATE TABLE board (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(50),
    message VARCHAR(200),
);

INSERT INTO board(title, message) VALUES('title1', 'message1');
INSERT INTO board(title, message) VALUES('title2', 'message2');