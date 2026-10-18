import struct, sys
data = open(sys.argv[1], 'rb').read()
# hunk exe: code hunk starts at 0x24; header block at code+0x134, packed stream at code+0x140
code = 0x24
hdr = code + 0x134
unk, dest, plen = struct.unpack('>III', data[hdr:hdr+12])
src = hdr + 12
a0 = src + plen
def rd():
    global a0
    a0 -= 4
    return struct.unpack('>I', data[a0:a0+4])[0]
outlen = rd()
d0 = rd()
out = bytearray(outlen)
a2 = outlen
def bit():
    global d0
    c = d0 & 1
    d0 >>= 1
    if d0 == 0:  # refill: X=1 marker shifted in at top
        d0 = rd()
        c = d0 & 1
        d0 = (d0 >> 1) | 0x80000000
    return c
def bits(n):
    v = 0
    for _ in range(n):
        v = (v << 1) | bit()
    return v
while True:
    n = bits(3)
    if n:
        if n == 7:
            if bit():
                n = bits(10)
                if n == 0:
                    n = bits(18)
            else:
                n = bits(4) + 7
        for _ in range(n):
            a2 -= 1
            out[a2] = bits(8)
    if a2 <= 0:
        break
    t = bits(2)
    if t == 0:
        ln, ob = 2, 8
    else:
        if t == 1:
            ln = 3
            ob = 8 if bit() else 14
        else:
            if t == 2:
                ln = 4
            else:
                u = bits(2)
                ln = bits(8) if u == 3 else (bits(2) + 7 if u == 2 else u + 5)
            ob = 16 if not bit() else (8 if bit() else 12)
    off = bits(ob)
    for _ in range(ln):
        a2 -= 1
        out[a2] = out[a2 + off]
print(f'unk=${unk:x} dest=${dest:x} packed=${plen:x} unpacked=${outlen:x} end_a2={a2}', file=sys.stderr)
open(sys.argv[2], 'wb').write(out)
