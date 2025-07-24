-- init_db.sql

CREATE TABLE IF NOT EXISTS users (
  id        SERIAL PRIMARY KEY,
  username  TEXT NOT NULL,
  password  TEXT NOT NULL,
  rc4_token TEXT NOT NULL
);

INSERT INTO users (username, password, rc4_token)
VALUES
  ('elliot', 'dont_use_this', 'QzJ1Y1hZWFlaVGhpc0lzQWJsb2I=')
ON CONFLICT DO NOTHING;
