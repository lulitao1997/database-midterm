# database-midterm

## 页面声明

```

```

# 如何运行
1. 安装virtualenv
``` bash
    pip3 install virtualenv
    cd project_folder
    virtualenv venv
    source venv/bin/activate
```
2. 安装所有依赖
``` bash
    pip install -r requirments.txt
```
3. 建立数据库及随机生成数据
``` bash
    # 先开启mysql
    mysql -u root
    # 在另一个终端里
    python config.py
```

# todo

    教师信息页面 teacher-info-<tid> : teacher—info.html
        包括姓名，职称，email（email可以点击 "mailto:...." 链接）, 电话
        如果是教师登录的话，可以修改自己的email、电话 (DONE in 前端)

    教师管理页面：
    teacher-manage : teacher-manage.html

    已修课程页面显示总学分和GPA (DONE in 前端)

    考虑加一个显示排名的页面

    选课和退课课程页选课、退课成功后考虑加一个flash

    在每个页面顶栏上显示登陆者的名字(DONE, 在before_request里给g.username赋值即可)


    数据库中加入学生专业信息

    不能重修的情况（如时间被占用）

    数据库中课程加入教室属性

    想办法高效的计算可选课程总共有多少页

    Admin页面？？

    写Ubuntu里如何解决MySQL的编码问题


# 变量声明

变量声明都写在test.py里啦！

# 一些问题&解决方法

ubuntu下mysql修改成utf-8编码：

```
修改配置文件：
"sudo gedit /etc/mysql/my.cnf"
在配置文件中加入以下语句：
	[client]
    default-character-set=utf8

    [mysql]
    default-character-set=utf8

    [mysqld]
    init_connect='SET collation_connection = utf8_unicode_ci'
    init_connect='SET NAMES utf8'
    character-set-server=utf8
    collation-server=utf8_unicode_ci
    skip-character-set-client-handshake

然后重启mysql:
"/etc/init.d/mysql restart"
```
