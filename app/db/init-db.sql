-- Insert data into reading.
INSERT INTO reading (name, creation_time, text,BG_passage_reference)
VALUES ('Reading for Moday', 1300 , 'this is the text','1 Corinthians 13:4-5');

INSERT INTO reading (name, creation_time, text,BG_passage_reference)
VALUES ('Reading for Tuesday', 1100 , 'this is the text','2 Corinthians 13:4-5');

-- Insert data into content.
INSERT INTO content (author_id, content_type, name, creation_time, approved,content)
VALUES (1, 1, 'Moday Content', 1300 , "TRUE" ,'LOTS OF CONTENT HERE');

INSERT INTO content (author_id, content_type, name, creation_time, approved,content)
VALUES (1, 1, 'Tuesday Content', 1400 , "TRUE" ,'TUESDAY CONTENT HERE');


-- Insert data into reading_content.
INSERT INTO reading_content(reading_id,content_id)
VALUES (1,1);

INSERT INTO reading_content(reading_id,content_id)
VALUES (2,2);

INSERT INTO reading_content(reading_id,content_id)
VALUES (1,2);

-- Insert data into content_type.
INSERT INTO content_type(name)
VALUES ('Scripture');

-- Insert data into user.
INSERT INTO user(username,password,email_address,first_name,last_name,active)
VALUES ('usernameone','orange43','cse243@gmail.com','Joe','King',"DEFAULT" );

-- Insert data into group.
INSERT INTO group (name, public,creation_time,description)
VALUES ('Orange Group',"TRUE", 1300, 'The best group ever!');

-- Insert data into group_invitation.
INSERT INTO group_invitation(user_id,group_id,creation_time)
VALUES (1,1,1300 );

-- Insert data into plan.
INSERT INTO plans(author_id_fk, name, creation_time, discription)
VALUES(1,'plan1',1300,'content for plan 1 entered here.');

-- Insert data into plan_reading.
INSERT INTO plan_reading (plans_id, reading_id, start_time_offset, start_time_offset)
VALUES (1,1,1300,1300);

-- Insert data into Subscription.
INSERT INTO subscription (plans_id, user_id, creation_time)
VALUES (1,1,1300);

-- Insert data into Group Subscription.
INSERT INTO group_subscription (plans_id, group_id, creation_time)
VALUES (1,1,1300);

-- Insert data into Feedback.
INSERT INTO feedback (author_id_fk, plan_id_fk, content_id_fk, reading_id_fk, comment, creation_time)
VALUES (1,1,1,1, 'feedback test 1.', "TIMESTAMP");