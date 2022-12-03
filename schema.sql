CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE events (id SERIAL PRIMARY KEY, name TEXT, description TEXT, creator_id INTEGER REFERENCES users, visible BOOLEAN DEFAULT TRUE, datetime TIMESTAMP, location TEXT DEFAULT '-', private_key TEXT);
CREATE TABLE enrolments (id SERIAL PRIMARY KEY, event_id INTEGER REFERENCES events, user_id INTEGER REFERENCES users, role INTEGER);
CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT, user_id INTEGER REFERENCES users, event_id INTEGER REFERENCES events, send_time TIMESTAMP);
CREATE TABLE votables (id SERIAL PRIMARY KEY, item TEXT, event_id INTEGER REFERENCES events);
CREATE TABLE votes (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, votable_id INTEGER REFERENCES votables, vote INTEGER DEFAULT 0);
CREATE TABLE tasks (id SERIAL PRIMARY KEY, task_name TEXT, event_id INTEGER REFERENCES events, volunteer INTEGER REFERENCES users);
