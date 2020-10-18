from CCapAC.admin import profile_table
from tinydb import Query
import datetime

from CCapAC.utils.uuid import generate_uid

import CCapAC.security.bigchaindb as bigch
from bigchaindb_driver import BigchainDB

class Profile:
    def __init__(self, asset_id=None, service_id=None, profile_issuer=None):
        self.asset_id = asset_id
        self.service_id = service_id
        self.profile_issuer = profile_issuer

    def create_profile(self):
        if not self.asset_id or not self.service_id or not self.profile_issuer:
            raise ValueError('Profile information is missing')
        else:
            uuid = generate_uid()
            time = datetime.datetime.now()
            profile_dict = {
                "context" : {
                    "id" : uuid,
                    "issuer" : self.profile_issuer,
                    "date" : str(time),
                },
                "profileCredential" : {
                    "asset_id" : self.asset_id,
                    "service_id" : self.service_id,
                },
            }
            exist = self.exist_profile()
            if not exist:
                result = profile_table.insert(profile_dict)
                # Call bigchainDB to create
                bigchaindb_instance = bigch.BigchaDb(tx_body=profile_dict, tx_type="PROFILE")
                bigchaindb_instance.create()
            else:
                result = True
            return result

    def exist_profile(self):
        """
        Check the existence of an asset before insertion
        :param = asset_id
        :param = service_id
        return a boolean
        """
        Profile = Query()
        return profile_table.search((Profile.profileCredential.asset_id == self.asset_id) & (Profile.profileCredential.service_id == self.service_id))

    def get_all(self):
        """
        List of all assets used for table representation
        return dict{}
        """
        return profile_table.all()

    def edit_profile(self):
        pass

    def delete_profile(self):
        pass

    def service_assets_profiles(self, service_id):
        profiles = profile_table.search(Query().profileCredential.service_id == service_id)
        if not profiles:
            return False
        return profiles

    def profile_asset_id(self, profile_id):
        asset_id = profile_table.search(Query().context.id == profile_id)
        if not asset_id:
            return False
        return asset_id
