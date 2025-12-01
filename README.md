# EVM From Scratch - Python Implementation

A from-scratch implementation of the Ethereum Virtual Machine in Python, built as part of the [EVM From Scratch](https://github.com/w1nt3r-eth/evm-from-scratch) project.

## About

This is my personal implementation of the EVM specification, written entirely in Python without relying on existing EVM libraries. The goal is to deeply understand how the EVM works by implementing each opcode and mechanism from first principles.

## Current Progress

**137 out of 152 tests passing** ✓

### Implemented Features

#### Stack Operations

- `PUSH0` through `PUSH32` - Push operations
- `POP` - Remove from stack
- `DUP1` through `DUP16` - Duplicate stack items
- `SWAP1` through `SWAP16` - Swap stack items

#### Arithmetic Operations

- `ADD`, `SUB`, `MUL`, `DIV`, `MOD` - Basic arithmetic
- `ADDMOD`, `MULMOD` - Modular arithmetic
- `EXP` - Exponentiation
- `SIGNEXTEND` - Sign extension
- `SDIV`, `SMOD` - Signed division and modulo

#### Comparison & Bitwise Operations

- `LT`, `GT`, `SLT`, `SGT` - Comparison operations
- `EQ`, `ISZERO` - Equality checks
- `AND`, `OR`, `XOR`, `NOT` - Bitwise operations
- `SHL`, `SHR`, `SAR` - Shift operations
- `BYTE` - Byte extraction

#### Memory Operations

- `MSTORE`, `MSTORE8` - Store to memory
- `MLOAD` - Load from memory
- `MSIZE` - Get memory size

#### Storage Operations

- `SSTORE` - Store to persistent storage
- `SLOAD` - Load from storage

#### Control Flow

- `JUMP`, `JUMPI` - Jump operations
- `JUMPDEST` - Jump destination marker
- `PC` - Program counter
- `STOP` - Halt execution
- `INVALID` - Invalid opcode

#### Environmental Information

- `ADDRESS`, `CALLER`, `ORIGIN` - Account information
- `BALANCE`, `SELFBALANCE` - Balance queries
- `CALLVALUE` - ETH value sent
- `GASPRICE`, `BASEFEE`, `GASLIMIT` - Gas information
- `COINBASE`, `TIMESTAMP`, `NUMBER` - Block information
- `DIFFICULTY`, `CHAINID`, `BLOCKHASH` - Chain information

#### Call Data Operations

- `CALLDATALOAD`, `CALLDATASIZE`, `CALLDATACOPY` - Access call data

#### Code Operations

- `CODESIZE`, `CODECOPY` - Contract code access
- `EXTCODESIZE`, `EXTCODECOPY`, `EXTCODEHASH` - External code access

#### Logging

- `LOG0` through `LOG4` - Event logging

#### Cryptographic Operations

- `SHA3` (KECCAK256) - Hashing

#### In Progress

- `RETURN` - Return data from execution

## Project Structure

```
evm-from-scratch/
├── evm.json              # Test specifications
├── python/               # Python implementation
│   └── evm.py           # Main EVM implementation
└── README.md            # This file
```

## Running Tests

```bash
# Run all tests
cd python
python evm.py

# Tests are defined in evm.json and automatically executed
```

## Implementation Notes

- **Language**: Pure Python 3
- **Dependencies**: None (standard library only)
- **Architecture**: Single-file implementation for clarity
- **Testing**: Uses the standardized test suite from evm.json

## Learning Resources

This implementation follows the [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf) specification and draws from:

- EVM Opcodes reference: [evm.codes](https://www.evm.codes/)
- Ethereum execution specs
- The original EVM From Scratch challenge materials

## Acknowledgments

Built as part of the [EVM From Scratch](https://github.com/w1nt3r-eth/evm-from-scratch) project by [@w1nt3r-eth](https://github.com/w1nt3r-eth).
