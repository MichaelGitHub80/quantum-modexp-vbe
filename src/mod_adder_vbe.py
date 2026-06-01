from qiskit import QuantumRegister, QuantumCircuit
from qiskit.circuit.library import VBERippleCarryAdder, CDKMRippleCarryAdder

def mod_adder_vbe(m, N_val):

    a = QuantumRegister(m, 'a') 
    b = QuantumRegister(m, 'b')
    c = QuantumRegister(1, 'c')
    N = QuantumRegister(m, 'N')
    t = QuantumRegister(1, 't')
    
    qc = QuantumCircuit(a, b, c, N, t)  
    
    adder = CDKMRippleCarryAdder(m, kind="fixed").to_gate()
    sub = adder.inverse()
    
    # |a>|b>|c>|N>|t> - > |a>|(a+b) mod 2^m>|c>|N>|t>
    qc.append(adder, a[:] + b[:] + c[:])

    # # |a>|b>|c>|N>|t> - > |N>|(a+b) mod 2^m>|c>|a>|t>
    for i in range(m):
        qc.swap(a[i], N[i])
        
    # subtract N
    # # |N>|(a+b) mod 2^m>|c>|a>|t> - > |N>|(a+b-N) mod 2^m>|c>|a>|t>
    # s' = s - N = a + b - N
    qc.append(sub, a[:] + b[:] + c[:])
    
    # determine whether subtraction of N led to an overflow bit in b
    qc.x(b[m-1])
    qc.cx(b[m-1], t[0])
    qc.x(b[m-1])
    
    # if a + b >= N -> MSB of b = 1, subtraction of N was correct, set a register to 0 which currently temporarily holds N
    # if a + b < N -> MSB of b = 0, subtraction of N was incorrect, set a register to N to add back N
    for i in range(m):
        if (N_val >> i) & 1:
            qc.cx(t[0], a[i])
            
    # add back N or 0 depending on state of the borrow bit t
    qc.append(adder, a[:] + b[:] + c[:])
     
    # uncompute
    for i in range(m):
       if (N_val >> i) & 1:
           qc.cx(t[0], a[i]) 
   
     
    # swap registers: |N>|a> -> |a>|N>
    for i in range(m):
        qc.swap(a[i], N[i])
    
    # subtract original a
    qc.append(sub, a[:] + b[:] + c[:])
    
    # uncompute t
    qc.cx(b[m-1], t[0])
    
    # uncompute subtraction
    qc.append(adder, a[:] + b[:] + c[:])
    
    return qc.to_gate(label=f"mod_adder_vbe_{N_val}")