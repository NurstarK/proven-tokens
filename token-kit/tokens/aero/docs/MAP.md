# Map of the AERO runtime bytecode (Base)

| index | entry pc | selector | signature | destination | covered by |
|---|---|---|---|---|---|
| 0 | 54 | 0xa457c2d7 | decreaseAllowance(address,uint256) | 584 (0x0248) | paths |
| 1 | 65 | 0xa9059cbb | transfer(address,uint256) | 603 (0x025b) | paths |
| 2 | 76 | 0xd505accf | ? | 622 (0x026e) | NOT covered |
| 3 | 87 | 0xdd62ed3e | allowance(address,address) | 643 (0x0283) | paths |
| 4 | 98 | 0xfca3b5aa | setMinter(address) | 662 (0x0296) | paths |
| 5 | 114 | 0x70a08231 | balanceOf(address) | 489 (0x01e9) | paths |
| 6 | 125 | 0x7ecebe00 | nonces(address) | 530 (0x0212) | paths |
| 7 | 136 | 0x84b0196e | eip712Domain() | 549 (0x0225) | read-only loop |
| 8 | 147 | 0x95d89b41 | symbol() | 576 (0x0240) | read-only loop |
| 9 | 174 | 0x23b872dd | transferFrom(address,address,uint256) | 409 (0x0199) | paths |
| 10 | 185 | 0x313ce567 | decimals() | 428 (0x01ac) | paths |
| 11 | 196 | 0x3644e515 | DOMAIN_SEPARATOR() | 443 (0x01bb) | paths |
| 12 | 207 | 0x39509351 | increaseAllowance(address,uint256) | 451 (0x01c3) | paths |
| 13 | 218 | 0x40c10f19 | mint(address,uint256) | 470 (0x01d6) | paths |
| 14 | 234 | 0x06fdde03 | name() | 283 (0x011b) | read-only loop |
| 15 | 245 | 0x07546172 | minter() | 313 (0x0139) | paths |
| 16 | 256 | 0x095ea7b3 | approve(address,uint256) | 356 (0x0164) | paths |
| 17 | 267 | 0x18160ddd | totalSupply() | 391 (0x0187) | paths |

Instructions: 2736; JUMPDESTs at an opcode boundary: 162.
