from CCapAC.admin import statement_table
from tinydb import Query
import datetime

import CCapAC.security.asset as asset
import CCapAC.security.profile as profile
from CCapAC.utils.uuid import generate_uid

class Statement:
    def __init__(self, st_issuer=None, st_action=None, st_profile_id=None):
        self.st_issuer = st_issuer
        self.st_action = st_action
        self.st_profile_id = st_profile_id

    def create_statement(self):
        if not self.st_action or not self.st_issuer or not self.st_profile_id:
            raise ValueError('params missing')
        
        sid = generate_uid()
        time = datetime.datetime.now()

        profile_instance = profile.Profile()
        asset_id = profile_instance.profile_asset_id(self.st_profile_id)

        asset_instance = asset.Asset()
        resource_uri = asset_instance.resource_uri(asset_id)

        if not asset_id or not resource_uri:
            raise ValueError('The asset id or resource uri are invalid')

        statement_dict = {
            "context": {
                "sid" : sid,
                "issuer" : self.st_issuer,
                "time" : str(time),
                "principal" : sid,
            },
            "statementCredential" : {
                "profile_id" : self.st_profile_id,
                "action" : self.st_action,
                "uri" : resource_uri,
            }
        }
        exist = self.exist_statement()
        if not exist:
            result = statement_table.insert(statement_dict)
        else:
            result = True
        return result

    def exist_statement(self):
        """
        Check the existence of a statement before insertion
        :param = profile_id
        return a boolean
        """
        return statement_table.search(Query().statementCredential.profile_id == self.st_profile_id)
    
    def edit_statement(self):
        pass
    
    def get_all(self):
        """
        List of all statements used for table representation
        return dict{}
        """
        return statement_table.all()