import requests

from main.qt.CurlUtil import CurlUtil
from main.qt.ISqlTranslator import ISqlTranslator
import main.qt.Vars as Vars


class SqlTranslator(ISqlTranslator):

    def __init__(self):
        self.valid_from_dialect = (
            "No specific dialect",
            "DB2",
            "Derby",
            "Firebird",
            "H2",
            "HANA",
            "HSQLDB",
            "Informix",
            "Ingres",
            "MariaDB",
            "MySQL",
            "Access",
            "Oracle",
            "PostgreSQL",
            "Redshift",
            "SQL Data Warehouse",
            "SQLite",
            "SQL Server",
            "ASE",
            "Sybase",
            "Teradata")
        self.valid_to_dialect = (
            "Aurora_MySQL",
            "Aurora_PostgreSQL",
            "DB2_9",
            "DB2_10",
            "DB2",
            "Derby",
            "FIREBIRD_2_5",
            "FIREBIRD_3_0",
            "Firebird",
            "H2",
            "HANA",
            "HSQLDB",
            "Informix",
            "Ingres",
            "MariaDB",
            "MySQL_5_7",
            "MySQL_8_0",
            "MySQL",
            "Access",
            "Oracle 10g",
            "Oracle 11g",
            "Oracle 12c",
            "Oracle 18c",
            "Oracle",
            "PostgreSQL_9_3",
            "PostgreSQL_9_4",
            "PostgreSQL_9_5",
            "PostgreSQL_10",
            "PostgreSQL_11",
            "PostgreSQL",
            "Redshift",
            "SQL Data Warehouse",
            "SQLite",
            "SQL Server 2008",
            "SQL Server 2012",
            "SQL Server 2014",
            "SQL Server 2016",
            "SQL Server 2017",
            "SQL Server",
            "ASE",
            "Sybase",
            "Teradata")

    def remote_translate(self, sql_str, to_db_type):
        ret = requests.post(Vars.server_api, {
            'sqlStr': sql_str,
            'destType': to_db_type
        })
        return ret.text

    def web_translate(self, sql_str, from_type, to_type):
        if from_type not in self.valid_from_dialect or to_type not in self.valid_to_dialect:
            return "invalid SQL dialect"
        else:
            from_type = from_type.replace(' ', '').upper()
            to_type = to_type.replace(' ', '').upper()
        c = CurlUtil.init_curl()
        data_str = 'from-dialect=%s&to-dialect=%s&to-keywords=LOWER&to-name-case=AS_IS&to-name-quoted' \
                   '=EXPLICIT_DEFAULT_UNQUOTED&to-param-type=NAMED&to-field-as=DEFAULT&to-table-as=DEFAULT&to-inner' \
                   '-keyword=DEFAULT&to-outer-keyword=DEFAULT&sql=%s' % (
            from_type, to_type, sql_str)
        html = CurlUtil.post_data(c, 'http://www.jooq.org/translate/translate', data_str)
        return html.decode('utf-8')

    def get_opposite_sql_type(self, sql_type, from_orient):
        if 'from' == from_orient:
            for i in range(0, len(self.valid_to_dialect)):
                if sql_type in self.valid_to_dialect[i]:
                    return i
        elif 'to' == from_orient:
            for i in range(0, len(self.valid_from_dialect)):
                if self.valid_from_dialect[i] in sql_type:
                    return i
        else:
            return 0
