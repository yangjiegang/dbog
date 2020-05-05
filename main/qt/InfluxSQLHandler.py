from influxdb import InfluxDBClient

import main.qt.Vars as mVars
from main.qt.Tools import cTool


# database util
class InfluxSQLHandler:

    # initialize
    def __init__(self):
        # self.sqlParser = SQLParser()
        self.field_lst = []
        self.def_pk_index = 0
        self.def_pk_name = "id"
        self.table_name_lst = []
        self.def_table_name = ""
        self.is_combine_sql = False
        self.tag_name_lst = []
        self.field_name_lst = []
        # self.row_count = 0
        # CTools.readConfig(None)
        self.host = mVars.host
        self.port = mVars.port
        self.username = mVars.username
        self.password = mVars.password
        self.db_name = mVars.database_name
        # variable
        self.delete_sql = ""
        self.table_data = []
        # 初始化
        self.client = InfluxDBClient(self.host, self.port, self.username, self.password, self.db_name)

    # change config
    def re_config(self, host, port, username, password, db_name):
        self.host = host if host else self.host
        self.port = port if host else self.host
        self.username = username if username else self.username
        self.password = password if password else self.password
        self.db_name = db_name if db_name else self.db_name
        # 初始化
        self.client = InfluxDBClient(self.host, self.port, self.username, self.password, self.db_name)

    def get_measurements(self):
        results = []
        try:
            ret = self.client.query("show measurements")
            tb_name_lst = ret.raw['series'][0]["values"]
            results = [tb_name[0] for tb_name in tb_name_lst]
        except Exception as e:
            cTool.logger.error(e)
        return results

    # query results only one sentence
    def get_all_result(self, sql_str):
        sql_str = sql_str.replace(";", "")
        results = []
        try:
            ret = self.client.query(sql_str)
            series_lst = ret.raw['series']
            series = series_lst[0]
            results = series["values"]
            self.field_name_lst = series["columns"]
            self.def_pk_index = list(series["columns"]).index(self.def_pk_name)
            # self.row_count = len(results)
        except Exception as e:
            cTool.logger.error(e)
        # 判断是否有表名 do not change the case of SQL
        self.build_main_sql(sql_str)
        # extra option
        # self.get_field_name_lst()
        self.get_tag_name_lst()
        return results

    def build_main_sql(self, sql_str):
        keyword = ""
        if "limit" in sql_str:
            keyword = "limit"
        elif "LIMIT" in sql_str:
            keyword = "LIMIT"
        if keyword:
            sql_str = str(sql_str.split(keyword)[0]).strip()
        # 判断是否有表名 do not change the case of SQL
        if "where" in sql_str:
            keyword = "where"
        elif "WHERE" in sql_str:
            keyword = "WHERE"
        if keyword:
            sql_str = (sql_str.split(keyword)[0]).strip()
        # from sub sentence
        if "from" in sql_str:
            keyword = "from"
        elif "FROM" in sql_str:
            keyword = "FROM"
        if keyword:
            self.table_name_lst = sql_str.split(keyword)[1].split(",")
            self.def_table_name = str(self.table_name_lst[0]).strip()
            self.is_combine_sql = len(self.table_name_lst) > 1

    # 获取字段名列表
    def get_name_lst(self, sql_str):
        ret = self.client.query(sql_str)
        series_lst = ret.raw['series']
        series = series_lst[0]
        field_lst = series["values"]
        self.field_name_lst.clear()
        self.field_name_lst.append("time")
        self.get_tag_name_lst()
        self.field_lst.clear()
        try:
            for field in field_lst:
                self.field_name_lst.append(field[0])
                self.field_lst.append(
                    {
                        series["columns"][0]: field[0],
                        series["columns"][1]: field[1]
                    }
                )
        except Exception as e:
            cTool.logger.error(e)
        return self.field_name_lst

    # 获取字段名列表
    def get_tag_name_lst(self):
        ret = self.client.query("show tag keys from %s" % self.def_table_name)
        series_lst = ret.raw['series']
        series = series_lst[0]
        tag_lst = series["values"]
        self.tag_name_lst = [item[0] for item in tag_lst]
        return self.tag_name_lst

    # 获取字段名列表
    def get_field_name_lst(self):
        return self.get_name_lst("show field keys from %s" % self.def_table_name)

    # 获取字段名列表
    def get_page_count(self, cmd_str: str) -> int:
        cnt_sql = "select count(%s) from %s" % (self.field_name_lst[-1], cmd_str)
        ret = self.client.query(cnt_sql)
        series_lst = ret.raw['series']
        series = series_lst[0]
        # [time, count]
        ret_cnt = series["values"][0][1]
        page_cnt = int(ret_cnt / 10)
        if page_cnt % 10 != 0:
            page_cnt = page_cnt + 1
        return page_cnt

    # 插入或更新数据
    def insert_record(self, dict_list: list):
        json_body = []
        for dict_data in dict_list:
            json_body.append(
                {
                    "measurement": self.def_table_name,
                    "tags": {k: v for k, v in dict_data.items() if k in self.tag_name_lst},
                    "time": dict_data["time"],
                    "fields": {k: v for k, v in dict_data.items() if k not in self.tag_name_lst}
                }
            )
        try:
            # 执行SQL语句
            self.client.write_points(json_body)
        except Exception as e:
            cTool.logger.error(e)

    # remove record
    def remove_record(self, sql):
        try:
            self.client.query(sql)
        except Exception as e:
            cTool.logger.error(e)

    # generate insert SQL
    def build_insert_data(self, matrix_data):
        dict_lst = []
        for i in range(0, len(matrix_data)):
            data_lst = matrix_data[i]
            dict_data = {}
            for j in range(0, len(data_lst)):
                dict_data.update({
                    self.field_name_lst[j]: data_lst[j]
                })
            dict_lst.append(dict_data)
        return dict_lst

    # generate delete SQL
    def build_delete_sql(self, value):
        return "DELETE FROM %s WHERE %s = '%s'" % (self.def_table_name, self.def_pk_name, value)

    # 关闭链接
    def close(self):
        self.client.close()

# db = InfluxDBHandler()
# print(db.get_all_result("select * from tb_user"))
# print(db.get_field_name_lst())
# print(db.get_tag_name_lst())


# db = InfluxSQLHandler()


# def test():
# print(db.get_all_result("select * from tb_user"))
# print(db.get_field_name_list())
# result_lst = db.get_all_result("select * from tb_user where id = '%s'" % '1234')
# results = []
# for i in range(0, len(result_lst)):
#     obj = {}
#     row = result_lst[i]
#     for j in range(0, len(row)):
#         val = row[j]
#         key = db.field_name_lst[j]
#         obj[key] = val
#     results.append(obj)
# print(results)
# # results[1]["climateId"] = "123"
# results[0]["id"] = "12345"
# db.modify_records(results[0])
# db.remove_records("delete from t_user where id = '%s'" % "3ae10a42a69549088115e6242409506b")
# print(db.get_measurements())
# db.remove_records("delete from t_user where %s = %d" % ("time", 1587820216529077300))
# test()
