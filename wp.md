### ER图：

![](/home/totoro/DataBase/database-midterm/pre/er图.png)



### 关系模式：

现在

teacher(**tno**, tname, sex, prof, email, tel, psw)

teacher(**编号**, 姓名, 性别, 职称, 邮箱, 手机, 密码)

course(**cno**, cname, credit, capacity, description text)

course(**编号**, 课程名, 学分, 容量, 描述)

course_time(*cno*, wnum, cnum)

course_time(*课程编号*，列号，行号)

student(**sno**, sname, sex, psw)

student(**学生编号**, 学生姓名, 性别, 密码)

teach_rel(*tno*, *cno*)

teach_rel(*老师编号*, *课程编号*)

performance(*sno*, *cno*, grade)

performance(*学生编号*, *课程编号*, 成绩)

userinfo(**id**, psw)

userinfo(**账号**, 密码)

-------------------------------------------------------------------------

历史

past_teach_rel(tno, cno, stime)

past_teach_rel(学生编号，课程编号，教学年份)

past_course_time(cno, wnum, cnum, stime)

past_course_time(课程编号, 列号, 行号, 年份)

past_performance(sno, cno, grade, stime)

past_performance(学生编号, 课程编号, 上课年份)



###  开发流程

![](/home/totoro/DataBase/database-midterm/pre/开发流程.png)

### 界面展示