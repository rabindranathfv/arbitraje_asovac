from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, arbitro, timestamp):
       
        return (
            six.text_type(arbitro.pk) + six.text_type(timestamp)  + six.text_type(arbitro.cedula_pasaporte)
        )

account_activation_token = AccountActivationTokenGenerator()