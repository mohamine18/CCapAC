from CCapAC.admin import service_table
from tinydb import Query
import datetime

from CCapAC.utils.uuid import generate_uid

import CCapAC.security.bigchaindb as bigch
from bigchaindb_driver import BigchainDB

class Service:
    """
    services creation and other functionality
    """
    def __init__(self, service_name=None, service_init=None, service_issuer=None, sm_number=None, req_quota=None, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        self.service_name = service_name
        self.service_init = service_init
        self.service_issuer = service_issuer
        self.sm_number = sm_number
        self.req_quota = req_quota

    def create_service(self):
        if not self.service_name or not self.service_init or not self.service_issuer or not self.sm_number or not self.req_quota:
            raise ValueError("One of the params is not defined")
        else:
            uuid = generate_uid()
            time = datetime.datetime.now()
            service_dict = {
                "context" : {
                    "id" : uuid,
                    "issuer" : self.service_issuer,
                    "date" : str(time),
                },
                "serviceCredential" : {
                    "name" : self.service_name,
                    "service_init" : self.service_init,
                },
                "metadata" : {
                    "sm_number" : self.sm_number,
                    "req_quota" : self.req_quota,
                }
            }
            exist = self.exist_service()
            if not exist:
                result = service_table.insert(service_dict)
                # Call bigchainDB to create
                bigchaindb_instance = bigch.BigchaDb(tx_body=service_dict, tx_type="SERVICE")
                bigchaindb_instance.create()
            else:
                result = True
            return result

    def edit_service(self):
        pass

    def exist_service(self):
        """
        Check the existence of a service before creation
        :param = service_name
        return a boolean
        """
        return service_table.search(Query().serviceCredential.name == self.service_name)
    
    def get_all(self):
        """
        List of all services used for table representation
        return dict{}
        """
        return service_table.all()

    def delete_service(self):
        pass

    def get_first_service(self):
        services = self.get_all()
        if not services:
            return False
        for service in services:
            return service