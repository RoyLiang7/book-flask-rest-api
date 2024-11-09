from src.services.base_service import BaseService


class BookTypeService(BaseService):

    def __init__(self):
        super().__init__()  # to gain access to parent objects


    # --- implement abstract methods
    def get_all(self):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("select * from book_types")
        result = cursor.fetchall()
        cursor.close()

        return result

    def get_by_id(self, id):
        cursor = self.dbcnx.cursor(dictionary=True)

        result = cursor.execute("select * from book_types where id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()

        return result

    def create(self, data):
        cursor = self.dbcnx.cursor()

        cursor.execute("insert into book_types (description) values (%s, %s)", (data['description']))
        newId = cursor.lastrowid

        self.dbcnx.commit()
        cursor.close()

        return newId

    def update(self, data):
        cursor = self.dbcnx.cursor()

        cursor.execute("update book_types set description = %s where id = %s", (data['description'], id))
        affected_rows = cursor.rowcount

        self.dbcnx.commit()
        cursor.close()

        return affected_rows

    def delete(self, id):
        cursor = self.dbcnx.cursor()

        cursor.execute("delete from book_types where id = %s", (id,))
        affected_rows = cursor.rowcount

        self.dbcnx.commit()
        cursor.close()

        return affected_rows
