import re

ipv4_cidr_pattern = re.compile(r"^([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\/([0-9]{1,2})$")

class IPv4:
    _octets = []
    def __init__(self, octets):
        self._octets = octets

    def octets(self):
        return self._octets

    def __str__(self):
        return f"{self._octets[0]}.{self._octets[1]}.{self._octets[2]}.{self._octets[3]}"

    def __eq__(self, other):
        if len(self._octets) != len(other.octets()):
            return False
        other_octets = other.octets()
        for i in range(len(self._octets)):
            if self._octets[i] != other_octets[i]:
                return False
        return True


class IPv4CIDR:
    _ip = None
    _mask = 0
    def __init__(self, cidr: str):
        match = ipv4_cidr_pattern.search(cidr)
        if len(match.groups()) < 5:
            raise ValueError(f"Expected IPv4 CIDR in format X.X.X.X/X")
        
        octets = [ int(match[i]) for i in range(1,5) ]
        for octet in octets:
            if octet > 255 or octet < 0:
                raise ValueError(f"Octet out of range: {octet}")
        self._ip = IPv4(octets)
        self._mask = int(match[5])
        if self._mask < 0 or self._mask > 32:
            raise ValueError(f"Mask out of range: {self._mask}")

    def mask(self):
        return self._mask

    def ip(self):
        return self._ip

    def __str__(self):
        return f"{self._ip}/{self._mask}"

class IPv6:
    _chunks = []
    def __init__(self, chunks: list[int]):
        self._chunks = chunks
        while len(self._chunks) < 8:
            self._chunks.append(0)

    def __str__(self):
        return ":".join([ str(f"{chunk:x}") for chunk in self._chunks ])
    
    def chunks(self):
        return self._chunks

    def __eq__(self, other):
        if len(self._chunks) != len(other.chunks()):
            return False
        other_chunks = other.chunks()
        for i in range(len(self._chunks)):
            if self._chunks[i] != other_chunks[i]:
                return False
        return True

class IPv6CIDR:
    _ip = None
    _mask = 0

    def __init__(self, cidr: str):
        parts = cidr.split("/")
        if len(parts) != 2:
            raise ValueError(f"Improperly formatted IPv6 CIDR: {cidr}")
        self._mask = int(parts[1])
        chunks = parts[0].split(":")
        self._ip = IPv6([int(chunk, 16) for chunk in chunks if chunk])
   
    def mask(self):
        return self._mask

    def ip(self):
        return self._ip

    def __str__(self):
        return f"{self._ip}/{self._mask}"
       


def ipv4_to_uint32(ipv4: IPv4) -> int:
    num = 0
    octets = ipv4.octets()
    num = num + ( octets[0] << 24 )
    num = num + ( octets[1] << 16 )
    num = num + ( octets[2] << 8 )
    num = num + octets[3]
    return num

def ipv6_to_uint128(ipv6: IPv6) -> int:
    num = 0
    chunks = ipv6.chunks()
    for i in range(8):
        shifter = 128 - (16*(i+1))
        num = num + ( chunks[0] << shifter )
    return num

def uint32_to_ipv4(num: int) -> IPv4:
    bit_masks = [
        int('11111111000000000000000000000000', 2),
        int('00000000111111110000000000000000', 2),
        int('00000000000000001111111100000000', 2),
        int('00000000000000000000000011111111', 2)
    ]
    shifts = [ 24, 16, 8, 0]
    octets = [0, 0, 0, 0]
    for i in range(4):
        octets[i] = (num & bit_masks[i]) >> shifts[i]
    
    return IPv4(octets)

def uint128_to_ipv6(num: int) -> IPv6:
    bit_masks = []
    shifts = []
    for i in range(8):
        shift = 128 - (16*(i+1))
        shifts.append(shift)
        bit_masks.append(int("ffff", 16) << shift)
    chunks = [0] * 16
    for i in range(8):
        chunks[i] = (num & bit_masks[i]) >> shifts[i]

    return IPv6(chunks)

def cidr_to_ip_range(cidr_str: str) -> (IPv4, IPv4):
    cidr = IPv4CIDR(cidr_str) 
    mask = cidr.mask()
    ip = cidr.ip()
    as_num = ipv4_to_uint32(ip)
    host_bits = 32 - mask
    host_mask = 0
    for i in range(host_bits):
        host_mask = host_mask | 1 << i
    
    subnet_mask = 0
    for i in range(mask):
        subnet_mask = subnet_mask | 1 << i
    
    subnet_mask = subnet_mask << host_bits

    # print(f"host_mask:\t{'{0:032b}'.format(host_mask)}")
    # print(f"subnet_mask:\t{'{0:032b}'.format(subnet_mask)}")

    lower_bound = uint32_to_ipv4(as_num & subnet_mask)
    upper_bound = uint32_to_ipv4(as_num | host_mask)
    return (lower_bound, upper_bound)

def cidr_to_ipv6_range(cidr: str) -> (IPv6, IPv6):
    net = IPv6CIDR(cidr)
    mask = net.mask()
    ip = net.ip()
    as_num = ipv6_to_uint128(ip)
    host_bits = 128 - mask
    host_mask = 0
    for i in range(host_bits):
        host_mask = host_mask | 1 << i

    subnet_mask = 0
    for i in range(mask):
        subnet_mask = subnet_mask | 1 << i

    subnet_mask = subnet_mask << host_bits
    lower_bound = uint128_to_ipv6(as_num & subnet_mask)
    upper_bound = uint128_to_ipv6(as_num | host_mask )
    return (lower_bound, upper_bound)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"{sys.argv[0]} requires argument")
        sys.exit(1)

    if ipv4_cidr_pattern.search(sys.argv[1]):
        low, high = cidr_to_ip_range(sys.argv[1])
    else:
        low, high = cidr_to_ipv6_range(sys.argv[1])
    print(f"{low} - {high}")