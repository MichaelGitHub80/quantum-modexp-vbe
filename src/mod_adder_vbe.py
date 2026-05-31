from qiskit import QuantumRegister, QuantumCircuit
from qiskit.circuit.library import VBERippleCarryAdder

def mod_adder_vbe(n, N_val):

    a = QuantumRegister(n, 'a') 
    b = QuantumRegister(n, 'b')
    c = QuantumRegister(n-1, 'c')
    N = QuantumRegister(n, 'N')
    t = QuantumRegister(1, 't')
    
    qc = QuantumCircuit(a, b, c, N, t)
    
    # consider using kind="half" oder "full", as with kind="fixed" there is no borrower-bit
    adder = VBERippleCarryAdder(n, kind="fixed").to_gate(label="mod ADD")
    sub = adder.inverse()
    
    qc.append(adder, a[:] + b[:] + c[:])

    # swap registers: |a>|N> -> |N>|a>
    for i in range(n):
        qc.swap(a[i], N[i])
        
    # subtract N
    qc.append(sub, a[:] + b[:] + c[:])
    
    # copy subtraction overflow/borrow bit into t
    qc.cx(c[n-2], t[0])
    
    # if a + b <= N -> MSB = 1, add back N
    # if a + b > N -> MSB = 0, keep result, add back 0
    for i in range(n):
        if (N_val >> i) & 1:
            qc.cx(t[0], a[i])
            
    # add back N or 0 depending on state of t
    qc.append(adder, a[:] + b[:] + c[:])
     
    # uncompute
    for i in range(n):
       if (N_val >> i) & 1:
           qc.cx(t[0], a[i])     
     
    # swap registers: |N>|a> -> |a>|N>
    for i in range(n):
        qc.swap(a[i], N[i])
        
    # subtract original a
    qc.append(sub, a[:] + b[:] + c[:])
    
    # uncompute t
    # qc.cx(b[n-1], t[0])
    qc.cx(c[n-2], t[0])
    
    # uncompute subtraction
    qc.append(adder, a[:] + b[:] + c[:])
    
    return qc.to_gate(label=f"mod_adder_vbe_{N_val}")