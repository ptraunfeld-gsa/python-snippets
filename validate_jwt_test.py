import unittest
from unittest.mock import patch, MagicMock, Mock
from dotenv import dotenv_values
from validate_jwt import validate_tokens
import json
import requests
import jwt

oidc_config_json = """
{
    "issuer": "https://accounts.google.com",
    "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
    "device_authorization_endpoint": "https://oauth2.googleapis.com/device/code",
    "token_endpoint": "https://oauth2.googleapis.com/token",
    "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
    "revocation_endpoint": "https://oauth2.googleapis.com/revoke",
    "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
    "response_types_supported": [
        "code",
        "token",
        "id_token",
        "code token",
        "code id_token",
        "token id_token",
        "code token id_token",
        "none"
    ],
    "subject_types_supported": [
        "public"
    ],
    "id_token_signing_alg_values_supported": [
        "RS256"
    ],
    "scopes_supported": [
        "openid",
        "email",
        "profile"
    ],
    "token_endpoint_auth_methods_supported": [
        "client_secret_post",
        "client_secret_basic"
    ],
    "claims_supported": [
        "aud",
        "email",
        "email_verified",
        "exp",
        "family_name",
        "given_name",
        "iat",
        "iss",
        "name",
        "picture",
        "sub"
    ],
    "code_challenge_methods_supported": [
        "plain",
        "S256"
    ],
    "grant_types_supported": [
        "authorization_code",
        "refresh_token",
        "urn:ietf:params:oauth:grant-type:device_code",
        "urn:ietf:params:oauth:grant-type:jwt-bearer"
    ]
}
"""
oidc_config_response = requests.Response()
oidc_config_response.json = Mock(return_value=json.loads(oidc_config_json))

decoded_token_data = {   
    "payload": {
        "at_hash": "KPVjQMq_V0nIYVq7OaLakQ",
        "exp": 1746214395
    },
    "header": {
        "alg": "RS256",
        "kid": "660ef3b9784bdf56ebe859f577f7fb2e8c1ceffb",
        "typ": "JWT"
    }
}

# jwk_data = {
#     "kid": "07b80a365428525f8bf7cd0846d74a8ee4ef3625", 
#     "n": r"03Cww27F2O7JxB5Ji9iT9szfKZ4MK-iPzVpQkdLjCuGKfpjaCVAz9zIQ0-7gbZ-8cJRaSLfByWTGMIHRYiX2efdjz1Z9jck0DK9W3mapFrBPvM7AlRni4lPlw\\UigDd8zxAMDCheqyK3vCOLFW-1xYHt_YGwv8b0dP7rjujarEYlWjeppO_QMNtXdKdT9eZtBEcj_9ms9W0aLdCFNR5AAR3y0kLkKR1H4DW7vncB46rqCJLenhlCbcW0MZ3asqcjqBQ2t9QMRnY83Zf_pNEsCcXlKp4uOQqEvzjAc9ZSr2sOmd_ESZ_3jMlNkCZ4J41TuG-My5i\\llFcW5LajSKvxD3w", 
#     "alg": "RS256", 
#     "kty": "RSA", 
#     "use": "sig", 
#     "e": "AQAB"
# }
jwk_data = {
    "kid": "660ef3b9784bdf56ebe859f577f7fb2e8c1ceffb",
    "alg": "RS256",
    "n": r"reAiA0pMszU7kbDpPS_zEUt3GSvs1nEgXdydY4mEoQvvGtyP9t48KzyE4MNQIEvH-HaanUREEfA_FRH5Ybgbkdp4XPA-1EZ-CeykXX_8MeKUoUPI7wxkEsNiK4vNOVGm1kvenMO4YzbU9AUmOVyAnBPgaza3hlxchyIjGUZVytetMtvr_VWQgBgicdwotVCc4PjOU8rCRl7RMldrVXV98H2zWev1ZAfLYLYE_NxqGfIbWxqZToX30eNrbyvJe4OjXc_jyK136KpC5rB9rKUhH3XFW7TSRIT5ZpibwZnipT34qErW1emj5Wg5mTEb2QjS9QmdEjmDvk_RgLb4v3Cn_Q",
    "e": "AQAB",
    "use": "sig",
    "kty": "RSA"
}
test_signing_key = jwt.PyJWK(jwk_data, 'RS256')

class TestValidateJwt(unittest.TestCase):

    @patch("jwt.decode_complete", return_value=decoded_token_data)
    @patch("requests.get", return_value=oidc_config_response)
    # @unittest.skip("skip for now")
    def test_validate_jwt1(self, mock_get, mock_decode):
        env = dotenv_values(".env")
        id_token = env["ID_TOKEN"]
        access_token = env["ACCESS_TOKEN"]
        client_id = env["CLIENT_ID"]
        jwks_url="https://www.googleapis.com/oauth2/v3/certs"
        # oidc_config_url="https://accounts.google.com/.well-known/openid-configuration"
        oidc_config_url="https://example.com/.well-known/openid-configuration"
        with patch.object(jwt.PyJWKClient, 'get_signing_key_from_jwt', return_value=test_signing_key) as mock_get_signing_key:
            validate_tokens(id_token, access_token, client_id, jwks_url, oidc_config_url, False)
        
        # self.assertTrue(result)


    def test_validate_jwt_valid_no_verify_exp(self):
        env = dotenv_values(".env")
        id_token = env["ID_TOKEN"]
        access_token = env["ACCESS_TOKEN"]
        client_id = env["CLIENT_ID"]
        jwks_url="https://www.googleapis.com/oauth2/v3/certs"
        oidc_config_url="https://accounts.google.com/.well-known/openid-configuration"
        validate_tokens(id_token, access_token, client_id, jwks_url, oidc_config_url, False)

    @unittest.skip
    def test_validate_jwt_invalid_expired(self):
        env = dotenv_values(".env")
        id_token = env["ID_TOKEN"]
        access_token = env["ACCESS_TOKEN"]
        client_id = env["CLIENT_ID"]
        jwks_url="https://www.googleapis.com/oauth2/v3/certs"
        oidc_config_url="https://accounts.google.com/.well-known/openid-configuration"
        with self.assertRaises(jwt.exceptions.ExpiredSignatureError):
            validate_tokens(id_token, access_token, client_id, jwks_url, oidc_config_url, True)


    def test_validate_jwt_invalid_token(self):
        env = dotenv_values(".env")
        id_token = env["BAD_ID_TOKEN"]
        access_token = env["ACCESS_TOKEN"]
        client_id = env["CLIENT_ID"]
        jwks_url="https://www.googleapis.com/oauth2/v3/certs"
        oidc_config_url="https://accounts.google.com/.well-known/openid-configuration"
        with self.assertRaises(jwt.exceptions.InvalidTokenError):
            validate_tokens(id_token, access_token, client_id, jwks_url, oidc_config_url, False)

    # @unittest.skip
    def test_validate_jwt_no_client_id(self):
        env = dotenv_values(".env")
        id_token = env["ID_TOKEN"]
        access_token = env["ACCESS_TOKEN"]
        client_id = env["CLIENT_ID"]
        jwks_url="https://www.googleapis.com/oauth2/v3/certs"
        oidc_config_url="https://accounts.google.com/.well-known/openid-configuration"
        validate_tokens(id_token, access_token, None, jwks_url, oidc_config_url, False)

