-- CREATE TABLE users(
--     user_id_email VARCHAR(20) PRIMARY KEY,
--     first_name VARCHAR(15) NOT NULL,
--     last_name VARCHAR(15) NOT NULL,
--     password VARCHAR(15) NOT NULL
-- );
-- --  take in input encode it and see if it matched password, like basic c4 store encoded
-- -- then when user enters in password take password encode and matchit to stored encoded password.
-- -- python encoding finctions , sha51? sha52? md5 base encoding - base64

-- -- CREATE TABLE pen_types(
-- --     type_id SERIAL PRIMARY KEY,
    
-- -- );

-- CREATE TABLE stock_pens(
--     s_pen_id SERIAL PRIMARY KEY,
--     pen_title VARCHAR(30) NOT NULL,
--     manufacturer VARCHAR(20),
--     start_year INTEGER,
--     end_year INTEGER,
--     general_info VARCHAR(2000) NOT NULL,
--     pen_version VARCHAR(15) NOT NULL, 
--     pen_category VARCHAR(20) NOT NULL
--     user_id_email VARCHAR(20) REFERENCES users(user_id_email) 
-- );

-- -- should I show active = true or false
-- -- 

-- -- type ahead search... and look at profaity filter libraries

-- -- CREATE TABLE version_pens(
-- --     v_pen_id  SERIAL PRIMARY KEY,
-- --     v_pen_title VARCHAR(30),
-- --     general_info VARCHAR(2000) NOT NULL,
-- --     year INTEGER,
-- --     s_pen_id SERIAL REFERENCES stock_pens(s_pen_id)
-- -- );

-- --  problem with entry if the user tries to put in a version pen that has not yet 
-- --  been created as a stock pen, as the forign key will error out?

-- CREATE TABLE event_log(
--     event_log_id SERIAL PRIMARY KEY,
--     date_time VARCHAR(30) NOT NULL,
--     user_id_email VARCHAR(20) REFERENCES users(user_id_email), 
--     s_pen_id SERIAL REFERENCES stock_pens(s_pen_id)
-- ); 

-- --  event_action_type 
-- --  log event type, create and update and delete
-- --  look at keeping records of deletes and keep data don't delete, keep 
-- --  keep info and  

-- CREATE TABLE images(
--     image_id SERIAL PRIMARY KEY,
--     image_url VARCHAR(300),
--     s_pen_id SERIAL REFERENCES stock_pens(s_pen_id),
-- );
-- -- file uploader for images

