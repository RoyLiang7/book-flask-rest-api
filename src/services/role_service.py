from src.services.base_service import BaseService


class RoleService(BaseService):

    def __init__(self):
        super().__init__()  # to gain access to parent objects


    # --- implement abstract methods
    def get_all(self):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("select id, name from roles")
        result = cursor.fetchall()
        cursor.close()

        return result

    def get_by_id(self, id):
        cursor = self.dbcnx.cursor(dictionary=True)

        result = cursor.execute("select id, name from roles where id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()

        return result

    def create(self, data):
        cursor = self.dbcnx.cursor()

        name = data['name']

        cursor.execute("insert into roles (name) values (%s)", (name))
        newId = cursor.lastrowid
        self.dbcnx.commit()
        cursor.close()

        return newId

    def update(self, data):
        cursor = self.dbcnx.cursor()

        id = data['id'] ; name = data['name']

        cursor.execute("update roles set name = %s where id = %s", (name, id))
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
