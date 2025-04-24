from enum import StrEnum

class RequestType(StrEnum):
    CLIENT_SERVER = "Client/Server"
    CHROME_EXTENSION = "Chrome Extension"


def process_request(request_type: RequestType):
    print(f"{request_type} has to be valid")


process_request(RequestType.CLIENT_SERVER) # Guaranteed to be valid parameter; 
process_request(RequestType.OOPS_TYPO) # otherwise, invalid syntax error caught by static type checker/linter


def process_request_str(request_type: str):
    if request_type not in ("Client/Server", "Chrome Extension"):
        raise RuntimeError("Invalid request type!")
    print(f"{request_type} is probably valid")


process_request_str("Chrome Extension")
process_request_str("Chrome extension") # Valid syntax, but typo will cause error at runtime