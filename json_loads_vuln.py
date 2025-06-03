import json

class UntrustedData():
    pass

untrusted_str = """{
    "name": "Untrusted Data",
    "__class__": "__main__.UntrustedData", 
    "__init__":"f=open('a.txt', 'w'); f.write('abcdefg'); f.close()"
}
"""

def main():
    print(f"Deserializing:\n{untrusted_str}")
    json_dict = json.loads(untrusted_str)

if __name__ == "__main__":
    main()