--drop table if exists users;
create table if not exists users (
  id integer primary key autoincrement,
  user_key string not null
);
