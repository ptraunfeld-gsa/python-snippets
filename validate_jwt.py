from dotenv import dotenv_values
import jwt
import requests
import base64
import traceback

class AccessTokenHashMismatchError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def _validate_tokens(id_token: str, access_token: str, client_id: str, jwks_client, oidc_config, verify_expiration=True):

    signing_algos = oidc_config["id_token_signing_alg_values_supported"]
    signing_key = jwks_client.get_signing_key_from_jwt(id_token)
    
    data = jwt.decode_complete(
        id_token,
        key=signing_key,
        audience=client_id,
        options={"verify_exp": verify_expiration},
        # options={"verify_exp": verify_expiration, "verify_aud": False},
        algorithms=signing_algos
    )

    header, payload = data["header"], data["payload"]
    alg = jwt.get_algorithm_by_name(header["alg"])
    digest = alg.compute_hash_digest(access_token.encode("ascii", "ignore"))
    d = digest[: (len(digest) // 2)]
    at_hash = base64.urlsafe_b64encode(d)
    at_hash = at_hash.rstrip(b"=").decode()
    # print(f"aud: {payload['aud']}")
    if at_hash != payload["at_hash"]:
        # print(f"at_hash: {at_hash}")
        # print(f"payload[at_hash]: {payload['at_hash']}")
        raise AccessTokenHashMismatchError("Access Token Hash does not match at_hash in the Identity JWT")

def validate_tokens(id_token: str,
    access_token: str,
    client_id: str,
    jwks_url="https://www.googleapis.com/oauth2/v3/certs", 
    oidc_config_url="https://accounts.google.com/.well-known/openid-configuration", 
    verify_expiration=True):

    oidc_config = requests.get(oidc_config_url).json()
    jwks_client = jwt.PyJWKClient(jwks_url)
    _validate_tokens(id_token, access_token, client_id, jwks_client, oidc_config, verify_expiration)


if __name__ == "__main__":
    env = dotenv_values(".env")
    id_token = env["ID_TOKEN"]
    access_token = env["ACCESS_TOKEN"]
    client_id = env["CLIENT_ID"]
    jwks_url="https://www.googleapis.com/oauth2/v3/certs"
    oidc_config_url="https://accounts.google.com/.well-known/openid-configuration"

    try:
        validate_tokens(id_token, access_token, client_id, jwks_url, oidc_config_url, False)
        print("Match!")
    except:
        print("No Match!")