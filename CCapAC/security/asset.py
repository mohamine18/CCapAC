from CCapAC.admin import asset_table
from tinydb import Query
import datetime

from CCapAC.utils.uuid import generate_uid

class Asset:
    """
    Asset Service provides resource management functionalities.
    """
    def __init__(self, entity_owner=None, entity_id=None, entity_type=None, asset_issuer=None, entity_uri=None, entity_func=None, *args, **kwargs):
        super(Asset, self).__init__(*args, **kwargs)
        self.entity_owner = entity_owner
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.asset_issuer = asset_issuer
        self.entity_uri = entity_uri
        self.entity_func = entity_func

    def create_asset(self):
        """
        Create assets
        """
        if not self.entity_owner or not self.entity_id or not self.entity_type or not self.asset_issuer or not self.entity_uri or not self.entity_func:
            raise ValueError("One of the params is not defined")
        else:
            uid = generate_uid()
            time = datetime.datetime.now()
            asset_dict = {
                "context" : {
                    "uid" : uid,
                    "issuer" : self.asset_issuer,
                    "date" : str(time),
                }, 
                "entityCredential" : {
                    "id" : self.entity_id,
                    "owner" : self.entity_owner,
                    "type" : self.entity_type,
                    "uri" : self.entity_uri,
                },
                "entityMetadata" : {
                    "func" : self.entity_func,
                }
            }
            exist = self.exist()
            if not exist:
                result = asset_table.insert(asset_dict)
            else:
                result = True
            return result
            
    def exist(self):
        """
        Check the existence of an asset before insertion
        :param = entity_id
        return a boolean
        """
        return asset_table.search(Query().entityCredential.id == self.entity_id)

    def get_all(self):
        """
        List of all assets used for table representation
        return dict{}
        """
        return asset_table.all()

    def delete(self):
        pass
    
    def resource_uri(self, uuid):
        asset = asset_table.search(Query().context.uid == uuid)
        if not asset:
            return False
        asset_id = asset[0]['entityCredential']['uri']
        print(asset_id)
        return asset_id
