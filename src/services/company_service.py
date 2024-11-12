from src.services.base_service import BaseService


class CompanySerbice(BaseService):
    def __init__(self):
        super().__init__()  # to gain access to parent objects


    # ---- implement abstract methods
    def get_all(self):
        cursor = self.dbcnx.cursor(dictionary=True)

        result = cursor.execute("select id, name from companies")
        self.cursor.close()

        return result

    def get_by_id(self, id):
        cursor = self.dbcnx.cursor(dictionary=True)

        result = cursor.execute("select id, name from companies where id = %s", (id,))
        cursor.close()

        return result

    def create(self, data):
        cursor = self.dbcnx.cursor()

        name = data['name']

        result = cursor.execute("insert into companies (name) values (%s)", (name))
        cursor.close()

        return result

    def update(self, data):
        cursor = self.dbcnx.cursor()

        id = data['id']
        name = data['name']

        result = cursor.execute("update companies set name = %s where id = %s", (name, id))
        cursor.close()

        return result

    def delete(self, id):
        cursor = self.dbcnx.cursor()

        result = cursor.execute("delete from companies where id = %s", (id,))
        cursor.close()

        return result
