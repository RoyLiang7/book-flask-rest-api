from src import bcrypt
from src.services.base_service import BaseService


class UserService(BaseService):

    def __init__(self):
        super().__init__()  # to gain access to parent objects

    # --- implement abstract methods
    def authenticate(self, data):
        cursor = self.dbcnx.execute("select * from users where email = $s", (data["email"]))
        response = cursor.fetchone()

        if response:
            pw_hash = bcrypt.generate_password_hash(data['password'])
            if response['password'] == pw_hash:
                return True
            
        return False


    def get_all(self):
        cursor = self.dbcnx.cursor(dictionary=True)
        
        cursor.execute("select * from users")
        response = cursor.fetchall() # ===> [{},{},{}]

        rowCount = cursor.rowcount
        cursor.close()

        return response

    def get_by_id(self, id):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("select * from users where id = %s", (id,))
        response = cursor.fetchone()  # ==> {"id":1, "name":"Kerrigan", }
        # --> check if fetchall() for only one record
        cursor.close()

        return response

    def create(self, model):
        cursor = self.dbcnx.cursor()

        name     = model['name']
        email    = model['email']
        password = model['password']

        pw_hash = bcrypt.generate_password_hash(password)

        cursor.execute("insert into users (name, email, password) values (%s, %s, %s)", 
                                (name, email, pw_hash,))

        newId = cursor.lastrowid
        self.dbcnx.commit()     # important !!!!
        cursor.close()

        return newId            # the id of the newly added record

    def update(self, data):
        cursor = self.dbcnx.cursor()

        id = data['id']
        name = data['name']
        email = data['email']
        password = data['password']

        cursor.execute("update users set name = %s, email = %s, password = %s where id = %s", 
                                (name, email, password, id,))
        affected_rows = cursor.rowcount
        self.dbcnx.commit()
        cursor.close()

        return affected_rows    # no of records updated

    def delete(self, id):
        cursor = self.dbcnx.cursor()

        cursor.execute("delete from users where id = %s", (id,))
        affected_rows = cursor.rowcount
        self.dbcnx.commit()
        cursor.close()

        return affected_rows    # no of records deleted




    # --- class specific methods
    def authenticate(self, data):
        cursor = self.dbcnx.cursor(dictionary=True)

        email = data['email']; password = data['password']
        cursor.execute("select * from users where email = %s and password = %s", (email, password,))
        response = cursor.fetchone()
        cursor.close()

        return response


    def get_related(self):
        # ---- https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("select * from users;select * from companies", None, multi=True)

        resultset = []
        for result in cursor.stored_results():
            resultset.append(result.fetchall())

        cursor.close()

        return resultset
    
    def get_sproc(self):
        # --- https://geert.vanderkelen.org/2010/multiple-result-sets-in-mysql-connectorpython/
        # --- https://dev.to/behainguyen/python-executing-mysql-stored-procedures-which-return-multiple-result-sets-1cif
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.callproc("new_procedure")

        resultset = []
        for result in cursor.stored_results():
            resultset.append(result.fetchall())

        cursor.close()

        return resultset

    def get_by_email(self, email):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("Select * from users where email = %s", (email,))
        response = cursor.fetchone()
        cursor.close()

        return response
