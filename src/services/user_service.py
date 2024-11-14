from flask import jsonify
from flask_jwt_extended import create_access_token

from src.services.base_service import BaseService
from src import bcrypt


class UserService(BaseService):

    def __init__(self):
        super().__init__()  # to gain access to parent objects

    def get_all(self):
        cursor = self.dbcnx.cursor(dictionary=True)
        
        cursor.execute("""
            select t1.id as id, t1.name as name, t2.name as role, t3.name as company, t1.email as email, t1.status as status 
                from users t1
                    left join roles t2 on t1.role_id = t2.id
                    left join companies t3 on t1.company_id = t3.id
        """)
        response = cursor.fetchall() # ===> [{},{},{}]

        rowCount = cursor.rowcount
        cursor.close()

        return response

    def get_by_id(self, id):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("select * from users where id = %s", (id,))
        result = cursor.fetchall()  # ===> [{}]
        
        cursor.close()

        return result

    def create(self, model):
        pw_hash = bcrypt.generate_password_hash(model['password']).decode('utf-8')

        cursor = self.dbcnx.cursor()
        cursor.execute("insert into users (name, email, role_id, company_id, password) values (%s, %s, %s, %s, %s)", 
                                (model['name'], model['email'], model['role_id'], model['company_id'], pw_hash))

        newId = cursor.lastrowid
        self.dbcnx.commit()     # important !!!!
        cursor.close()

        return newId            # the id of the newly added record

    def update(self, model):
        cursor = self.dbcnx.cursor()

        cursor.execute("update users set name = %s, email = %s, role_id = %s, company_id = %s, password = %s where id = %s", 
                                (model['name'], model['email'], model['role_id'], model['company_id'], model['password'], model['id']))
        
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


    def authenticate(self, data):
        cursor = self.dbcnx.cursor(dictionary=True)
        cursor.execute("select id, name, email, password, status from users where email = %s", (data["email"],))
        result = cursor.fetchone()
        cursor.close()

        if result:
            pw_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            if result['password'] == pw_hash:
                return result
            
        return None
    
    def get_token(self, data):
        user = self.authenticate(data)
        if not user:
            return jsonify({"msg": "Bad email or password"}), 401

        access_token = create_access_token(identity=user)
        return jsonify({"access_token": access_token, "user": user})

    def get_hash(self, pwd):
        pw_hash = bcrypt.generate_password_hash(pwd).decode('utf-8')
        return pw_hash
