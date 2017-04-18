@tid-- 以下均不考虑重修情况

-- Student
-- set @sid='15307100008';
-- 获得@sid已经选过的所有课程
select * from performance where sno=@sid;

-- 获得@sid的平均分,总学分
select AVG(grade), SUM(credit) from performance natural join course
where sno=@sid and grade is not NULL
group by sno;

-- 获得全部学生的成绩表
@rank_table=(
select * from (
    select @rank:=@rank+1 as rnk, A.*
    from (
        select sno, avg(grade) as avg_grade, sum(credit) as tot_credit
        from performance natural join course
        where grade is not NULL
        group by sno
        order by avg_grade desc
    ) A, (select @rank:=0) B
) M
order by rnk);

-- 获得id选过的所有时间
select wnum, cnum from performance natural join course_time
where sno=@sid;

-- 获得@cid占用的所有时间
select wnum, cnum from course_time where cno=@cid

-- 获得@sid已经有课的所有时间
select wnum, cnum from course_time natural join performance
where sno=@sid;

-- 获得@sid可以选择的所有课程(不包括重修的)
select * from course
where cno not in (
    select cno from performance where sno=@sid
) and not exists (
    select * from course_time A, course_time B, performance C
    where (A.wnum,A.cnum)=(B.wnum,B.cnum) and B.cno=C.cno and A.cno=course.cno and C.sno=@sid
);

-- Teacher
-- set @tid='09236';
-- set @cid='LAWS130775.01';
-- 获得@tid教授的所有课程
select * from teach_rel where tno=@tid;

-- 获得上@cid课的所有学生
select * from performance where cno=@cid;

-- 获得被@tid教授的所有学生
select distinct * from student natural join performance natural join teach_rel
where tno=@tid
order by cno;

#include <iostream>
using namespace std;
int main() {
    int a,b;
    cin>>a>>b;
    cout<<a+b<<endl;
}
