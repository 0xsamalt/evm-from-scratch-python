#!/usr/bin/env python3

# EVM From Scratch
# Python template
#
# To work on EVM From Scratch in Python:
#
# - Install Python3: https://www.python.org/downloads/
# - Go to the `python` directory: `cd python`
# - Edit `evm.py` (this file!), see TODO below
# - Run `python3 evm.py` to run the tests

import json
import os

from eth_hash.auto import keccak
INT_MAX = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

def evm(code, tranx, sts):
    pc = 0
    success = True
    stack = []
    memo = bytearray()
    tx = tranx
    state = sts
    storage = {}

    while pc < len(code):
        op = code[pc]
        pc += 1

        # TODO: implement the EVM here!
        if op == 0x5f :
            stack.append(0)

        if op == 0x50:
            stack.pop(0)

        if op == 0x00:
            break

        if op == 0x01:
            a = stack.pop()
            b = stack.pop()
            c = a+b
            
            if c > INT_MAX :
                d = c % INT_MAX 
                stack.insert(0,d - 1) #after overflow the count starts from 0
            else:
                stack.insert(0,c)
        
        #MUL
        if op == 0x02:
            a = stack.pop()
            b = stack.pop()

            c = a*b
            if c > INT_MAX:
                d = c % (INT_MAX)

                if d == 0:
                    stack.insert(0,INT_MAX -1)
                else:
                    stack.insert(0,d-1)
            else:
                stack.insert(0,c)
            
        #SUB
        if op == 0x03:
            a = stack.pop()
            b = stack.pop()

            c = b-a

            if c < 0:
                stack.insert(0,c + INT_MAX +1)
            else: stack.insert(0,c)

        #DIV
        if op == 0x04:
            a = stack.pop()
            b = stack.pop()

            if a==0:
                stack.insert(0,0)
            else: 
                c = b/a
                stack.insert(0, int(c))            

        #MOD
        if op == 0x06:
            a = stack.pop()
            b = stack.pop()

            if a==0:
                stack.insert(0,0)
            else:
                c = b%a
                stack.insert(0,c)

        #ADDMOD: a+b mod c stack: [c,b,a]
        if op == 0x08:
            a = stack.pop()
            b = stack.pop()
            c = stack.pop()

            if a == 0:
                stack.insert(0,0)
            else:
                d = (c+b)%a
                stack.insert(0,d)

        #MULMOD: a*b mod c stack: [c,b,a]
        if op == 0x09:
            a = stack.pop()
            b = stack.pop()
            c = stack.pop()

            if a == 0:
                stack.insert(0,0)
            else:
                d = (b*c)%a
                stack.insert(0,d)

        #EXP
        if op == 0x0a:
            a = stack.pop()
            b = stack.pop()

            stack.insert(0,(b**a))

        #SIGNEXTEND
        if op == 0x0b:
            val = stack.pop()
            n = stack.pop()
            
            bit_index = (n * 8) + 7 
            sign_bit = (val >> bit_index) & 1
            
            
            if sign_bit == 0:
                extended = val
            else:
                mask = (1 << (bit_index + 1)) - 1
                extended = val | (INT_MAX & ~mask)  
                
            stack.insert(0, extended)

        if op == 0x05:
            a = stack.pop()
            b = stack.pop()

            if a == 0:
                stack.insert(0,0)
            
            else:
                n = 256
                
                if (a >> n-1) & 1 == 1:
                    a = a - (1 << n)
                if (b >> n-1) & 1 == 1:
                    b = b - (1 << n) 

                result = int(b/a)

                if (result < 0):
                    result = (1 << n) + result
                
                stack.insert(0, result)

        if op == 0x07:
            a = stack.pop()
            b = stack.pop()

            if a == 0:
                stack.insert(0,0)

            else:
                n =256

                if (a >> n-1) & 1 == 1:
                    a = a - (1 << n)
                if (b >> n-1) & 1 == 1:
                    b = b - (1 << n)

                result = int(b%a)

                if a == 0:
                    stack.insert(0,0)

                if result < 0:
                    result += (1 << n)
                
                stack.insert(0, result)

        if op == 0x10:
            a = stack.pop() #10
            b = stack.pop() #9

            if b < a:
                stack.insert(0,1)
            else:
                stack.insert(0,0)
        
        if op == 0x11:
            a = stack.pop() #9
            b = stack.pop() #10

            if b > a:
                stack.insert(0,1)
            else: stack.insert(0,0)
        
        if op == 0x12:
            a = stack.pop() #n
            b = stack.pop() #0

            if (a >> 255) & 1 == 1:
                a = a - (1 << 255)
            if (b >> 255) & 1 == 1:
                b = b - (1 << 255)
            
            if (b > a):
                stack.insert(0,1)
            else: stack.insert(0,0)

        if op == 0x13:
            a = stack.pop() 
            b = stack.pop() 

            if (a >> 255) & 1 == 1:
                a = a - (1 << 255)
            if (b >> 255) & 1 == 1:
                b = b - (1 << 255)
            
            if (b > a):
                stack.insert(0,1)
            else: stack.insert(0,0)

        if op == 0x14:
            a = stack.pop() 
            b = stack.pop()
            
            if (b == a):
                stack.insert(0,1)
            else: stack.insert(0,0)
        
        if op == 0x15:
            a = stack.pop()

            if a==0:
                stack.insert(0,1)
            else: stack.insert(0,0)

        if op == 0x19:
            a = stack.pop()

            result = (1<< 256) - a - 1
            stack.insert(0,result)
            
        if op == 0x16:
            a = stack.pop() #13
            b = stack.pop() #3
            c = 0 
            
            n = 256

            for i in range(n):
                if ((b >> i) & 1) + ((a >> i) & 1) == 2:
                    c = c | (1 << i)
                else: c = c & ~(1 << i)

            stack.insert(0,c)

        if op == 0x17:
            a = stack.pop() 
            b = stack.pop()
            n = 256
            c = 0

            for i in range(n):
                if ((b >> i) & 1) | ((a >> i) & 1):
                    c = c | (1 << i)
                else: c = c & ~(1 << i)
            
            stack.insert(0,c)

        if op == 0x18:
            a = stack.pop()
            b = stack.pop()

            n = 256
            c=0
            for i in range(n):
                if ((a >> i) & 1 == (b >> i)& 1):
                    c = c & ~(1<< i)
                else: c = c | (1<<i)

            stack.insert(0,c)
        
        if op == 0x1b:
            value = stack.pop()
            shift = stack.pop()
            c = 0

            if shift >= 256:
                stack.insert(0, 0)
            else:
                c = (value << shift) & ((1 << 256) -1)
                stack.insert(0,c)

        if op == 0x1c:
            val = stack.pop()
            shift = stack.pop()

            c = 0 
            if shift >=256:
                stack.insert(0,0)
            else:
                c = (val >> shift) & ((1 << 256) - 1)
                stack.insert(0,c)

        if op == 0x1d:
            val = stack.pop()
            shift = stack.pop()

            if (val >> 255) & 1 == 0:
                c = (val >> shift) & ((1 << 256) - 1)
                stack.insert(0,c)
            else:
                neg_val = val - (1 << 256)
                c = neg_val >> shift
                d = c + (1 << 256)
                stack.insert(0,d)

        if op == 0x1a:
            val = stack.pop()
            by = stack.pop()

            if by <= 31:
                c = (val >> (31 - by)*8) & 0b11111111
            else:
                c = 0

            stack.insert(0,c)

        if 0x80 <= op <= 0x8F:
            n = op - 0x80
            stack.insert(0,stack[n])

        if 0x90 <= op <= 0x9F:

            n = op - 0x90 + 1
            a = stack[0]
            b = stack[n]

            stack.remove(a)
            stack.remove(b)

            stack.insert(0,b)
            stack.insert(n,a)


        if 0x60 <= op <= 0x7f:
            byte_number = op - 0x60 + 1
            value = int.from_bytes(code[pc:pc+ byte_number],"big")
            stack.insert(0,value)
            pc += byte_number

        if op == 0xfe:
            success = False

        if op == 0x58:
            stack.insert(0,pc - 1)

        if op == 0x5a:
            a = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
            stack.insert(0,a)          
        
        if op == 0x56:  # JUMP
            dest = stack.pop(0)  # Get jump target
            if dest >= len(code) or code[dest] != 0x5b:
                success = False # Invalid jump target
                break
            
            if code[dest] == 0x5b and 0x60 <= code[dest-1] <= 0x7f:
                success = False
                break

            pc = dest

        if op == 0x57:
            con = stack.pop()
            des = stack.pop()

            if con == 1 and code[des] == 0x5b:
                pc = des
        
        if op == 0x52:
            val = stack.pop()
            offset = stack.pop()

            byt = val.to_bytes(32,'big')

            for i in range(len(byt)):
                memo.append(0)

            for i in range(len(byt)):
                memo[offset+i] = byt[i]

        if op == 0x51:
            offset = stack.pop()

            if offset + 32 > len(memo):
                memo.extend([0] * (offset + 32 - len(memo)))
            
            result = memo[offset:offset+32]
            val = int.from_bytes(result, 'big')
            stack.insert(0,val)

        if op == 0x53:
            offset = stack.pop(0)  
            val = stack.pop(0)

            if offset >= len(memo):
                memo.extend([0] * (offset + 1 - len(memo)))

            memo[offset] = val & 0xff

        if op == 0x59:

            siz = len(memo)
            
            if siz%32 == 0:
                stack.insert(0,siz)
            else:
                n = int(siz/32)
                if siz % 32 < 16:
                    stack.insert(0,n*32)
                if siz % 32 > 16:
                    stack.insert(0,(n+1)*32)

        if op == 0x20:

            length = stack.pop()
            offset = stack.pop()

            val = memo[offset:offset+length]

            result = int.from_bytes(keccak(val))

            stack.insert(0,result)

        if op == 0x30:
            to_addr = int(tx["to"] , 16)
            stack.insert(0, to_addr)

        if op == 0x33:
            from_addr = tx["from"]
            stack.insert(0, int(from_addr,16))

        if op == 0x32:
            addr = tx["origin"]
            stack.insert(0,int(addr,16))

        if op== 0x3a:
            price = tx["gasprice"]
            stack.insert(0,int(price,16))  
        
        if op == 0x48:
            base = tx["basefee"]
            stack.insert(0,int(base, 16))

        if op == 0x41:
            coinbase = tx["coinbase"]
            stack.insert(0,int(coinbase,16))

        if op == 0x42:
            time = tx["timestamp"]
            stack.insert(0,int(time,16))
        
        if op == 0x43:
            number = tx["number"]
            stack.insert(0,int(number, 16))
        
        if op == 0x44:
            difficulty = tx["difficulty"]
            stack.insert(0,int(difficulty, 16))

        if op == 0x45:
            gaslimit = tx["gaslimit"]
            stack.insert(0, int(gaslimit,16))

        if op == 0x46:
            chainid = tx["chainid"]
            stack.insert(0,int(chainid,16))
        
        if op == 0x31:
            addr_raw = stack.pop()
            addr = hex(addr_raw)[2:].rjust(40,"0")
            addr_final = "0x" + addr.lower()

            balance_raw = tx.get(addr_final,{}).get("balance", "0x0")
            balance = int(balance_raw,16)

            stack.insert(0,balance)
        
        if op == 0x34:
            value = tx["value"]
            stack.insert(0, int(value, 16))

        if op == 0x35:
            offset = stack.pop()
            call_raw  = tx["data"]
            call = bytes.fromhex(call_raw)
            result = call[offset:offset+32]
            data_padded = result + b"\x00" * (32 - len(result))
            stack.insert(0,int.from_bytes(data_padded))
        
        if op == 0x36:
            raw = tx.get("data","")
            data = bytes.fromhex(raw)
            length = len(data)
            stack.insert(0,length)

        if op == 0x37:
            size = stack.pop()
            call_offset = stack.pop()
            memo_offset = stack.pop()

            call_raw = tx.get("data","0")
            call_bytes = bytes.fromhex(call_raw)
            call = call_bytes[call_offset:call_offset+size]
            call_final = call + b"\x00" * (32 - len(call))

            if len(memo) < call_offset+32 :
                memo.extend([0]* (call_offset + 32 - len(memo)))
            
            memo[memo_offset:memo_offset+32] = call_final

        if op == 0x38:
            stack.insert(0,pc)

        if op == 0x39:
            size = stack.pop()
            offset = stack.pop()
            memo_offset = stack.pop()

            if len(memo) < memo_offset + size:
                memo.extend([0] * (memo_offset + size - len(memo)))

            copied = code[offset:offset + size]
            copied += b'\x00' * (size - len(copied))

            memo[memo_offset:memo_offset+size] = copied


        if op == 0x3B:  
            addr = stack.pop()
        
            addr_hex = hex(addr)[2:].rjust(40, '0')
            addr_str = "0x" + addr_hex.lower()


            code_hex = tx.get(addr_str, {}).get("code", {}).get("bin", "")

            code_bytes = bytes.fromhex(code_hex)
            stack.insert(0, len(code_bytes))

        if op == 0x3C:
            sz = stack.pop()
            offset = stack.pop()
            dest_offset = stack.pop()
            addr = stack.pop()

            addr_hex = hex(addr)[2:].rjust(40, '0')
            addr_str = "0x" + addr_hex.lower()

            code_hex = tx.get(addr_str, {}).get("code",{}).get("bin","")

            code_bytes = bytes.fromhex(code_hex)

            if dest_offset+sz > len(memo):
                memo.extend([0]* (dest_offset + sz - len(memo)))
            
            memo[dest_offset:dest_offset+sz] = code_bytes

        if op == 0x3f:
            addr = stack.pop()

            addr_hex = hex(addr)[2:].rjust(40, '0')
            addr_str = "0x" + addr_hex.lower()

            code_raw = tx.get(addr_str,{}).get("code",{}).get("bin","")
            
            if code_raw:
                
                code_bty = bytes.fromhex(code_raw)

                code_sha = keccak(code_bty)

                stack.insert(0,int.from_bytes(code_sha))
            else:
                stack.insert(0,0)
        
        if op == 0x47:
            addr = tx.get("to", "")
            add_hex = addr[2:].rjust(40, "0")
            add_str = "0x" + add_hex.lower()

            balance = state.get(add_str, {}).get("balance", "0x0")
            hex_str = balance[2:].strip()
            if len(hex_str) % 2 != 0:
                hex_str = "0" + hex_str

            result = bytes.fromhex(hex_str)
            stack.insert(0, int.from_bytes(result))

        if op == 0x55:
            value = stack.pop()
            slot = stack.pop()

            storage[slot] = value

        if op == 0x54:
            slot = stack.pop()

            stack.insert(0,storage.get(slot, 0))
        
        if 0xA0 <= op <= 0xA4 :
            n = op - 0xA0
            topics = []
            for i in range(n):
                topics.insert(0,hex(stack.pop()))
            
            size = stack.pop()
            offset = stack.pop()

            addr = tx.get("to", "")
            add_hex = addr[2:].rjust(40, "0")
            add_str = "0x" + add_hex.lower()

            data_bytes = memo[offset:offset+size]
            data_int = int.from_bytes(data_bytes)
            data = hex(data_int)[2:]

            logs = {
                "address" : add_str,
                "data" : data,
                "topics": topics
            }
            
            stack.insert(0,logs)

        if op == 0xF3:
            size = stack.pop()
            offset = stack.pop()

            return (True,hex(int.from_bytes(memo[offset:offset+size]))[2:])
        
        if op == 0xFD:
            size = stack.pop()
            offset = stack.pop()

            return (False, hex(int.from_bytes(memo[offset:offset+size]))[2:])


    return (success, stack)


def test():
    script_dirname = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dirname, "..", "evm.json")
    with open(json_file) as f:
        data = json.load(f)
        total = len(data)

        for i, test in enumerate(data):
            # Determine which context to pass based on test index
            if 101 > i > 96 or 111 < i < 116 or 116 < i < 119 or 131 < i < 137:
                tx = test['tx']
                code = bytes.fromhex(test['code']['bin'])
                (success, result) = evm(code, tx, {})
            elif 109 > i > 100:
                tx = test['block']
                code = bytes.fromhex(test['code']['bin'])
                (success, result) = evm(code, tx, {})
            elif i == 110 or 123 < i < 127:
                tx = test['state']
                code = bytes.fromhex(test['code']['bin'])
                (success, result) = evm(code, tx, {})
            elif i == 128:
                sts = test['state']
                tx = test['tx']
                code = bytes.fromhex(test['code']['bin'])
                (success, result) = evm(code, tx, sts)
            else:
                code = bytes.fromhex(test['code']['bin'])
                (success, result) = evm(code, {}, {})

            expect = test.get('expect', {})

            # Handle stack-based tests
            if 'stack' in expect:
                expected = [int(x, 16) for x in expect['stack']]
                result_type = "Stack"
            # Handle logs-based tests
            elif 'logs' in expect:
                expected = expect['logs']
                result_type = "Logs"
            # Handle return-based tests (if any)
            elif 'return' in expect:
                expected = expect['return']
                result_type = "Return"
            else:
                # No specific expectation, just check success
                if success == expect.get('success', True):
                    print(f"✓  Test #{i + 1}/{total} {test['name']}")
                else:
                    print(f"❌ Test #{i + 1}/{total} {test['name']}")
                    print("Success doesn't match")
                    print(" expected:", expect.get('success', True))
                    print("   actual:", success)
                    print(f"Progress: {i}/{len(data)}")
                    break
                continue

            # Compare results
            if result != expected or success != expect['success']:
                print(f"❌ Test #{i + 1}/{total} {test['name']}")
                if result != expected:
                    print(f"{result_type} doesn't match")
                    print(" expected:", expected)
                    print("   actual:", result)
                if success != expect['success']:
                    print("Success doesn't match")
                    print(" expected:", expect['success'])
                    print("   actual:", success)
                print("\nTest code:")
                print(test['code']['asm'])
                print("Hint:", test['hint'])
                print(f"Progress: {i}/{len(data)}")
                break
            else:
                print(f"✓  Test #{i + 1}/{total} {test['name']}")


if __name__ == '__main__':
    test()