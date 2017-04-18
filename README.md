# database-midterm

## 页面声明

```
/ : {
    welcome.html    
}

/please_login : {
    please_login.html
}

/login : {
	login.html
}
/dashboard/curriculum : {
  	dashboard-curriculum.html
}
/dashboard/list : {
  	dashboard-list.html
}
/courseinfo : {
  	courseinfo.html
}
/teacherinfo : {
  	teacherinfo.html
}
/studentinfo : {
  	studentinfo.html
}
/info/success : {
  	info-success.html
}
/info/fail : {
  	info-fail.html
}
```



# todo

email 改成 username
wecolme.html 中点击登录按钮后会出现Method Not Allowed错误


# dashboard

学生：

​	课表(可选课程和已选课程都要显示课表，选中课程课表对应区高亮) {

​		如果已选：显示重修 否则显示选课

​	}

​	成绩查询

​	课程信息 {

​	}

老师

​	课表

​	课程信息 { 课程描述，花名册(包括给分)。}

# 变量声明

```
dashboard-coursesavailable.html {
	后端传给前端：
	pagenumber: 已选课程列表中的当前页码
	pageamount: 已选课程列表中的页面数
	course: 当前页面应该显示出的课程，list类型或set类型 {
      	内部元素为dict类型
      	dict{
      		'cid': 类似于cno，但是不能有'.'，例如1345.01要写成'1234501'
      		'cells': list类型或set类型，存储占据的课程格子，格式:'1-3'表示星期一的第三节课
      		'info': tuple(元组)类型(list类型应该也可以?0..0),格式：(cno, cname, tname, 				credit, capacity)
      	}
	}
	cnameincell: 二维list,cnameincell[i][j]表示课程表第i天第j节课的课程名。

	前端传给后端：
	select：如果存在，返回试图选课的cid
	search：如果存在，返回cname, cno, tname
	turnpage：如果存在，返回'next'或'past'或试图turn到的页码
}
```
