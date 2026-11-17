# AERO runtime bytecode

- Contract: Aero (Aerodrome Finance), `0x940181a94a35a4569e4529a3cdfb74e38fd98631` on **Base** (chain id 8453).
- Fetched on 2026-11-17 with one JSON-RPC `eth_getCode` call at Base block 58638827, endpoint https://mainnet.base.org.
- Verified source: Sourcify (exact/partial match), `Aero.sol`, solc 0.8.19+commit.7dd6d404, optimizer on (200 runs), EVM paris. OpenZeppelin 4.8/4.9 ERC20 + ERC20Permit + EIP712.
- Storage layout checked on chain (eth_getStorageAt): slot 2 = total supply, slot 9 = minter (0xeb0183…3fe5, a contract), slot 10 = private owner.
- Cached EIP-712 domain separator in the code (PUSH32 at pc 2733) equals keccak(EIP712Domain, "Aerodrome", "1", 8453, address), recomputed independently.
