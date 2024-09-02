"""Command-line interface."""

import argparse

import harpy
from harpy.consts import DEFAULT_OCTET, DEFAULT_SLEEP
from harpy.custom import device, ipv4
from harpy.utils import get_devices


class Namespace(argparse.Namespace):
    """Simple object for storing attributes."""

    def __call__(self) -> str:
        """Get currently active modes."""
        return ''.join(k for k, v in vars(self).items() if len(k) == 1 and v)


parser = argparse.ArgumentParser(
    prog='harpy',
    description='%(prog)s - active/passive arp discovery tool',
    formatter_class=argparse.RawTextHelpFormatter,
)

modes = parser.add_argument_group('modes')

mutual = modes.add_mutually_exclusive_group()

###############
# Positionals #
###############
parser.add_argument('range', type=ipv4, help='ip range in cidr format')

###########
# Options #
###########
parser.add_argument(
    '-D',
    action='store_true',
    help='create/update the manufacturer database',
    dest='db',
)
parser.add_argument(
    '-i',
    default=next(iter(devices := get_devices()), ''),
    type=device,
    choices=devices,
    help='use %(metavar)s as network device (default: %(default)s)',
    metavar='DEVICE',
    dest='device',
)
parser.add_argument(
    '-n',
    default=DEFAULT_OCTET,
    type=int,
    choices=range(2, 254),
    help='use %(metavar)s as last ip octet for sending (default: %(default)s)',
    metavar='NODE',
    dest='node',
)
parser.add_argument(
    '-s',
    default=DEFAULT_SLEEP,
    type=int,
    help='sleep %(metavar)s ms between each request (default: %(default)s)',
    metavar='TIME',
    dest='sleep',
)
parser.add_argument(
    '-V',
    action='version',
    help='show program version and exit',
    version=harpy.VERSION,
)

##################
# Options: Modes #
##################
modes.add_argument(
    '-f',
    action='store_true',
    help='enable fast mode, only scan specific hosts',
    dest='f',
)
modes.add_argument(
    '-F',
    action='store_true',
    help='enable filter mode, exclude hosts not in range',
    dest='F',
)
mutual.add_argument(
    '-p',
    action='store_true',
    help='enable passive mode, do not send any packets',
    dest='p',
)
mutual.add_argument(
    '-R',
    action='store_true',
    help='enable continuous mode, never stop sending packets',
    dest='R',
)
modes.add_argument(
    '-S',
    action='store_true',
    help='enable strict mode, treat inconsistent packets as new',
    dest='S',
)
