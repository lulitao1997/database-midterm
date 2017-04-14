# -*- coding: utf-8 -*-
from random import choice, randint, sample
from random_words import *
import pymysql
import string

rw = RandomWords()
db = pymysql.connect(host='localhost', port=3306, password="", user='root', database='edu_manage', charset='utf8')

last_name = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
'何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
'云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
'酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
'乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
'姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
'熊', '纪', '舒', '屈', '项', '祝', '董', '梁']

first_name = ['晨', '辰', '士', '以', '建', '家', '致', '树', '炎', '德', '行', '时', '泰', '盛', '雄', '琛', '钧', '冠', '策',
'腾', '伟', '刚', '勇', '毅', '俊', '峰', '强', '军', '平', '保', '东', '文', '辉', '力', '明', '永', '健', '世', '广', '志',
 '义', '兴', '良', '海', '山', '仁', '波', '宁', '贵', '福', '生', '龙', '元', '全', '国', '胜', '学', '祥', '才', '发', '成',
  '康', '星', '冰', '爽', '琬', '茗', '羽', '希', '宁', '欣', '飘', '育', '滢', '馥', '筠', '柔', '竹', '霭', '凝', '晓', '欢',
  '霄', '枫', '芸', '菲', '寒', '伊', '亚', '宜', '可', '姬', '舒', '影', '荔']

def rand_name():
    s = choice(last_name) + choice(first_name)
    if randint(0,1)==1:
        s = s + choice(first_name)
    return s

def rand_str(N, all_num = False):
    return ''.join(choice(string.digits + ('' if all_num else string.ascii_letters)) for _ in range(N))
def rand_ns(N):
    return rand_str(N, True)

tno_s = set()
def rand_tno():
    global tno_s
    n = '0'+rand_ns(4)
    while n in tno_s:
        n = '0' + rand_ns(4)
    tno_s.add(n)
    return n

def rand_teacher():
    return (rand_tno(), rand_name(), choice(['M','F']), choice(['Professor', 'Lecturer']), rand_str(8))

major_n = ['713', '710']
scnt = dict()
sno_s = set()
def rand_sno():
    global major_cnt, sno_s
    pre = str(randint(13,16)) + '30' + choice(major_n)
    if pre not in scnt:
        scnt[pre] = 1
    else:
        scnt[pre] += 1
    sno = pre + str(scnt[pre]).rjust(4,'0')
    sno_s.add(sno)
    return sno

def rand_stu():
    return (rand_sno(), rand_name(), choice(['M','F']), rand_str(8))

course_code = ['COMP', 'PEDU', 'INFO', 'LAWS']
ccnt = dict()
cno_s = set()
def rand_cno():
    global ccnt, cno_s
    pre = choice(course_code) + '130' + rand_ns(3)
    if pre not in ccnt:
        ccnt[pre] = 1
    else:
        ccnt[pre] += 1
    cno = pre + '.' + str(ccnt[pre]).rjust(2,'0')
    cno_s.add(cno)
    return cno

def rand_cname(cap = True, cnt = 2):
    l = rw.random_words(count=cnt)
    return ' '.join(map(str.capitalize, l) if cap else l)

def rand_course():
    return (rand_cno(), rand_cname(), randint(3,5), 5*randint(4,25), rand_cname(False, randint(10,20)))

def rand_teach_rel():
    return (choice(list(tno_s)), choice(list(cno_s)))

def rand_performance():
    return(choice(list(sno_s)), choice(list(cno_s)), randint(0,1000)/10)

def gen_ctime(cno):
    ctime_l = list()
    days = sample(range(1,8), randint(1,3));
    for i in days:
        l = randint(1,3)
        st = randint(1,15-l)
        for j in range(st, st+l):
            ctime_l.append((cno, i, j))
    return ctime_l

def gen_sql(table, L):
    cmd = 'INSERT INTO ' + table + ' VALUES'
    for i in L:
        cmd += '\n'+str(i)+','
    return cmd[:-1]+';'

if __name__ == '__main__':
    stu_l = [rand_stu() for i in range(100)]
    course_l = [rand_course() for i in range(15)]
    teacher_l = [rand_teacher() for i in range(20)]
    performance_l = [rand_performance() for i in range(200)]
    teach_rel_l = [rand_teach_rel() for i in range(20)]
    ctime_l = list()
    for i in course_l:
        for j in gen_ctime(i[0]):
            ctime_l.append(j)
    # print(gen_sql('teach_rel', teach_rel_l))
    try:
        cursor = db.cursor()
        cursor.execute(gen_sql('student', stu_l))
        cursor.execute(gen_sql('course', course_l))
        cursor.execute(gen_sql('teacher', teacher_l))
        cursor.execute(gen_sql('performance', performance_l))
        cursor.execute(gen_sql('teach_rel', teach_rel_l))
        cursor.execute(gen_sql('course_time', ctime_l))
        db.commit()
    except:
        db.rollback()
