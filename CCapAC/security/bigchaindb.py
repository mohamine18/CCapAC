from bigchaindb_driver import BigchainDB
from CCapAC.admin import bigchaindb_table
import datetime
import sys

#online testing node address (https://test.ipdb.io/)
bdb_root_url = 'http://localhost:9984/'
bdb = BigchainDB(bdb_root_url)

admin_public_key = "9SXGTajcQ4WmmoSVzCvDMPneqGrmcpSYc4Kg71f651Pc"
admin_private_key = "DDzreuu4dQAGhbBqUj3uWWVBD38XJJs5V6WjMwDN4EyT"

rep_public_key = "DDbXro8xWCY5NhzfQ5QWQBmeUDYspt5H3JoPR9RvKTR"
rep_private_key = "33GH7mNR2BsJWMKdu1VbJ8NPe3tByfJXcXeYhJHPyqBB"

class BigchaDb:
    def __init__(self, tx_body=None, tx_type=None):
        self.tx_body = tx_body
        self.tx_type = tx_type

    def create(self):
        asset_tx = {
            "data": {
                'tx_type' : self.tx_type,
                'tx_body' : self.tx_body
            }
        }
        t1 = datetime.datetime.now()
        prepared_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=admin_public_key,
        recipients=[([rep_public_key], 10)],
        asset = asset_tx )
        t2 = datetime.datetime.now()

        t3 = datetime.datetime.now()
        fulfilled_tx = bdb.transactions.fulfill(
            prepared_tx,
            private_keys=admin_private_key)
        t4 = datetime.datetime.now()

        t5 = datetime.datetime.now()
        bdb.transactions.send_commit(fulfilled_tx)
        t6 = datetime.datetime.now()

        print(f"System Tx: {sys.getsizeof(self.tx_body)}")
        print(f"BigchainDB TX: {sys.getsizeof(fulfilled_tx)}")

        txid = fulfilled_tx['id']
        txtype = fulfilled_tx['asset']['data']['tx_type']
        tx = {
            'operation': 'CREATE',
            'tx_type' : txtype,
            'BigDB_id' : txid,
            'prepar_time' : {
                'start': t1.strftime('%M:%S.%f'),
                'finish' : t2.strftime('%M:%S.%f')
            },
            'fulfill_time' : {
                'start':t3.strftime('%M:%S.%f'),
                'finish' : t4.strftime('%M:%S.%f')
            },
            'commit_time' : {
                'start': t5.strftime('%M:%S.%f'),
                'finish' : t6.strftime('%M:%S.%f')
            }
        }
        bigchaindb_table.insert(tx)

    def search(self, text=None):
        return bdb.assets.get(search=text, limit=1)
