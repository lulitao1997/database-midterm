drop database if exists edu_manage;
create database edu_manage;
use edu_manage;

create table teacher (
    tno     char(5)     not null, -- like 01898
    tname   char(30)    not null,
    sex     char(1),
    prof    char(10), -- job title
    psw     char(40), -- sha-1
    primary key(tno)
);

create table course (
    cno         char(13)    not null, -- like ECON130005.01
    cname       char(30)    not null,
    credit      smallint    not null,
    capacity    smallint    not null,
    -- ctime       char(10)    not null,
    description text,
    primary key(cno)
);

create table course_time (
    cno     char(13)    not null,
    -- wcnt    smallint    not null, -- week count
    wnum    smallint    not null, -- 1~7, Monday~Sunday
    cnum    smallint    not null, -- course count 1~14
    foreign key(cno) references course(cno)
);

create table student (
    sno     char(11)    not null, -- like 15307130084
    sname   char(30)    not null,
    sex     char(1),
    psw     char(40), -- sha-1
    primary key(sno)
);

create table teach_rel (
    tno     char(5)     not null,
    cno     char(13)    not null,
    foreign key(tno) references teacher(tno),
    foreign key(cno) references course(cno)
);

create table performance (
    sno     char(11)    not null,
    cno     char(13)    not null,
    grade   decimal(4,1),
    foreign key(sno) references student(sno),
    foreign key(cno) references course(cno)
);
