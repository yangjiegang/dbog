# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Authority(Base):
    __tablename__ = 'authority'

    auth_id = Column(INTEGER(8), primary_key=True)
    auth_name = Column(String(255), nullable=False)
    auth_value = Column(TINYINT(1), nullable=False)


class Exam(Base):
    __tablename__ = 'exam'

    id = Column(INTEGER(65), primary_key=True)
    username = Column(String(32))
    password = Column(String(32))
    marks = Column(BIGINT(10))
    sex = Column(TINYINT(1))
    role_id = Column(BIGINT(10))


class MByrow(Base):
    __tablename__ = 'm_byrow'

    id = Column(INTEGER(11), primary_key=True)
    class_id = Column(INTEGER(11))
    teacher_id = Column(INTEGER(11))
    col_value = Column(INTEGER(11))
    row_value = Column(INTEGER(11))
    course_id = Column(INTEGER(11))
    room_id = Column(INTEGER(11))


class MCategory(Base):
    __tablename__ = 'm_category'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(100))
    remark = Column(String(100))
    code = Column(String(50))


class MChoose(Base):
    __tablename__ = 'm_choose'

    id = Column(INTEGER(11), primary_key=True)
    course_id = Column(INTEGER(11))
    student_id = Column(INTEGER(11))


class MCourse(Base):
    __tablename__ = 'm_course'

    id = Column(INTEGER(11), primary_key=True)
    c_code = Column(String(100))
    c_name = Column(String(100))
    c_descr = Column(String(255))
    c_state = Column(String(30))
    c_cate = Column(String(30))


class MMessage(Base):
    __tablename__ = 'm_message'

    id = Column(INTEGER(11), primary_key=True)
    content = Column(String(100))
    t_name = Column(String(100))


class MMyclas(Base):
    __tablename__ = 'm_myclass'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(100))
    remark = Column(String(100))
    cate_id = Column(INTEGER(11))


class MProject(Base):
    __tablename__ = 'm_project'

    id = Column(INTEGER(11), primary_key=True)
    teacher_id = Column(INTEGER(11))
    course_id = Column(INTEGER(11))
    class_Id = Column(INTEGER(11))
    code = Column(String(100))


class MRoom(Base):
    __tablename__ = 'm_room'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(100))


class MScore(Base):
    __tablename__ = 'm_score'

    id = Column(INTEGER(11), primary_key=True)
    course_id = Column(INTEGER(11))
    student_id = Column(INTEGER(11))
    teacher_id = Column(INTEGER(11))
    value = Column(String(30))


class MSubject(Base):
    __tablename__ = 'm_subject'

    id = Column(INTEGER(11), primary_key=True)
    teacher_id = Column(INTEGER(11))
    class_id = Column(INTEGER(11))
    cate_id = Column(INTEGER(11))
    status = Column(String(100))
    code = Column(String(30))
    course_id = Column(INTEGER(11))


class MUser(Base):
    __tablename__ = 'm_user'

    id = Column(INTEGER(11), primary_key=True)
    u_name = Column(String(100))
    u_pwd = Column(String(100))
    u_type = Column(String(20))
    cate_name = Column(String(30))
    real_name = Column(String(30))
    grade = Column(String(30))
    sex = Column(String(30))
    title_name = Column(String(30))
    class_id = Column(INTEGER(11))


class RoleGroup(Base):
    __tablename__ = 'role_group'

    role_group_id = Column(INTEGER(8), primary_key=True)
    role_gourp_name = Column(String(255), nullable=False)
    has_role_ids = Column(String(255))


class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(INTEGER(99), primary_key=True)
    role_name = Column(String(255), nullable=False)
    role_auths = Column(BIGINT(10), nullable=False)
    role_group_ids = Column(String(255))


class TbClas(Base):
    __tablename__ = 'tb_class'

    id = Column(INTEGER(11), primary_key=True)
    class_name = Column(LONGTEXT)


class TbMajor(Base):
    __tablename__ = 'tb_major'

    id = Column(INTEGER(11), primary_key=True)
    major_name = Column(LONGTEXT)


class TbScro(Base):
    __tablename__ = 'tb_scroes'

    id = Column(INTEGER(11), primary_key=True)
    subject_id = Column(INTEGER(11))
    stu_id = Column(INTEGER(11))
    scroes = Column(INTEGER(11))


class TbStu(Base):
    __tablename__ = 'tb_stu'

    id = Column(INTEGER(11), primary_key=True)
    stu_name = Column(LONGTEXT)
    stu_no = Column(INTEGER(11))
    enter_year = Column(INTEGER(11))


class TbSubject(Base):
    __tablename__ = 'tb_subject'

    id = Column(INTEGER(11), primary_key=True)
    subject_name = Column(LONGTEXT)


class TbTeacher(Base):
    __tablename__ = 'tb_teacher'

    id = Column(INTEGER(11), primary_key=True)
    t_name = Column(LONGTEXT)
    subject_name = Column(LONGTEXT)
