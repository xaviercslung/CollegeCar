from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
import os
import pandas as pd

curr_dir = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(curr_dir, 'data')

mapped_data_path = os.path.join(data_path, 'mapped_data.xlsx')
df_mapped_data = pd.read_excel(mapped_data_path)
random_users_path = os.path.join(data_path, 'users.csv')


class Base:

    def __init__(self):
        self.BASEDIR = os.path.abspath(os.path.dirname(__file__))
        self.USERNAME = "postgres"
        self.PASSWORD = "admin"
        self.PORT = 5432
        self.DB_NAME = "CollegeCardDB"

        self.POSTGRES_LOCAL_BASE = "postgresql://{username}:{password}@localhost:{port}/{db_name}".format(username=self.USERNAME,
                                                                                                     password=self.PASSWORD,
                                                                                                     port=self.PORT,
                                                                                                     db_name=self.DB_NAME)

        self.engine = create_engine(self.POSTGRES_LOCAL_BASE)
        self.conn = self.engine.connect()


class Users(Base):

    def __init__(self):
        super().__init__()
        id = "id integer GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY"
        first_name = "first_name VARCHAR(255)"
        last_name = "last_name VARCHAR(255)"
        email = "email VARCHAR(255)"
        username = "username VARCHAR(255) UNIQUE"
        dob = "dob DATE"
        joined_site = "joined_site DATE"
        password = "password VARCHAR(255)"
        educational_attainment = "educational_attainment VARCHAR(255)"
        try:
            self.conn.execute("CREATE TABLE Users({id},"
                              "{first_name}, "
                              "{last_name}, "
                              "{username},"
                              "{email},"
                              "{dob},"
                              "{joined_site},"
                              "{password},"
                              "{educational_attainment}"");".format(id=id,
                                                                    first_name=first_name,
                                                                    last_name=last_name,
                                                                    email=email,
                                                                    username=username,
                                                                    dob=dob,
                                                                    joined_site=joined_site,
                                                                    password=password,
                                                                    educational_attainment=educational_attainment))
        except ProgrammingError as error:
            print('TABLE ALREADY EXISTS')

        except:
            print("SOMETHING ELSE WENT TERRIBLY WRONG")

    def add_dummy_users(self):
        file_path = os.path.join(data_path, 'users.csv')
        with open(file_path, 'r') as f:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            cmd = 'COPY users(dob,educational_attainment,email,first_name,joined_site,last_name,password,username) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'
            cursor.copy_expert(cmd, f)
            connection.commit()

    def insert_user(self, first_name, last_name, username, email, dob, joined_site, password, educational_attainment):
        self.conn.execute("INSERT INTO users(first_name, last_name, username, dob, joined_site, password, "
                          "educational_attainment) "
                          "VALUES ("
                          "'{first_name}',"
                          "'{last_name}',"
                          "'{username}',"
                          "'{email}',"
                          "'{dob}',"
                          "'{joined_site}',"
                          "'{password}',"
                          "'{educational_attainment}')".format(first_name=first_name,
                                                               last_name=last_name,
                                                               username=username,
                                                               email=email,
                                                               dob=dob,
                                                               joined_site=joined_site,
                                                               password=password,
                                                               educational_attainment=educational_attainment))

    def get_users_by_age(self, age):
        res = self.conn.execute("SELECT first_name, last_name, date_part('year',age(dob)) as age, * FROM users")
        return res

    def get_users_joined_before_date(self, date):
        res = self.conn.execute("SELECT * FROM users WHERE joined_site <= '{date}'".format(date=date))
        return res


class Comments(Base):
    def __init__(self):
        super().__init__()
        comment_id = "comment_id integer GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY"
        university_id = "university_id integer"
        user_id = "user_id integer"
        comment = "comment TEXT"
        try:
            self.conn.execute("CREATE TABLE comments({university_id},{user_id}, {comment_id}, {comment});".format(
                university_id=university_id,
                user_id=user_id,
                comment_id=comment_id,
                comment=comment))
        except ProgrammingError:
            print('TABLE ALREADY EXISTS')

    def add_dummy_comments(self):
        file_path = os.path.join(data_path, 'comments.csv')
        with open(file_path, 'r') as f:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            cmd = 'COPY comments(comment_id,university_id,user_id,comment) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'
            cursor.copy_expert(cmd, f)
            connection.commit()

    def insert_comment(self, university_id, user_id, comment_id, comment):
        self.conn.execute("INSERT INTO comments(university_id,user_id,comment_id,comment) "
                          "VALUES ("
                          "'{university_id}',"
                          "'{user_id}',"
                          "'{comment_id}',"
                          "'{comment}',".format(university_id=university_id,
                                                user_id=user_id,
                                                comment_id=comment_id,
                                                comment=comment))


class University(Base):

    def __init__(self):
        super().__init__()
        # self.conn.execute("DROP TABLE universities;")
        try:
            self.conn.execute(
                "CREATE TABLE universities (id integer PRIMARY KEY, ope8_id integer, ope6_id integer,name VARCHAR(500), accreditor text, school_url text);")
        except ProgrammingError:
            print("TABLE ALREADY EXISTS")

    def import_db(self):
        #self.conn.execute("DROP TABLE universities;")
        file_path = os.path.join(data_path, 'universities.csv')
        with open(file_path, 'r') as f:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            cols = "id,ope8_id,ope6_id,name,accreditor,school_url"
            cmd = 'COPY universities({cols}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'.format(cols=cols)
            cursor.copy_expert(cmd, f)
            connection.commit()

    def insert(self):
        self.conn.execute("INSERT INTO universities (uname, description)"
        "VALUES ('biubfewk', 'dkl  csd');")
        self.conn.execute("INSERT INTO universities (uname, description)"
                          "VALUES ('iurfif', 'dkl  csd');")



university = University()
university.import_db()


users = Users()
users.get_users_joined_before_date('2019-08-01')
