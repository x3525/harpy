"""This file contains constants."""

###########
# Request #
###########
UA = 'Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0'

############
# Argument #
############
DEFAULT_OCTET = 43
DEFAULT_SLEEP = 1

##########
# Socket #
##########
GGP = 3  # https://www.iana.org/assignments/protocol-numbers
PORT = 0  # auto

##########
# Packet #
##########
FMT_ETH = '!6s6s2s'
FMT_ARP = '!2s2s1s1s2s6s4s6s4s'

##########
# Thread #
##########
WAIT_PRINT = 1
WAIT_BLOCK = .001

############
# Terminal #
############
CLS = '\x1b[H\x1b[2J\x1b[3J'  # https://en.wikipedia.org/wiki/ANSI_escape_code
LOGO = (
    r'|_  _  _ _   ',
    r'| |(_|| |_)\/',
    r'        |  / ',
)
