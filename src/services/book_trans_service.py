from datetime import datetime
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
            select t1.id as id, t1.trans_date as trans_date, t3.id as user_id, t3.name, t3.email, t1.rent_days, t1.total_amt, 
                t5.description, t6.description 
                from book_trans_hdr t1
                    left join book_trans_detl t2 on t1.id = t2.hdr_id
                    left join users t3 on t1.user_id = t3.id
                    left join books t4 on t2.book_id = t4.id
                    left join book_types t5 on t2.type_id = t5.id
                    left join book_categories t6 on t4.category_id = t6.id
                where t1.id = %s
        """,(id,))
        result = cursor.fetchall()
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


    def get_invoices(self):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("""
            select t1.id as recipt_id, t1.inv_date as inv_date, t1.user_id as user_id, t2.name as name
                from book_receipts t1
                        left join users t2 on t1.user_id = t2.id
                        left join book_trans_hdr t3 on t1.ref_id = t3.id
        """)


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
    
    
    def get_late_trans(self):
        cursor = self.dbcnx.cursor(dictionary=True)

        cursor.execute("""
            select t1.id as hdr_id, t1.user_id as user_id, t1.trans_date as trans_date, t1.rent_days as rent_days, t1.total_amt as total_amt,
                    t2.id as detl_id, t2.book_id as book_id, t2.type_id as type_id, t2.book_qty as qty   
                        from book_trans_hdr t1
                            left join book_trans_detl t2 on t1.id = t2.hdr_id
                    where t1.status = 1
        """)

        results = cursor.fetchall()
        cursor.close()

        # result =>
        # [
        #   {hdr_id: 1, user_id: 1, trans_date: '2024-01-01', detl_id: 1, book_id: 1, type_id: 2, qty: 3},
        #   {hdr_id: 1, user_id: 1, trans_date: '2024-01-01', detl_id: 2, book_id: 2, type_id: 1, qty: 4},
        #   {hdr_id: 2, user_id: 1, trans_date: '2024-01-01', detl_id: 1, book_id: 2, type_id: 2, qty: 5}
        # ]


        # ------ convert result to dict with list of books dict and details =>
        # [
        #   {
        #       hdr_id: 1,
        #       user_id: 1,
        #       rent_days: 3,
        #       trans_date: '2024-01-01',
        #       details:[
        #           {detl_id: 1, book_id: 1, type_id: 2, qty: 3},
        #           {detl_id: 2, book_id: 2, type_id: 1, qty: 4}
        #       ]
        #   },
        #   {
        #       hdr_id: 2,
        #       user_id: 1,
        #       rent_days:3,
        #       trans_date: '2024-01-01',
        #       details:[
        #           {detl_id: 1, book_id: 2, type_id, 2, qty: 2}
        #       ] 
        #   }
        #]
        # ---- 1. simple for.next loop
        data = []

        for item in results:
            # Check if the hdr_id already exists in the result
            for entry in data:
                if entry['hdr_id'] == item['hdr_id']:
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
                    'user_id'   : item['user_id'],
                    'rent_days' : item['rent_days'],
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
    

    def process_late_fees(self):
        late_trans = self.get_late_trans()

        late_list = []
        late_fees = 0
        for trans in late_trans:

            # trans_date = datetime.strptime(trans['trans_date'], '%Y-%m-%d %H:%M:%S')
            
            # ======= t r a n s ['t r a n s _ d a t e'] is a DATETIME object ======== #
            # *********************************************************************** #
            days_rented = datetime.now() - trans['trans_date']
            days_rented = days_rented.days

            if days_rented < trans['rent_days']: continue

            fees = 0
            late_days = days_rented - trans['rent_days']
            for book in trans['details']:
                if book['type_id'] == 1:            # hard cover
                    fees += late_days * 1.20
                elif book['type_id'] == 2:          # soft cover
                    fees += late_days * 1.20
                elif book['type_id'] == 3:          # magazine
                    fees += late_days * 1.20
                else:                               # letters
                    fees += late_days * 1.20
                           
            late_list.append({
                "hdr_id": trans['hdr_id'],
                "user_id": trans['user_id'],
                "fees": fees
            })            

        return late_list
    