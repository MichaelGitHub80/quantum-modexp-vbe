from fractions import Fraction
from math import gcd

def reduce_to_minimal_period(a: int, N: int, r: int):
    if r is None:
        return None
        
    for d in range(1, r+1):
        if r % d == 0:
            if pow(a, d, N) == 1:
                return d
             
    return r
    
def estimate_r_from_bitstring(bitstr: str, m: int, a: int, N: int, max_den=None):
    if max_den is None:
        max_den = N
        
    y = int(bitstr, 2)
    theta = y / (2**m)
    
    frac = Fraction(theta).limit_denominator(max_den)   
    s, r0 = frac.numerator, frac.denominator
    
    r = None
    for k in range(1, m*N):
        cand = r0 * k
        if pow(a, cand, N) == 1:
            r = cand
            break
            
    return {
        "bitstr": bitstr,
        "y": y,
        "theta": theta,
        "frac": frac, # s/r0
        "r0": r0,
        "r": r}
        
def factors_from_r(a: int, N: int, r: int):
    if r is None or r % 2 == 1:
        return None, None
    x = pow(a, r // 2, N)
    if x == N-1:
        return None, None
    p = gcd(x - 1, N)
    q = gcd(x + 1, N)
    if p in (1, N) or q in (1, N):
        return None, None
        
    return p, q