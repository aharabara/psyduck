import optparse

import stun
import struct
import socket



FullCone = "Full Cone"  # 0
RestrictNAT = "Restrict NAT"  # 1
RestrictPortNAT = "Restrict Port NAT"  # 2
SymmetricNAT = "Symmetric NAT"  # 3
UnknownNAT = "Unknown NAT"  # 4
NATTYPE = (FullCone, RestrictNAT, RestrictPortNAT, SymmetricNAT, UnknownNAT)


def get_nat_type():
    parser = optparse.OptionParser(version=stun.__version__)
    parser.add_option(
        "-d",
        "--debug",
        dest="DEBUG",
        action="store_true",
        default=False,
        help="Enable debug logging")
    parser.add_option(
        "-H",
        "--host",
        dest="stun_host",
        default=None,
        help="STUN host to use")
    parser.add_option(
        "-P",
        "--host-port",
        dest="stun_port",
        type="int",
        default=3478,
        help="STUN host port to use (default: "
        "3478)")
    parser.add_option(
        "-i",
        "--interface",
        dest="source_ip",
        default="0.0.0.0",
        help="network interface for client (default: 0.0.0.0)")
    parser.add_option(
        "-p",
        "--port",
        dest="source_port",
        type="int",
        default=54320,
        help="port to listen on for client "
        "(default: 54320)")
    (options, args) = parser.parse_args()
    if options.DEBUG:
        stun.enable_logging()
    kwargs = dict(
        source_ip=options.source_ip,
        source_port=int(options.source_port),
        stun_host=options.stun_host,
        stun_port=options.stun_port)
    nat_type, external_ip, external_port = stun.get_ip_info(**kwargs)
    print("NAT Type:", nat_type)
    print("External IP:", external_ip)
    print("External Port:", external_port)
    return nat_type, external_ip, external_port


def bytes2addr(bytes_data):
    """Convert a hash to an address pair."""
    if len(bytes_data) != 8:
        raise ValueError("invalid bytes")
    host = socket.inet_ntoa(bytes_data[:4])
    port = struct.unpack("H", bytes_data[-4:-2])[
        0]  # unpack returns a tuple even if it contains exactly one item
    nat_type_id = struct.unpack("H", bytes_data[-2:])[0]
    target = (host, port)
    return target, nat_type_id
