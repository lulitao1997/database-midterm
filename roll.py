ROLL_SQL = """
insert into past_course(cno,cname,credit,capacity,description) select * from course;
insert into past_course_time(cno,wnum,cnum) select * from course_time;
insert into past_performance(sno,cno,grade) select * from performance;
insert into past_teach_rel(tno,cno) select * from teach_rel;
update past_course set stime=%s where stime is NULL;
update past_course_time set stime=%s where stime is NULL;
update past_performance set stime=%s where stime is NULL;
update past_teach_rel set stime=%s where stime is NULL;
delete from course_time;
delete from teach_rel;
delete from performance;
delete from course;
"""
from config import *
def roll(db, semester):
    with db.cursor() as c:
        try:
            c.execute(ROLL_SQL, [semester]*4)
            c.execute("use edu_manage",[])
            # db.commit()
            gen_data(c, True)
            db.commit()
        except:
            db.rollback()
            return -1
    return 0
