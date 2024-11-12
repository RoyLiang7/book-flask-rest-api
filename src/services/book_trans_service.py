from src.services.base_service import BaseService


class BookTransactionService(BaseService):
    def __init__(self):
        super().__init__()  


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
            select t1.id as id, t3.id, t3.name, t3.email, t1.rent_days, t1.total_amt, t5.description, t6.description 
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
        """
        {
            user_id: 1, rent_days: 6, total_amt: 99,
            details:[
                {book_id: 1, type_id: 2, rental_fee: 23, book_qty: 3},
                {book_id: 1, type_id: 2, rental_fee: 23, book_qty: 3}
            ]
        }
        """
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
                cursor.execute("""insert into book_trans_detlsss (hdr_id, book_id, type_id, rental_fee, book_qty)
                                    values (%s, %s, %s, %s, %s)
                               """, (newHdrId, detl['book_id'], detl['type_id'], detl['rental_fee'], detl['book_qty']))
                
            # --- update user credit used
            cursor.exeute("update user_credit set used_amt = user_amt + %s where user_id = %s", (data['total_amt'], data['user_id']))
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
    
    
    def get_late_books(self):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("""
            select t2.id as trans_id, t2.user_id as user_id, t2.trans_date as trans_date, t1.book_id as book_id, t1.type_id as type_id, t1.book_qty as qty   
                from book_trans_detl t1
                    left join book_trans_hdr t2 on t1.hdr_id = t2.id
                    left join books t3 on t1.book_id = t3.id
                where t2.status = 1
        """)
        result = cursor.fetchall()
        cursor.close()

        return result
    

    def get_late_trans(self):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("""
            select t1.id as trans_id, t1.user_id as user_id, t1.trans_date as trans_date, t2.id as detl.id, t2.book_id as book_id, t2.type_id as type_id, t2.book_qty as qty   
                from book_trans_hdr t1
                    left join book_trans_detl t2 on t1.id = t2.hdr_id
                where t1.status = 1
        """)

        results = cursor.fetchall()
        cursor.close()

        # result =>
        # [
        #   {trans_id: 1, user_id: 1, trans_date: '2024-01-01', detl_id: 1, book_id: 1, type_id: 2, qty: 3},
        #   {trans_id: 1, user_id: 1, trans_date: '2024-01-01', detl_id: 2, book_id: 2, type_id: 1, qty: 4},
        #   {trans_id: 2, user_id: 1, trans_date: '2024-01-01', detl_id: 1, book_id: 2, type_id: 2, qty: 5}
        # ]


        # ------ convert return to dict with list for details {...., details:[.....]}
        # ---- 1. simple for.next loop
        data = []

        for item in results:
            # Check if the hdr_id already exists in the result
            for entry in data:
                if entry['trans_id'] == item['trans_id']:
                    # If it exists, append the details
                    details = {
                        'detl_id' : item['detl_id'],
                        'book_id' : item['book_id'],
                        'type_id' : item['type_id'],
                        'qty'     : item['qty']
                    }
                    entry['details'].append(details)

                    break
            else:
                # If hdr_id does not exist, create a new entry
                new_entry = {
                    'hdr_id'    : item['hdr_id'],
                    'trans_date': item['trans_date'],
                    'details': [{
                        'detl_id' : item['detl_id'],
                        'book_id' : item['book_id'],
                        'type_id' : item['type_id'],
                        'qty'     : item['qty']
                    }]
                }
                data.append(new_entry)


        # ---- 2.
        # grouped_data = {}
        # for item in results:
        #     if item['hdr_id'] not in grouped_data:
        #         grouped_data[item['hdr_id']] = {
        #             'hdr_id'    : item['hdr_id'],
        #             'trans_date': item['trans_date'],
        #             'details'   : []
        #         }

        #     grouped_data[item['hdr_id']]['details'].append({
        #         'detl_id': item['detl_id'],
        #         'book_id': item['book_id'],
        #         'type_id': item['type_id'],
        #         'qty'    : item['qty']
        #     })
        # data = list(grouped_data.values())


        return data
    