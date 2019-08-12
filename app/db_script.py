from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text
import os
import pandas as pd

curr_dir = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(curr_dir, 'db_data')


class Base:

    def __init__(self):
        self.BASEDIR = os.path.abspath(os.path.dirname(__file__))
        self.USERNAME = "postgres"
        self.PASSWORD = "admin"
        self.PORT = 5432
        self.DB_NAME = "collegecarddb"
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
        university_id = "university_id integer"
        try:
            self.conn.execute("CREATE TABLE "
                              "Users({id}, {dob},"
                              "{educational_attainment}, "
                              "{email}, "
                              "{first_name},"
                              "{joined_site},"
                              "{last_name},"
                              "{password},"
                              "{university_id},"
                              "{username}"");".format(id=id,
                                                            dob=dob,
                                                            educational_attainment=educational_attainment,
                                                            email=email,
                                                            first_name=first_name,
                                                            joined_site=joined_site,
                                                            last_name=last_name,
                                                            password=password,
                                                            university_id=university_id,
                                                            username=username))
        except ProgrammingError as error:
            print('TABLE ALREADY EXISTS')
        except:
            print("SOMETHING ELSE WENT TERRIBLY WRONG")

    def import_db(self):
        file_path = os.path.join(data_path, 'users.csv')
        with open(file_path, 'r') as f:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            cmd = 'COPY users(dob,educational_attainment,email,first_name,joined_site,last_name,password,university_id,username) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'
            cursor.copy_expert(cmd, f)
            connection.commit()

    def insert_user(self, first_name, last_name, username, email, password, joined_site, dob, attainment, alumni_of):
        q = text("INSERT INTO users(first_name, last_name, username, email, password, joined_site, dob, educational_attainment, university_id) "
                 "VALUES('{first_name}', '{last_name}', '{username}', '{email}', '{password}', '{dob}', '{joined_site}', '{edu_attainment}', '{alumni_of}')".format(
            first_name=first_name, last_name=last_name, username=username, email=email, password=password, dob=dob, joined_site=joined_site,
            alumni_of=alumni_of, edu_attainment=attainment))

        try:
            self.conn.execute(q)
            return True
        except:
            return False

    def get_user_by_username(self, username):
        q = text("SELECT * FROM users WHERE username = '{name}'".format(name=username))
        res = self.conn.execute(q)
        if res.rowcount == 1:
            return dict(res.first())
        else:
            return False

    def get_user_by_id(self, id):
        q = text("SELECT * FROM users WHERE id = '{id}'".format(id=id))
        res = self.conn.execute(q)
        if res.rowcount == 1:
            return dict(res.first())
        else:
            return False


    def get_users_by_age(self, age):
        res = self.conn.execute("SELECT first_name, last_name, date_part('year',age(dob)) as age, * FROM users;")
        return res

    def get_users_joined_before_date(self, date):
        res = self.conn.execute("SELECT * FROM users WHERE joined_site <= '{date}';".format(date=date))
        return res


class Comment(Base):
    def __init__(self):
        super().__init__()
        comment_id = "id integer GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY"
        university_id = "university_id integer"
        user_id = "user_id integer"
        comment = "comment TEXT"
        try:
            self.conn.execute("CREATE TABLE comment({comment_id}, {university_id}, {user_id}, {comment});".format(
                university_id=university_id,
                user_id=user_id,
                comment_id=comment_id,
                comment=comment))
        except ProgrammingError:
            print('TABLE ALREADY EXISTS')

    def import_db(self):
        file_path = os.path.join(data_path, 'comments.csv')
        with open(file_path, 'r') as f:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            cmd = 'COPY comment(comment,university_id,user_id) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'
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

    def get_comments_by_user_id(self, user_id):
        q = text("SELECT comment FROM comment WHERE user_id = '{user_id}'".format(user_id=user_id))
        res = self.conn.execute(q)
        if res.rowcount > 0:
            return [dict(i) for i in res]
        return False


class University(Base):
    def __init__(self):
        super().__init__()
        # self.conn.execute("DROP TABLE universities;")

        try:
            self.conn.execute(
                "CREATE TABLE universities (id integer PRIMARY KEY, ope8_id integer, ope6_id integer, name VARCHAR(500), city VARCHAR(500), state integer, "
                "zip integer, accreditor VARCHAR(500),	school_url VARCHAR(500), price_calculator_url VARCHAR(500), main_campus	integer, branches integer, region_id integer);")
        except ProgrammingError:
            print("TABLE ALREADY EXISTS")

    def import_db(self):
        # self.conn.execute("DROP TABLE universities;")
        file_path = os.path.join(data_path, 'university_data.csv')
        with open(file_path, 'r') as f:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            cols = "id,ope8_id,ope6_id,name,city,state,zip,accreditor,school_url,price_calculator_url,main_campus,branches,region_id"
            cmd = 'COPY universities({cols}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'.format(cols=cols)
            cursor.copy_expert(cmd, f)
            connection.commit()

    def get_university_id_from_name(self, name):
        q = text("SELECT id, name FROM universities WHERE name LIKE '%{name}'".format(name=name))
        res = self.conn.execute(q)
        data = res.first()
        if data:
            return data['id']
        else:
            return -1

    def get_university_by_name(self, name):
        q = text("SELECT * FROM universities WHERE name LIKE '{name}%'".format(name=name))
        res = self.conn.execute(q)
        if res.rowcount > 0:
            return [dict(i) for i in res]
        return False


class Regions(Base):
    def __init__(self):
        super().__init__()
        #self.conn.execute("DROP TABLE regions;")
        try:
            self.conn.execute(
                "CREATE TABLE regions (id integer PRIMARY KEY, region VARCHAR(500))")
        except ProgrammingError:
            print("TABLE ALREADY EXISTS")

    def import_db(self):
        # self.conn.execute("DROP TABLE universities;")
        file_path = os.path.join(data_path, 'regions.csv')
        with open(file_path, 'r') as f:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            cols = "id, region"
            cmd = 'COPY regions({cols}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'.format(cols=cols)
            cursor.copy_expert(cmd, f)
            connection.commit()


class Locations(Base):
    def __init__(self):
        super().__init__()
        # self.conn.execute("DROP TABLE universities;")

        try:
            self.conn.execute(
                "CREATE TABLE locations (zip integer PRIMARY KEY, type VARCHAR(500), city VARCHAR(500), state integer, county VARCHAR(500), "
                "timezone VARCHAR(500), country VARCHAR(500), latitude REAL, longitude REAL, irs_estimated_population_2015 integer);")
        except ProgrammingError:
            print("TABLE ALREADY EXISTS")

    def import_db(self):
        # self.conn.execute("DROP TABLE universities;")
        file_path = os.path.join(data_path, 'location.csv')
        with open(file_path, 'r') as f:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            cols = "zip,type,city,state,county,timezone,country,latitude,longitude,irs_estimated_population_2015"
            cmd = 'COPY locations({cols}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE);'.format(cols=cols)
            cursor.copy_expert(cmd, f)
            connection.commit()


class States(Base):
    def __init__(self):
        super().__init__()
        # self.conn.execute("DROP TABLE universities;")

        try:
            self.conn.execute(
                "CREATE TABLE States(id integer PRIMARY KEY, state VARCHAR(3));")
        except ProgrammingError:
            print("TABLE ALREADY EXISTS")

    def import_db(self):
        # self.conn.execute("DROP TABLE universities;")
        file_path = os.path.join(data_path, 'states.csv')
        with open(file_path, 'r') as f:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            cols = "id,state"
            cmd = 'COPY states({cols}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE);'.format(cols=cols)
            cursor.copy_expert(cmd, f)
            connection.commit()


class Statistics(Base):
    def __init__(self):
        super().__init__()
        # self.conn.execute("DROP TABLE universities;")
        id = "id integer PRIMARY KEY"
        carnegie_basic = "carnegie_basic INTEGER"
        carnegie_undergrad = "carnegie_undergrad INTEGER"
        carnegie_size_setting = "carnegie_size_setting INTEGER"
        minority_serving_historically_black = "minority_serving_historically_black INTEGER"
        minority_serving_predominantly_black = "minority_serving_predominantly_black INTEGER"
        minority_serving_annh = "minority_serving_annh INTEGER"
        minority_serving_tribal = "minority_serving_tribal INTEGER"
        minority_serving_aanipi = "minority_serving_aanipi INTEGER"
        minority_serving_hispanic = "minority_serving_hispanic INTEGER"
        minority_serving_nant = "minority_serving_nant INTEGER"
        men_only = "men_only INTEGER"
        women_only = "women_only INTEGER"
        religious_affiliation = "religious_affiliation INTEGER"
        admission_rate_overall = "admission_rate_overall REAL"
        admission_rate_by_ope_id = "admission_rate_by_ope_id REAL"
        attendance_academic_year = "attendance_academic_year INTEGER"
        attendance_program_year = "attendance_program_year INTEGER"
        tuition_in_state = "tuition_in_state INTEGER"
        tuition_out_of_state = "tuition_out_of_state INTEGER"
        tuition_program_year = "tuition_program_year INTEGER"
        tuition_revenue_per_fte = "tuition_revenue_per_fte INTEGER"
        instructional_expenditure_per_fte = "instructional_expenditure_per_fte INTEGER"
        faculty_salary = "faculty_salary INTEGER"
        ft_faculty_rate = "ft_faculty_rate REAL"
        pell_grant_rate = "pell_grant_rate REAL"
        completion_rate_4yr_150nt = "completion_rate_4yr_150nt REAL"
        completion_rate_less_than_4yr_150nt = "completion_rate_less_than_4yr_150nt REAL"

        try:
            self.conn.execute("CREATE TABLE Statistics({id},"
                              "{carnegie_basic},"
                              "{carnegie_undergrad},"
                              "{carnegie_size_setting},"
                              "{minority_serving_historically_black},"
                              "{minority_serving_predominantly_black},"
                              "{minority_serving_annh},"
                              "{minority_serving_tribal},"
                              "{minority_serving_aanipi},"
                              "{minority_serving_hispanic},"
                              "{minority_serving_nant},"
                              "{men_only},"
                              "{women_only},"
                              "{religious_affiliation},"
                              "{admission_rate_overall},"
                              "{admission_rate_by_ope_id},"
                              "{attendance_academic_year},"
                              "{attendance_program_year},"
                              "{tuition_in_state},"
                              "{tuition_out_of_state},"
                              "{tuition_program_year},"
                              "{tuition_revenue_per_fte},"
                              "{instructional_expenditure_per_fte},"
                              "{faculty_salary},"
                              "{ft_faculty_rate},"
                              "{pell_grant_rate},"
                              "{completion_rate_4yr_150nt},"
                              "{completion_rate_less_than_4yr_150nt}"");".format(id=id,
                                                                                 carnegie_basic=carnegie_basic,
                                                                                 carnegie_undergrad=carnegie_undergrad,
                                                                                 carnegie_size_setting=carnegie_size_setting,
                                                                                 minority_serving_historically_black=minority_serving_historically_black,
                                                                                 minority_serving_predominantly_black=minority_serving_predominantly_black,
                                                                                 minority_serving_annh=minority_serving_annh,
                                                                                 minority_serving_tribal=minority_serving_tribal,
                                                                                 minority_serving_aanipi=minority_serving_aanipi,
                                                                                 minority_serving_hispanic=minority_serving_hispanic,
                                                                                 minority_serving_nant=minority_serving_nant,
                                                                                 men_only=men_only,
                                                                                 women_only=women_only,
                                                                                 religious_affiliation=religious_affiliation,
                                                                                 admission_rate_overall=admission_rate_overall,
                                                                                 admission_rate_by_ope_id=admission_rate_by_ope_id,
                                                                                 attendance_academic_year=attendance_academic_year,
                                                                                 attendance_program_year=attendance_program_year,
                                                                                 tuition_in_state=tuition_in_state,
                                                                                 tuition_out_of_state=tuition_out_of_state,
                                                                                 tuition_program_year=tuition_program_year,
                                                                                 tuition_revenue_per_fte=tuition_revenue_per_fte,
                                                                                 instructional_expenditure_per_fte=instructional_expenditure_per_fte,
                                                                                 faculty_salary=faculty_salary,
                                                                                 ft_faculty_rate=ft_faculty_rate,
                                                                                 pell_grant_rate=pell_grant_rate,
                                                                                 completion_rate_4yr_150nt=completion_rate_4yr_150nt,
                                                                                 completion_rate_less_than_4yr_150nt=completion_rate_less_than_4yr_150nt))

        except ProgrammingError:
            print("TABLE ALREADY EXISTS")

    def import_db(self):
        # self.conn.execute("DROP TABLE universities;")
        file_path = os.path.join(data_path, 'statistics.csv')
        with open(file_path, 'r') as f:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            cols = "id,carnegie_basic,carnegie_undergrad,carnegie_size_setting,minority_serving_historically_black,minority_serving_predominantly_black,minority_serving_annh,minority_serving_tribal,minority_serving_aanipi,minority_serving_hispanic,minority_serving_nant,men_only,women_only,religious_affiliation,admission_rate_overall,admission_rate_by_ope_id,attendance_academic_year,attendance_program_year,tuition_in_state,tuition_out_of_state,tuition_program_year,tuition_revenue_per_fte,instructional_expenditure_per_fte,faculty_salary,ft_faculty_rate,pell_grant_rate,completion_rate_4yr_150nt,completion_rate_less_than_4yr_150nt"
            cmd = 'COPY Statistics({cols}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'.format(cols=cols)
            cursor.copy_expert(cmd, f)
            connection.commit()


class UniversityImages(Base):
    def __init__(self):
        super().__init__()
        try:
            self.conn.execute(
                "CREATE TABLE UniversityImages(id integer PRIMARY KEY, ope8_id integer, campus_photo VARCHAR(500));")
        except ProgrammingError:
            print("TABLE ALREADY EXISTS")

    def import_db(self):
        # self.conn.execute("DROP TABLE universities;")
        file_path = os.path.join(data_path, 'university_image_links.csv')
        with open(file_path, 'r') as f:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            cols = "campus_photo,id,ope8_id"
            cmd = 'COPY UniversityImages({cols}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'.format(cols=cols)
            cursor.copy_expert(cmd, f)
            connection.commit()


class Subscribes(Base):

    def __init__(self):
        super().__init__()
        try:
            self.conn.execute(
                "CREATE TABLE Subscribes(user_id integer REFERENCES users(id), university_id integer REFERENCES universities(id), "
                "CONSTRAINT p_id PRIMARY KEY (user_id, university_id));")
        except ProgrammingError:
            print("TABLE ALREADY EXISTS")

    def import_db(self):
        file_path = os.path.join(data_path, 'university_subscriptions.csv')
        with open(file_path, 'r') as f:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            cols = "user_id,university_id"
            cmd = 'COPY Subscribes({cols}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'.format(cols=cols)
            cursor.copy_expert(cmd, f)
            connection.commit()


class Friend(Base):

    def __init__(self):
        super().__init__()
        try:
            self.conn.execute("CREATE TABLE Friend(user_id integer REFERENCES users(id), friend_id integer REFERENCES users(id));")
        except ProgrammingError:
            print("TABLE ALREADY EXISTS")

    def import_db(self):
        file_path = os.path.join(data_path, 'user_friends.csv')
        with open(file_path, 'r') as f:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            cols = "user_id,friend_id"
            cmd = 'COPY Friend({cols}) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'.format(cols=cols)
            cursor.copy_expert(cmd, f)
            connection.commit()


if __name__ == "__main__":
    try:
        universities = University()
        universities.import_db()
    except:
        print ("DB EXISTS WITH DATA")

    try:
        university_images = UniversityImages()
        university_images.import_db()
    except:
        print("DB EXISTS WITH DATA")

    try:
        comment = Comment()
        comment.import_db()
    except:
        print("DB EXISTS WITH DATA")

    try:
        region = Regions()
        region.import_db()
    except:
        print("DB EXISTS WITH DATA")


    try:
        stats = Statistics()
        stats.import_db()
    except:
        print("DB EXISTS WITH DATA")


    try:
        states = States()
        states.import_db()
    except:
        print("DB EXISTS WITH DATA")


    try:
        users = Users()
        users.import_db()
    except:
        print("DB EXISTS WITH DATA")

    try:
        locations = Locations()
        locations.import_db()
    except:
        print("DB EXISTS WITH DATA")

    try:
        friend = Friend()
        friend.import_db()
    except:
        print("DB EXISTS WITH DATA")

    try:
        subs = Subscribes()
        subs.import_db()
    except:
        print("DB EXISTS WITH DATA")