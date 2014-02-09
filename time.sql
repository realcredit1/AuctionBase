drop table if exists Time;
create table Time(currtime string PRIMARY KEY);
insert into Time values ('2001-12-20 00:00:01');
select currtime from Time;