from .base_service import BaseService

class BookService(BaseService):
    def __init__(self):
        super().__init__()  

    # --- implement abstract methods
    def get_all(self):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("""select title, pub_date
                            from books t1 
                            left join book_authors t2 on t1.author_id = t2.id
                            left join book_types t3 on t1.type_id = t3.id
                            left join book_categories t4 on t1.category_id = t4.id
                       """)
        result = cursor.fetchall()
        cursor.close()

        return result

    def get_by_id(self, id):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("""select title, pub_date
                            from books t1 
                            left join book_authors t2 on t1.author_id = t2.id
                            left join book_types t3 on t1.type_id = t3.id
                            left join book_categories t4 on t1.category_id = t4.id
                            where t1.id = %s
                       """, (id,))
        result = cursor.fetchone()
        cursor.close()

        return result

    def create(self, data):
        cursor = self.dbcnx.cursor()

        cursor.execute("insert into books (title, pub_date, status, category_id, type_id) values (%s, %s, %s, %s, %s)", 
                        (data['title'], data['pub_date'], data['status'], data['category_id'], data['type_id']))
        newId = cursor.lastrowid

        self.dbcnx.commit()
        cursor.close()

        return newId

    def update(self, data):
        cursor = self.dbcnx.cursor()

        cursor.execute("""
                       update books set title = %s, pub_date = %s, status = %s, category_id = %s, type_id = %s where id = %s""",
                            (data['title'], data['pub_date'], data['status'], data['category_id'], data['type_id'], data['id'],))

        affected_rows = cursor.rowcount
        self.dbcnx.commit()
        cursor.close()

        return affected_rows

    def delete(self, id):
        cursor = self.dbcnx.cursor()

        cursor.execute("delete from users where id = %s", (id,))
        affected_rows = cursor.rowcount
        self.dbcnx.commit()
        cursor.close()

        return affected_rows
