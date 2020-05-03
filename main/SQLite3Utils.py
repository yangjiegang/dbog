#!/usr/bin/python
# -*- coding:utf-8 -*-
import sqlite3

import Params as params


# import Vars as mVars


#
# 连接数据库帮助类
# eg:
#   db = database()
#   count,listRes = db.executeQueryPage("select * from student where id=? and name like ? ", 2, 10, "id01", "%name%")
#   listRes = db.executeQuery("select * from student where id=? and name like ? ", "id01", "%name%")
#   db.execute("delete from student where id=? ", "id01")
#   count = db.getCount("select * from student ")
#   db.close()
#
class SQLite3Database(object):
    dbfile = params.db_params['db_file_path']
    # dbfile = mVars.db_memory
    # dbfile = "./db/manage.db"
    memory = params.db_params['db_memory_path']
    conn = None
    showsql = False

    def __init__(self, dbfile=params.db_params['db_file_path'], memory=params.db_params['db_memory_path'],
                 showsql=True):
        self.dbfile = dbfile
        self.memory = memory
        self.showsql = showsql
        self.conn = self.getConn()
        self.cur = self.conn.cursor()

    # 输出工具
    def out(self, outStr, *args):
        if (self.showsql):
            for var in args:
                if (var):
                    outStr = outStr + ", " + str(var)
            print("db. " + outStr)
        return

    # 获取连接
    def getConn(self):
        if (self.conn is None):
            conn = sqlite3.connect(self.dbfile, check_same_thread=False, timeout=20)
            if (conn is None):
                conn = sqlite3.connect(self.memory, check_same_thread=False)
            if (conn is None):
                print("dbfile : " + self.dbfile + " is not found && the memory connect error ! ")
            else:
                conn.row_factory = self.dict_factory  # 字典解决方案
                self.conn = conn
            # self.out("db init conn ok ! ")
        else:
            conn = self.conn

        return conn

    # 字典解决方案
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    # 关闭连接
    def close(self, conn=None):
        res = 2
        if (not conn is None):
            self.cur and self.cur.close()
            conn.close()
            res = res - 1
        if (not self.conn is None):
            self.cur and self.cur.close()
            self.conn.close()
            res = res - 1
        # self.out("db close res : " + str(res))
        return res

    # 加工参数tuple or list 获取合理参数list
    # 把动态参数集合tuple转为list 并把单独的传递动态参数list从tuple中取出作为参数
    def turnArray(self, args):
        # args (1, 2, 3) 直接调用型 exe("select x x", 1, 2, 3)
        # return [1, 2, 3] <- list(args)
        # args ([1, 2, 3], ) list传入型 exe("select x x",[ 1, 2, 3]) len(args)=1 && type(args[0])=list
        # return [1, 2, 3]
        if (args and len(args) == 1 and (type(args[0]) is list)):
            res = args[0]
        else:
            res = list(args)
        return res

    # 分页查询 查询page页 每页num条 返回 分页前总条数 和 当前页的数据列表 count,listR = db.executeQueryPage("select x x",1,10,(args))
    def executeQueryPage(self, sql, page, num, *args):
        args = self.turnArray(args)
        count = self.getCount(sql, args)
        # pageSql = "select * from ( " + sql + " ) limit 5 offset 0 "
        pageSql = "SELECT * FROM ( " + sql + " ) LIMIT 5 OFFSET 0 "
        # args.append(num)
        # args.append(int(num) * (int(page) - 1) )
        # self.out(pageSql, args)
        conn = self.getConn()
        cursor = conn.cursor()
        listRes = cursor.execute(sql, args).fetchall()
        return (count, listRes)
        # 查询列表array[map] eg: [{'id': u'id02', 'birth': u'birth01', 'name': u'name02'}, {'id': u'id03', 'birth': u'birth01', 'name': u'name03'}]

    def executeQuery(self, sql, *args):
        args = self.turnArray(args)
        # self.out(sql, args)
        conn = self.getConn()
        cursor = conn.cursor()
        res = cursor.execute(sql, args).fetchall()
        return res
        # 执行sql或者查询列表 并提交

    def execute(self, sql, *args):
        args = self.turnArray(args)
        # self.out(sql, args)
        conn = self.getConn()
        cursor = conn.cursor()
        # sql占位符 填充args 可以是tuple(1, 2)(动态参数数组) 也可以是list[1, 2] list(tuple) tuple(list)
        res = cursor.execute(sql, args).fetchall()
        conn.commit()
        cursor.close()
        # self.close(conn)
        return res
        # 查询列名列表array[str]  eg: ['id', 'name', 'birth']

    def getColumnNames(self, sql, *args):
        args = self.turnArray(args)
        # self.out(sql, args)

        conn = self.getConn()
        if (not conn is None):
            cursor = conn.cursor()
            cursor.execute(sql, args)
            res = [tuple[0] for tuple in cursor.description]
        return res
        # 查询结果为单str eg: 'xxxx'

    def getString(self, sql, *args):
        args = self.turnArray(args)
        # self.out(sql, args)

        conn = self.getConn()
        cursor = conn.cursor()
        listRes = cursor.execute(sql, args).fetchall()
        columnNames = [tuple[0] for tuple in cursor.description]
        # print(columnNames)
        res = ""
        if (listRes and len(listRes) >= 1):
            res = listRes[0][columnNames[0]]
        return res
        # 查询记录数量 自动附加count(*) eg: 3

    def getCount(self, sql, *args):
        args = self.turnArray(args)
        sql = "SELECT count(*) cc FROM ( " + sql + " ) "
        resString = self.getString(sql, args)
        res = 0
        if (resString):
            res = int(resString)
        return res

    def export2csv(self, tbl_name):
        cols = self.getColumnNames("select * from %s" % tbl_name)
        data = self.executeQuery("select * from %s" % tbl_name)
        from CsvUtil import CsvHandler as CSVer
        csvHd = CSVer(cols)
        writer = csvHd.createWriter(tbl_name)
        for dat_dict in list(data):
            value_list = dict(dat_dict).values()
            csvHd.wrtCsv(writer, list(value_list))
        return csvHd.csvPath

    def get_data_rows(self, tbl_name):
        # cols = self.getColumnNames("select * from %s" % tbl_name)
        data_rows = []
        if tbl_name:
            data_rows = self.executeQuery("select * from %s" % tbl_name)
        return data_rows
        # from CsvUtil import CsvHandler as CSVer
        # csvHd = CSVer(cols)
        # writer = csvHd.createWriter(tbl_name)
        # for dat_dict in list(data):
        #     value_list = dict(dat_dict).values()
        #     csvHd.wrtCsv(writer, list(value_list))
        # return csvHd.csvPath

    def get_specific_rows(self, row_name, tbl_name):
        data_rows = []
        if tbl_name:
            data_rows = self.executeQuery("select %s from %s" % (row_name, tbl_name))
        return data_rows
        # from CsvUtil import CsvHandler as CSVer
        # csvHd = CSVer(cols)
        # writer = csvHd.createWriter(tbl_name)
        # for dat_dict in list(data):
        #     value_list = dict(dat_dict).values()
        #     csvHd.wrtCsv(writer, list(value_list))
        # return csvHd.csvPath

####################################测试
# def main():
#     db = SQLite3Database()
#     # db.execute(
#     #     '''
#     #     create table if not exists student(
#     #         id      text primary key,
#     #         name    text not null,
#     #         birth   text
#     #     )
#     #     '''
#     # )
#     # for i in range(10):
#     #     db.execute("insert into student values('id1" + str(i) + "', 'name1" + str(i) + "', 'birth1" + str(i) + "')")
#     # db.execute("insert into student values('id01', 'name01', 'birth01')")
#     # db.execute("insert into student values('id02', 'name02', 'birth01')")
#     # db.execute("insert into student values('id03', 'name03', 'birth01')")
#
#     # print(db.getColumnNames("select * from student"))
#     # print(db.getColumnNames("select * from tbl_shop_data"))
#     tbl_name = 'tbl_shop_data'
#     db.export2CSV(tbl_name)
#     print("done")
#
#     # print(db.getString("select name from student where id = ? ", "id02"))
#
#     # print(db.executeQuery("select * from student where 1=? and 2=? ", 1, 2))
#     # print(db.executeQueryPage("select * from student where id like ? ", 1, 5, "id0%"))
#     # db.execute("update  student set name='nameupdate' where id = ? ", "id02")
#     # db.execute("delete from student where id = ? or 1=1 ", "id01")
#     # db.execute("delete from student where id = ? or 1=1 ", "id01")
#
#     db.close()


# if __name__ == '__main__':
#     main()

# -*- coding: UTF-8 -*-
# import os
# ret = messagebox.askyesno(title='导出文件成功', message="文件地址：11")
# file = 'E:/workspace_me10/manage_num/csv/tbl_vip_info_1529827541_5816212.csv'
# if  (ret):
#     os.startfile(file)
# path = 'E:\workspace_me10\manage_num'
# os.startfile(path)
# import win32api
# path = 'C:/Documents and Settings/liushen/Application Data/Macromedia/Flash Player/#SharedObjects'
# win32api.ShellExecute(0, 'open', path, '', '', 1)
