CREATE DATABASE app;

\connect app;

CREATE TABLE IF NOT EXISTS datasets (
    name TEXT PRIMARY KEY,
    path TEXT NOT NULL
);
