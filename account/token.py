from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.timezone import now
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36 


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self , user , timestamp):
        
        return super()._make_hash_value(user , timestamp)

    def make_token(self , user):
       
        timestamp = int(str(now()).replace("-" , "").replace(" " , "").replace(":" , "").replace("." , "").split("+")[0])
       
        return super()._make_token_with_timestamp(user , timestamp)



account_activation_token = AccountActivationTokenGenerator()