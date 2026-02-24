# db_helper.py
import pymysql

DB_CONFIG = dict(
    host="localhost",
    user="root",
    password="0000",
    database="sungsimdang",
    charset="utf8"
)

class DB:
    def __init__(self, **config):
        self.config = config

    def connect(self):
        return pymysql.connect(**self.config)



    # 멤버 전체 조회
    def fetch_members(self):
        sql = "SELECT id, name, price, num FROM item ORDER BY id"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()

    # 멤버 추가
    def insert_member(self, name, price, num):
        sql = "INSERT INTO item (name, price, num) VALUES (%s, %s, %s)"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (name, price, num))
                conn.commit()
                return True
            except Exception as e:
                print(f"진짜 에러 원인: {e}")
                conn.rollback()
                return False

    def modify_member(self,price, num, name):
        sql = "UPDATE item SET price=%s, num=%s WHERE name=%s"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (price, num, name))
                conn.commit()
                return True
            except Exception as e:
                print(f"진짜 에러 원인: {e}")
                conn.rollback()
                return False


    def err_member(self, name):
        sql = "DELETE FROM item WHERE name=%s"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, name)
                conn.commit()
                return True
            except Exception as e:
                print(f"진짜 에러 원인: {e}")
                conn.rollback()
                return False