from cidr_to_range import IPv4, cidr_to_ip_range
import unittest

class TestCidrToIpRange(unittest.TestCase):
    def test_cidr_to_ip_range(self):
        cidr_str = "255.255.255.0/24"
        expected_low = IPv4([255, 255, 255, 0])
        expected_high = IPv4([255, 255, 255, 255])
        low, high = cidr_to_ip_range(cidr_str)

        self.assertEqual(expected_low, low)
        self.assertEqual(expected_high, high)


    def test_cidr_to_ip_range2(self):
        cidr_str = "255.255.255.0/25"
        expected_low = IPv4([255, 255, 255, 0])
        expected_high = IPv4([255, 255, 255, 127])
        low, high = cidr_to_ip_range(cidr_str)

        self.assertEqual(expected_low, low)
        self.assertEqual(expected_high, high)


    def test_cidr_to_ip_range3(self):
        cidr_str = "255.255.255.128/25"
        expected_low = IPv4([255, 255, 255, 128])
        expected_high = IPv4([255, 255, 255, 255])
        low, high = cidr_to_ip_range(cidr_str)

        self.assertEqual(expected_low, low)
        self.assertEqual(expected_high, high)


if __name__ == "__main__":
    unittest.main()
