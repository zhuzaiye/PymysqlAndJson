#! /usr/bin/env python
# coding:utf8

# built-in package
import pymysql
import time
import json

# third-party package

# custom package

"""
作者：hzzhu
目的：将数据进行重新规划填充
时间：2019/8/13
修改时间：2019/8/13
"""


# select 'id' from 'skillup_resource' and 'eiken_resource' tables to get data for inserting into 'school_resource_auth'
SelectTemplate_1 = '''SELECT id FROM {tb} ORDER BY id ASC;'''

# select 'branch_id' from 'branch_school' and 'branch_student' table
SelectBranch_student = '''SELECT b.id AS student_id, GROUP_CONCAT(a.branch_id) AS branch_id FROM branch_student AS a 
                          JOIN (SELECT id FROM students) AS b ON b.id=a.student_id GROUP BY b.id'''

SelectBranch_school = '''SELECT b.id AS school_id, GROUP_CONCAT(a.branch_id) AS branch_id FROM branch_school AS a 
                         JOIN (SELECT id FROM schools) AS b ON b.id=a.school_id GROUP BY b.id'''

SelectEiken_school =''''''

# 获得英检和技能训练的每个用户的资源
SelectTemplate_eiken = '''SELECT b.id AS student_id,GROUP_CONCAT(a.resource_id) AS resource_id 
                          FROM eiken_educard_resource AS a JOIN (SELECT a.id,b.card_id FROM students AS a 
                          JOIN student_cards AS b ON a.id=b.student_id) AS b ON a.card_id=b.card_id GROUP BY b.id'''

SelectTemplate_skillup = '''SELECT b.id AS student_id,GROUP_CONCAT(a.resource_id) AS resource_id 
                            FROM skillup_educard_resource AS a JOIN 
                            (SELECT a.id,b.card_id FROM students AS a JOIN student_cards AS b ON a.id=b.student_id) AS b
                            ON a.card_id=b.card_id GROUP BY b.id'''

# mysql insert commands
# SELECT student_id FROM student_resource_auth WHERE student_id=?
InsertTemplate_student_resource = '''INSERT INTO student_resource_auth (student_id, {field}) values(%s, %s);'''
UpdateTemplate_student_resource = '''UPDATE student_resource_auth SET {field}={value2} WHERE student_id={value1};'''
Insert_student_resource = '''INSERT INTO student_resource_auth (student_id, {field}) VALUES({v1}, {v2}) ON DUPLICATE KEY
                             UPDATE {field}={v2};'''

InsertTemplate_school_resource = '''INSERT INTO school_resource_auth (school_id, {field}) VALUES({v1}, {v2});'''
Insert_school_resouce = '''INSERT INTO student_resource_auth (school_id, {field}) VALUES({v1}, {v2}) ON DUPLICATE KEY
                             UPDATE {field}={v2};'''
Insert_school_branch = '''INSERT INTO school_resource_auth (school_id, {field}) VALUES({v1}, {v2}) ON DUPLICATE KEY
                             UPDATE {field}={v2};'''


# connect mysql database
host = ""
port = 
user = ""
password = ""
database = ""

DB = pymysql.connect(host=host, port=port, user=user, password=password, db=database, use_unicode=True, charset="utf8")


# 装饰器，计算插入数据所需的时间
def timer(func):
    def decor(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        d_time = end_time - start_time
        print("    the running time is: ", d_time)

    return decor


@timer
def insert_student():
    with DB.cursor() as cursor:
        sel_studentid_sql = SelectTemplate_1.format(tb="students")
        cursor.execute(sel_studentid_sql)
        student_id = cursor.fetchall()
        if student_id is None:
            raise ValueError("nothing!")
        else:
            pass
        # print(student_id)

        sel_eiken_sql = SelectTemplate_eiken
        cursor.execute(sel_eiken_sql)
        stuid_eiken = cursor.fetchall()
        if stuid_eiken is None:
            raise ValueError("nothing!")
        else:
            pass

        sel_skillup_sql = SelectTemplate_skillup
        cursor.execute(sel_skillup_sql)
        stuid_skillup = cursor.fetchall()
        if stuid_skillup is None:
            raise ValueError("nothing!")
        else:
            pass

        sel_branch_sql = SelectBranch_student
        cursor.execute(sel_branch_sql)
        stuid_branch = cursor.fetchall()
        if stuid_branch is None:
            raise ValueError("nothing!")
        else:
            pass

        eiken_values = []
        for eiken in stuid_eiken:
            eiken_values.append((eiken[0], json.dumps(sorted(list(map(int, eiken[1].split(",")))), separators=(',', ':'))))

        # print(eiken_values[:5])

        # # formation (1, '["1", "10", "100"])
        #

        skillup_resource = []
        for skillup in stuid_skillup:
            skillup_resource.append((skillup[0], json.dumps(sorted(list(map(int, skillup[1].split(",")))))))
        print(skillup_resource[:5])


        branch_resource = []
        for branch in stuid_branch:
            branch_resource.append((branch[0], json.dumps(sorted(list(map(int, branch[1].split(",")))))))
        # # print(branch_resource[:5])
        #
        insert_eiken_sql = InsertTemplate_student_resource.format(field="eiken_resource_ids")
        cursor.executemany(insert_eiken_sql, eiken_values)
        print("OK")

        for item in skillup_resource:
            insert_dic ={
                "field": "skillup_resource_ids",
                "v1": item[0],
                "v2": json.dumps(item[1], separators=(',', ':'))
            }
            insert_skillup_sql = Insert_student_resource.format(**insert_dic)
            # print(insert_skillup_sql)
            cursor.execute(insert_skillup_sql)
        print("OK")


        for item in branch_resource:
            insert_dic ={
                "field": "branch_ids",
                "v1": item[0],
                "v2": json.dumps(item[1], separators=(',', ':'))
            }
            insert_branch_sql = Insert_student_resource.format(**insert_dic)
            cursor.execute(insert_branch_sql)

        DB.commit()
        print("OK")



@timer
def insert_school():
    with DB.cursor() as cursor:
        sel_school_sql = SelectTemplate_1.format(tb="schools")
        cursor.execute(sel_school_sql)
        school_id = cursor.fetchall()
        if school_id is None:
            raise ValueError("nothing!")
        else:
            pass

        sel_branch_sql = SelectBranch_school
        cursor.execute(sel_branch_sql)
        school_branch = cursor.fetchall()
        if school_branch is None:
            raise ValueError("nothing!")
        else:
            pass

        # print(school_branch[:4])

        sel_eiken_sql = SelectTemplate_1.format(tb="eiken_resources")
        cursor.execute(sel_eiken_sql)
        eiken_id = cursor.fetchall()
        if eiken_id is None:
            raise ValueError("nothing")
        else:
            pass
        new_eiken = []
        for i in eiken_id:
            new_eiken.append(i[0])
        # print(new_eiken)

        sel_skillup_sql = SelectTemplate_1.format(tb="skillup_resources")
        cursor.execute(sel_skillup_sql)
        skillup_id = cursor.fetchall()
        if skillup_id is None:
            raise ValueError("nothing")
        else:
            pass
        new_skill = []
        for i in skillup_id:
            new_skill.append(i[0])
        # print(new_skill)

        for sid in school_id:
            insert_dic = {
                "field": "eiken_resource_ids",
                "v1": sid[0],
                "v2": json.dumps(json.dumps(new_eiken, separators=(',', ':')))
            }
            insert_eiken_sql = InsertTemplate_school_resource.format(**insert_dic)
            # print(insert_eiken_sql)
            cursor.execute(insert_eiken_sql)

            insert_dic1 = {
                "field": "skillup_resource_ids",
                "v1": sid[0],
                "v2": json.dumps(json.dumps(new_skill, separators=(',', ':')))
            }
            insert_skillup_sql = Insert_school_branch.format(**insert_dic1)
            cursor.execute(insert_skillup_sql)
        print("OK")

        # branch_resource = []
        # for branch in school_branch:
        #     branch_resource.append((branch[0], json.dumps(sorted(list(map(int, branch[1].split(",")))), separators=(',', ':'))))

        for item in school_branch:
            insert_dic2 = {
                "field": "branch_ids",
                "v1": item[0],
                "v2": json.dumps(json.dumps(sorted(list(map(int, item[1].split(",")))), separators=(',', ':')))
            }
            insert_branch_sql = Insert_school_branch.format(**insert_dic2)
            cursor.execute(insert_branch_sql)

        DB.commit()
        print("ok")


if __name__ == '__main__':
    insert_student()
    insert_school()

















