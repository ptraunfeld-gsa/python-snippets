import json
from pathlib import Path
from ipaddress import IPv4Network, IPv4Address, IPv6Network, IPv6Address
from cidr_to_range import cidr_to_ip_range
from dataclasses import dataclass
from typing import Iterator

@dataclass
class Subnet:
    name: str
    access_type: str
    cidr: IPv4Network
    low: IPv4Address
    high: IPv4Address
    available_ip_count: int

def get_subnets(subnets: dict, vpc_id: str) -> Iterator[Subnet]:
    # print("Name,AccessType,Cidr,Low,High,IPs Available")
    for subnet in filter(lambda x: x['VpcId'] == vpc_id, subnets['Subnets']):
        name_tags = [ tag['Value'] for tag in subnet['Tags'] if tag['Key'] == 'Name']
        name = name_tags[0] if name_tags else ""
        access_type_tags = [ tag['Value'] for tag in subnet['Tags'] if tag['Key'] == 'AccessType']
        access_type = access_type_tags[0] if access_type_tags else ""
        cidr = subnet['CidrBlock']
        low, high = cidr_to_ip_range(cidr)
        available_ip_count = subnet['AvailableIpAddressCount']
        s = Subnet(
                name=name,
                access_type=access_type,
                cidr=IPv4Network(cidr),
                low=IPv4Address(low), 
                high=IPv4Address(high), 
                available_ip_count=available_ip_count
            )
        yield s
        # print(f"{name},{access_type},{cidr},{low},{high},{available_ip_count}")

def get_ipv6_cidr_blocks(subnets: dict, vpc_id: str) -> Iterator[str]: 
    for subnet in filter(lambda x: x['VpcId'] == vpc_id, subnets['Subnets']):
        if 'Ipv6CidrBlockAssociationSet' in subnet and subnet['Ipv6CidrBlockAssociationSet']:
            yield subnet['Ipv6CidrBlockAssociationSet'][0]['Ipv6CidrBlock']


def subnets_to_csv(subnets: dict, vpc_id: str):
    print("Name,AccessType,Cidr,Low,High,IPs Available")
    for s in get_subnets(subnets, vpc_id):
        print(f"{s.name},{s.access_type},{s.cidr},{s.low},{s.high},{s.available_ip_count}")

def find_unused_subnets(vpc_cidr: str, subnet_cidrs: list[Subnet], subnet_mask_size: int = 24) -> list[str]:
    vpc_network = IPv4Network(vpc_cidr)
    used_networks = { s.name: IPv4Network(s.cidr) for s in subnet_cidrs }
    possible_subnets = list(vpc_network.subnets(new_prefix=subnet_mask_size))
    unused_subnets = []
    for possible in possible_subnets:
        is_free = True
        for name,used in used_networks.items():
            if possible.overlaps(used):
                # print(f"Overlap with {name}")
                is_free = False
                break
        if is_free:
            unused_subnets.append(possible)
    
    return unused_subnets

def find_unused_subnets_ipv6(vpc_cidr: str, subnet_cidrs: list[str], subnet_mask_size: int = 64) -> list[str]:
    vpc_network = IPv6Network(vpc_cidr)
    used_networks = [ IPv6Network(s) for s in subnet_cidrs ]
    possible_subnets = list(vpc_network.subnets(new_prefix=subnet_mask_size))
    unused_subnets = []
    for possible in possible_subnets:
        is_free = True
        for used in used_networks:
            if possible.overlaps(used):
                is_free = False
                break
        if is_free:
            unused_subnets.append(possible)
    
    return unused_subnets



if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        subnets_json = json.load(sys.stdin)
    else:
        subnets_file = Path(sys.argv[1])
        if not subnets_file.exists():
            print(f"{subnets_file} does not exit")
            sys.exit(1)
        with open(subnets_file, 'r') as f:
            subnets_json = json.load(f)

    # subnets_to_csv(subnets_json)

    # Dev
    vpc_id='vpc-685a670f'
    vpc_cidr='10.177.112.0/24'
    # vpc_cidr='10.56.250.0/23'
    # vpc_ipv6_cidr='2600:1f28:40:4e00::/56'
    
    # prod
    # vpc_id = 'vpc-92898bf7'
    # vpc_cidr='10.176.16.0/20'
    # vpc_cidr='10.190.128.0/22'
    # vpc_cidr='10.42.56.0/22'
    # vpc_ipv6_cidr='2600:1f28:45:1100::/56'
    subnet_mask_size=28
    # subnet_cidrs = [ s['CidrBlock'] for s in subnets_json['Subnets'] ]
    subnets = [ s for s in get_subnets(subnets_json, vpc_id=vpc_id) ]
    # print(f"Subnet CIDRs:{'\n'.join(subnet_cidrs)}")
    unused_subnets = find_unused_subnets(vpc_cidr, subnets, subnet_mask_size)
    
    # subnets = [ s for s in get_ipv6_cidr_blocks(subnets_json, vpc_id=vpc_id) ]
    # unused_subnets = find_unused_subnets_ipv6(vpc_ipv6_cidr, subnets)
    print("Unused:")
    # for s in unused_subnets:
    #     low,high = cidr_to_ip_range(f"{s}")
    #     print(f"{s} ({low} - {high})") 
    for s in unused_subnets:
        print(f"{s}")