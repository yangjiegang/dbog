import threading

import Vars as mVars
from NumQueryDAO import NumQueryDAO
from Tools import tool


class SQLite3DAOConsumerWorker(threading.Thread):

    def __init__(self, thread_name):
        super(SQLite3DAOConsumerWorker, self).__init__(name=thread_name)
        self.stop_event = threading.Event()
        self.num_query_dao = NumQueryDAO()
        self.DAO_Queue = mVars.GlobalDAOQueue

    def run(self):
        # 消费队列线程已启动
        if mVars.DAO_worker_started_flag and not self.stop_event.isSet():
            while not self.DAO_Queue.empty():
                try:
                    # if not self.DAO_Queue.empty():
                    #     print('------------------------- taek is done-----------------------')
                    # else:
                    (q_type, _cols, _data) = self.DAO_Queue.get(block=True, Timeout=3)
                    self.num_query_dao.execute_insert(q_type, _cols, _data)
                    # if self.num_query_dao.execute_insert(q_type, _cols, _data):
                    #     self.DAO_Queue.task_done()
                except Exception as e:
                    tool.logger.error(e)
                finally:
                    self.stop_event.set()
            # 消费队列线程已启动
            print('------------------------- all DAO taek was done-----------------------')

    # def execute_insert(self, q_type, _cols, _data):
    #     mVars.t_lock.acquire()  # 加锁，锁住相应的资源
    #     self.insert(('tbl_%s' % q_type),
    #                 dict(zip(_cols, _data)))
    #     mVars.t_lock.release()  # 解锁，离开该资源
    #
    # def do_insert(self, tbl_name, kv_dict):
    #     field_value_str = ''
    #     field_name_str = ''
    #     for (f_name, value) in kv_dict.items():
    #         field_name_str += '%s,' % f_name
    #         field_value_str += "'%s'," % value
    #     field_name_str = field_name_str[0:-1]
    #     field_value_str = field_value_str[0:-1]
    #     sql_str = "insert into %s(%s) values(%s)" % (tbl_name, field_name_str, field_value_str)
    #     self.db.execute(sql_str)
# DAO_Worker = SQLite3DAOConsumerWorker('dao_consumer')
# DAO_Worker.start()