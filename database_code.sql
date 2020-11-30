-- create table users(
-- 	userId int auto_increment primary key,
--     userName varchar(30) unique not null,
--     password varchar(30),
--     firstName varchar(30),
--     lastName varchar(30),
--     age int,
--     email varchar(30)
-- )

-- create table listOfConversation(
-- 	chatId int auto_increment primary key,
--     userName1 varchar(30),
--     userName2 varchar(30),
--     foreign key(userName1) references users(userName),
--     foreign key(userName2) references users(userName)
-- )

-- insert into listOfConversation(userName1,userName2)
-- values ("ken","ken1"),("ken1","ken")

-- delete from listOfConversation where chatId=2

-- CREATE TABLE `5` (
-- messageId int auto_increment primary key, 
-- sender varchar(30), 
-- content varchar(400), 
-- sent_at datetime,status varchar(30),
-- foreign key(sender) references users(userName)

-- );
