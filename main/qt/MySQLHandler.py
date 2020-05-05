import pymysql

import main.qt.Vars as mVars
from main.qt.SQLParser import SQLParser
from main.qt.Tools import CTools, cTool


# database util
class MyDBHandler:
    cursor = None  # 句柄
    db = None  # 打开数据库连接
    '''
        定义构造方法
        host：主机名
        username;用户名
        password:密码
        dbname:数据库名
        db:打开数据库连接
        cursor:获取游标句柄
    '''

    # initailize
    def __init__(self):
        self.sqlParser = SQLParser()
        CTools.readConfig(None)
        self.host = mVars.host
        self.username = mVars.username
        self.password = mVars.password
        self.db_name = mVars.database_name
        self.table_name_lst = ""
        self.is_combine_sql = ""
        self.def_table_name = ""
        self.def_pk_name = ""
        self.def_pk_index = 0
        self.delete_sql = ""
        self.def_field_name_lst = []

    # change config
    def config(self, host, username, password, db_name):
        self.host = host if host else self.host
        self.username = username if username else self.username
        self.password = password if password else self.password
        self.db_name = db_name if db_name else self.db_name
        self.db = pymysql.connect(self.host, self.username, self.password, self.db_name)
        self.cursor = self.db.cursor()

    # 获取所有的结果集
    def get_all_result(self, sql_str):
        self.cursor.execute(sql_str)
        results = self.cursor.fetchall()
        # 判断是否有表名
        if "from" in sql_str:
            self.table_name_lst = self.sqlParser.extract_table_name_from_sql(sql_str)
            self.def_table_name = list(self.table_name_lst)[0]
            self.is_combine_sql = (len(self.table_name_lst) > 1)
        return results

    # 获取主键序号
    def gen_def_pk_index(self):
        self.def_field_name_lst = []
        for i in range(0, len(self.cursor.description)):
            field_desc = self.cursor.description[i]
            field_name = field_desc[0]
            self.def_field_name_lst.append(field_name)
            if self.def_pk_name == field_name:
                self.def_pk_index = i
                break

    # 获取字段名列表
    def gen_filed_name_list(self):
        # generate table description
        self.gen_alter(self.def_table_name)
        # generate table field names
        self.def_field_name_lst = []
        # tmp_pk_index = 0
        # for field_desc in self.cursor.description:
        for field_desc in self.table_desc_list:
            self.def_field_name_lst.append(field_desc['Field'])
        return self.def_field_name_lst

    # 获取所有的结果集
    def get_all_result_count(self, sql_str):
        # 判斷是否有表名
        if "from" in sql_str:
            self.table_name_lst = self.sqlParser.extract_table_name_from_sql(sql_str)
            self.is_combine_sql = (len(self.table_name_lst) > 1)
            self.def_table_name = list(self.table_name_lst)[0]
        self.cursor.execute(sql_str)
        results = self.cursor.fetchall()
        return results

    # 获取所有的结果集
    def get_single_result(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchone()
        return results

    # 插入或更新数据 TODO field type should not had been ignored
    def modifyRecords(self, sql):
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except Exception as e:
            cTool.logger.error(e)
            # 发生错误时回滚
            self.db.rollback()
        # 返回受影响的行数
        return self.cursor.rowcount

    # generate description of table
    def gen_alter(self, table_name):
        sql_list = 'desc %s;' % table_name
        self.cursor.execute(sql_list)
        result_sets = self.cursor.fetchall()
        self.table_desc_list = [
            {
                'Field': ret[0],
                'Type': ret[1],
                'Null': ret[2],
                'Key': ret[3],
                'Default': ret[4]
            } for ret in result_sets
        ]
        # take the first PK field
        tmp_pk_index = 0
        self.def_pk_name = \
            dict(list(filter(lambda field_desc_dict: self.is_pk(field_desc_dict, tmp_pk_index), self.table_desc_list))[
                     0])[
                "Field"]
        # 定位主键序号
        # self.gen_def_pk_index()
        sql_list = 'show table status where NAME="%s";' % table_name
        self.cursor.execute(sql_list)
        result_sets = self.cursor.fetchall()
        table_comment = result_sets[0][-1]
        [item.update(TableComment=table_comment) for item in self.table_desc_list]
        sql_list = 'show full columns from %s;' % table_name
        self.cursor.execute(sql_list)
        result_sets = self.cursor.fetchall()
        for item in self.table_desc_list:
            for ret in result_sets:
                if item['Field'] == ret[0]:
                    item['Extra'] = ret[-1]
                    break
        # self.def_field_name_lst = [db_filed["Field"] for db_filed in table_desc_list]
        return self.table_desc_list

    # get index of PK from field list
    def is_pk(self, field_desc_dict, tmp_pk_index):
        if field_desc_dict["Key"] == "PRI":
            self.def_pk_index = tmp_pk_index
            return True
        else:
            tmp_pk_index += 1

    # generate description of table
    def descTable(self, table_name):
        sqllist = '''
                select aa.COLUMN_NAME,
                aa.DATA_TYPE,aa.COLUMN_COMMENT, cc.TABLE_COMMENT 
                from information_schema.`COLUMNS` aa LEFT JOIN 
                (select DISTINCT bb.TABLE_SCHEMA,bb.TABLE_NAME,bb.TABLE_COMMENT 
                from information_schema.`TABLES` bb ) cc  
                ON (aa.TABLE_SCHEMA=cc.TABLE_SCHEMA and aa.TABLE_NAME = cc.TABLE_NAME )
                where aa.TABLE_SCHEMA = '%s' and aa.TABLE_NAME = '%s';
                ''' % (self.db_name, table_name)
        self.cursor.execute(sqllist)
        result = self.cursor.fetchall()
        td = [
            {
                'Field': ret[0],
                'Type': ret[1],
                'Extra': ret[2],
                'TableComment': ret[3]
            } for ret in result
        ]
        return td

    # generate update SQL
    def buildUpdateSQL(self, tblName, fdNameLst, vertirxData, oldData):
        updStr = ""
        whereStr = ""
        batchSqlStr = ""
        updItemStr = ""
        whereItemStr = ""
        singleSqlStr = ""
        for ret in range(0, len(vertirxData)):
            rowData = vertirxData[ret]
            for j in range(0, len(rowData)):
                cellData = vertirxData[ret][j]
                updItemStr = fdNameLst[j] + "=" + cellData[j] + ","
                whereItemStr = fdNameLst[j] + "=" + oldData[ret, j] + " AND "
            updStr += updItemStr[:-1]
            whereStr += whereItemStr[:-1]
            singleSqlStr = "UPDATE %s SET (%s) WHERE (%s);" % (tblName, updStr, whereStr)
        batchSqlStr += singleSqlStr
        return batchSqlStr

    # generate insert SQL
    def buildInsertSQL(self, tblName, vertirxData):
        valStr = ""
        for row in vertirxData:
            valStr += "(%s)," % (",".join(["\"%s\"" % item for item in row]))
        valStr = valStr[:-1]
        if len(vertirxData) > 1:
            valStr = "(%s)" % valStr
        return "INSERT INTO %s VALUES %s" % (tblName, valStr)

    # generate delete SQL
    def buildDeleteSQL(self, tblName, fdName, dataLst):
        return "DELETE FROM %s WHERE %s IN (%s);" % (tblName, fdName, ",".join(["\"%s\"" % item for item in dataLst]))

    # 关闭链接
    def close(self):
        self.db.close()
