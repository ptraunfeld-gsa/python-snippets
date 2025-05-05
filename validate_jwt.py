from dotenv import dotenv_values
import jwt
import requests
import base64

def _valid_tokens(id_token: str, access_token: str, client_id: str, jwks_client, oidc_config, verify_expiration=True) -> bool:

    signing_algos = oidc_config["id_token_signing_alg_values_supported"]
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(id_token)
    except jwt.exceptions.DecodeError as decodeError:
        print(f"{decodeError}") 
        return False

    try:
        data = jwt.decode_complete(
            id_token,
            key=signing_key,
            audience=client_id,
            options={"verify_exp": verify_expiration},
            algorithms=signing_algos
        )
    except jwt.exceptions.ExpiredSignatureError as e:
        print(f"{e}")
        return False

    header, payload = data["header"], data["payload"]
    alg = jwt.get_algorithm_by_name(header["alg"])
    digest = alg.compute_hash_digest(access_token.encode("ascii", "ignore"))
    d = digest[: (len(digest) // 2)]
    at_hash = base64.urlsafe_b64encode(d)
    at_hash = at_hash.rstrip(b"=").decode()

    return at_hash == payload["at_hash"]

def valid_tokens(id_token: str, 
    access_token: str, 
    client_id: str, 
    jwks_url="https://www.googleapis.com/oauth2/v3/certs", 
    oidc_config_url="https://accounts.google.com/.well-known/openid-configuration", 
    verify_expiration=True) -> bool:

    oidc_config = requests.get(oidc_config_url).json()
    jwks_client = jwt.PyJWKClient(jwks_url)
    return _valid_tokens(id_token, access_token, client_id, jwks_client, oidc_config, verify_expiration)


if __name__ == "__main__":
    env = dotenv_values(".env")
    id_token = env["ID_TOKEN"]
    access_token = env["ACCESS_TOKEN"]
    client_id = env["CLIENT_ID"]
    jwks_url="https://www.googleapis.com/oauth2/v3/certs"
    oidc_config_url="https://accounts.google.com/.well-known/openid-configuration"

    are_valid = valid_tokens(id_token, access_token, client_id, jwks_url, oidc_config_url, False)

    if are_valid:
        print("Match!")
    else:
        print("No Match!")