from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from main.StuInfoModels import Exam

mysql_engine = create_engine('mysql+pymysql://xyang:heitou45@localhost:3306/stu_info?charset=utf8', echo=True)
MysqlSession = sessionmaker(bind=mysql_engine)
Base = declarative_base()


# class Student(Base):  # 必须继承declaraive_base得到的那个基类
#     __tablename__ = "Students"  # 必须要有__tablename__来指出这个类对应什么表，这个表可以暂时在库中不存在，SQLAlchemy会帮我们创建这个表
#     Sno = Column(String(10), primary_key=True)  # Column类创建一个字段
#     Sname = Column(String(20), nullable=False, unique=True,
#                    index=True)  # nullable就是决定是否not null，unique就是决定是否unique。。这里假定没人重名，设置index可以让系统自动根据这个字段为基础建立索引
#     Ssex = Column(String(2), nullable=False)
#     Sage = Column(Integer, nullable=False)
#     Sdept = Column(String(20))
#
#     def __repr__(self):
#         return "<Student>{}:{}".format(self.Sname, self.Sno)


Base.metadata.create_all(mysql_engine)  # 这就是为什么表类一定要继承Base，因为Base会通过一些方法来通过引擎初始化数据库结构。不继承Base自然就没有办法和数据库发生联系了。

mysql_session = MysqlSession()    #创建session对象
# frank = Students(name='Frank')    #数据对象得到创建，此时为Transient状态
# session.add(frank)    #数据对象被关联到session上，此时为Pending状态
# session.commit()    #数据对象被推到数据库中，此时为Persistent状态
# session.close()    #关闭session对象
# print(frank.name)    #此时会报错DetachedInstanceError，因为此时是Detached状态。

# print(session.query(MChoose))
print(mysql_session.query(Exam))
# session.query(MChoose).filter(Student.Sname == 'Frank').first()
# session.query(Student).filter_by(Sname == 'Frank').first()

# student = MChoose()
# session.add(student)
# session.commit()  # 不要忘了commit
# session.close()

