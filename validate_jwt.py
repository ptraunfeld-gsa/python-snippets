from dotenv import dotenv_values
import jwt
import requests
import base64

env = dotenv_values(".env")
id_token = env["ID_TOKEN"]
access_token = env["ACCESS_TOKEN"]
client_id = env["CLIENT_ID"]

jwks_url="https://www.googleapis.com/oauth2/v3/certs"
oidc_config_url="https://accounts.google.com/.well-known/openid-configuration"

oidc_config = requests.get(oidc_config_url).json()
signing_algos = oidc_config["id_token_signing_alg_values_supported"]

jwks_client = jwt.PyJWKClient(jwks_url)

signing_key = jwks_client.get_signing_key_from_jwt(id_token)

data = jwt.decode_complete(
    id_token,
    key=signing_key,
    audience=client_id,
    options={"verify_exp": False},
    algorithms=signing_algos
)
header, payload = data["header"], data["payload"]
alg = jwt.get_algorithm_by_name(header["alg"])
digest = alg.compute_hash_digest(access_token.encode("ascii", "ignore"))
d = digest[: (len(digest) // 2)]
at_hash = base64.urlsafe_b64encode(d)
at_hash = at_hash.rstrip(b"=").decode()

if at_hash == payload["at_hash"]:
    print("Match!")
else:
    print("No Match!")
    print(f"{at_hash}\n{payload['at_hash']}")