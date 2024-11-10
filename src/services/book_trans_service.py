from .base_service import BaseService

class BookTransactionService(BaseService):
    def __init__(self):
        super().__init__()  

    # --- implement abstract methods
    def get_all(self):
        cursor = self.dbcnx.cursor(dictionary=True)

    def get_by_id(self, id):
        pass


    def test_trans(self):
        try:
            self.dbcnx.start_transaction()

            cursor = self.dbcnx.cursor()
            cursor.dbcnx.start_transaction()

            cursor.execute("insert into book_categories (description) values (%s)", ('test category', ) )
            cursor.execute("insert into book_types (description) values (%s)", ('test type', ) )

            self.dbcnx.commit()
        except Exception as ex:
            self.dbcnx.rollback()
            raise Exception(ex)
        finally:
            cursor.close()


    def create(self, data):
        try:
            self.dbcnx.start_transaction()

            cursor = self.dbcnx.cursor()

            # --- trasaction hdr
            cursor.execute("""insert into book_trans_hdr (user_id, rent_days, total_amt)
                                    values (%s, %s, %s)
                               """, (data['user_id'], data['rent_days'], data['total_amt']))
            newHdrId = cursor.lastrowid

            # --- transaction details
            for detl in data['details']:
                cursor.execute("""insert into book_detl (hdr_id, book_id, type_id, rental_fees, book_qty)
                                    values (%s, %s, %s, %s, %s)
                               """, (newHdrId, detl['book_id'], detl['type_id'], detl['rental_fees'], detl['book_qty']))
            self.dbcnx.commit()            

            return newHdrId
        except :
            self.dbcnx.rollback()
        finally:
            cursor.close()


    def update(self, data):
        pass

    def delete(self, id):
        pass
    