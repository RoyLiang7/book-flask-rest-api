from src.services.base_service import BaseService


class BookTransactionService(BaseService):
    def __init__(self):
        super().__init__()  


    def test_trans(self):
        try:
            self.dbcnx.start_transaction()

            cursor = self.dbcnx.cursor()
            cursor.execute("insert into book_categories (description) values (%s)", ('test category', ) )
            cursor.execute("insert into book_types (description) values (%s)", ('test type', ) )

            self.dbcnx.commit()

        except Exception as ex:
            self.dbcnx.rollback()
            raise Exception(ex)
        finally:
            cursor.close()


    # --- implement abstract methods
    def get_all(self):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("""
            select *
                from book_trans_hdr t1
                    left join book_trans_detl t2 on t1.id = t2.hdr_id
                    left join users t3 on t1.user_id = t3.id
                    left join books t4 on t2.book_id = t4.id
                    left join book_types t5 on t2.type_id = t5.id
                    left join book_categories t6 on t4.category_id = t6.id
        """)
        result = cursor.fetchall()
        cursor.close()

        return result

    def get_by_id(self, id):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("""
            select *
                from book_trans_hdr t1
                    left join book_trans_detl t2 on t1.id = t2.hdr_id
                    left join users t3 on t1.user_id = t3.id
                    left join books t4 on t2.book_id = t4.id
                    left join book_types t5 on t2.type_id = t5.id
                    left join book_categories t6 on t4.category_id = t6.id
                where t1.id = %s
        """,(id,))
        result = cursor.fetchone()
        cursor.close()

        return result

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
        except Exception as ex:
            self.dbcnx.rollback()
            raise Exception(ex)
        finally:
            cursor.close()

    def update(self, data):
        cursor = self.dbcnx.cursor()

        cursor.execute("update book_trans_hdr set status = %s where id = %s", (2,))
        affected_rows = cursor.rowcount
        self.dbcnx.commit()
        cursor.close()

        return affected_rows

    def delete(self, id):
        cursor = self.dbcnx.cursor()

        cursor.execute("update book_trans_hdr set status = %s where id = %s", (2,))
        affected_rows = cursor.rowcount
        self.dbcnx.commit()
        cursor.close()

        return affected_rows


    # --- class methods
    def get_by_date(self, start_date: str, end_date: str):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("""
            select *
                from book_trans_hdr t1
                    left join book_detl t2 on t1.id = t2.hdr_id
                    left join users t3 on t1.user_id = t3.id
                    left join books t4 on t2.book_id = t4.id
                    left join book_types t5 on t2.type_id = t5.id
                    left join book_categories t6 on t4.category_id = t6.id
                where t1.trans_date between %s and = %s
        """,(start_date, end_date,))
        result = cursor.fetchall()
        cursor.close()

        return result
    
    def get_by_user(self, user_id, status):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("""
            select *
                from book_trans_hdr t1
                    left join book_detl t2 on t1.id = t2.hdr_id
                    left join users t3 on t1.user_id = t3.id
                    left join books t4 on t2.book_id = t4.id
                    left join book_types t5 on t2.type_id = t5.id
                    left join book_categories t6 on t4.category_id = t6.id
                where t1.user_id = %s and t1.status = %s
        """,(user_id, status,))
        result = cursor.fetchall()
        cursor.close()

        return result
    