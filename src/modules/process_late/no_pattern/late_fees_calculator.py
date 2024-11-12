import datetime
from typing import Dict, Any
from src.services.book_trans_service import BookTransactionService

class LateFeesCalculator():
    def __init__(self):
        pass

    ### model -> {user_id, trans_date, book_id, type_id, qty}
    def calculate(self, late_days: int, models:Dict[Any, Any]):
        late_fee = 0

        if model['type_id'] == 1:       # hard cover
            late_fee = 100
        elif model['type_id'] == 2:     # soft cover
            late_fee = 200
        elif model['type_id'] == 3:     # magazine
            late_fee = 300
        else:                           # letters
            late_fee = 400

        return late_fee
            
