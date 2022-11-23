CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE events (id SERIAL PRIMARY KEY, name TEXT, description TEXT, creator_id INTEGER REFERENCES users, visible BOOLEAN DEFAULT TRUE);
CREATE TABLE enrolments (id SERIAL PRIMARY KEY, event_id INTEGER REFERENCES events, user_id INTEGER REFERENCES users, role INTEGER);
CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT, user_id INTEGER REFERENCES users, event_id INTEGER REFERENCES events, send_time TIMESTAMP)
