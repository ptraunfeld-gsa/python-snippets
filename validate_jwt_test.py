import unittest
from dotenv import dotenv_values
from validate_jwt import valid_tokens

class TestValidateJwt(unittest.TestCase):

    def test_validate_jwt_valid_no_verify_exp(self):
        env = dotenv_values(".env")
        id_token = env["ID_TOKEN"]
        access_token = env["ACCESS_TOKEN"]
        client_id = env["CLIENT_ID"]
        jwks_url="https://www.googleapis.com/oauth2/v3/certs"
        oidc_config_url="https://accounts.google.com/.well-known/openid-configuration"
        result = valid_tokens(id_token, access_token, client_id, jwks_url, oidc_config_url, False)
        self.assertTrue(result)

    def test_validate_jwt_invalid_expired(self):
        env = dotenv_values(".env")
        id_token = env["ID_TOKEN"]
        access_token = env["ACCESS_TOKEN"]
        client_id = env["CLIENT_ID"]
        jwks_url="https://www.googleapis.com/oauth2/v3/certs"
        oidc_config_url="https://accounts.google.com/.well-known/openid-configuration"
        result = valid_tokens(id_token, access_token, client_id, jwks_url, oidc_config_url, True)
        self.assertFalse(result)


    def test_validate_jwt_invalid_token(self):
        env = dotenv_values(".env")
        id_token = env["BAD_ID_TOKEN"]
        access_token = env["ACCESS_TOKEN"]
        client_id = env["CLIENT_ID"]
        jwks_url="https://www.googleapis.com/oauth2/v3/certs"
        oidc_config_url="https://accounts.google.com/.well-known/openid-configuration"
        result = valid_tokens(id_token, access_token, client_id, jwks_url, oidc_config_url, False)
        self.assertFalse(result)

   


