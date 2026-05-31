from qiskit import QuantumRegister, QuantumCircuit  

def mod_mult_vbe(n, k, N_val, mod_add):

    ctrl = QuantumRegister(1, 'ctrl')
    a = QuantumRegister(n, 'a') 
    b = QuantumRegister(n, 'b')
    c = QuantumRegister(n-1, 'c')
    N = QuantumRegister(n, 'N')
    t = QuantumRegister(1, 't')
    y = QuantumRegister(n, 'y')
    
    qc = QuantumCircuit(ctrl, a, b, c, N, t, y, name=f"CMUL_{k}_MOD_{N_val}")
    
    mod_sub = mod_add.inverse()
    
    # k_inv = pow(k, -1, N_val) does not work for all k
    
    # set constant, where (1 << i) = 2**i
    for i in range(n):
        const = (k * (1 << i)) % N_val
        
        # load constant
        for j in range(n):
            if (const >> j) & 1:
                qc.ccx(ctrl[0], y[i], a[j])
                
        qc.append(mod_add, a[:] + b[:] + c[:] + N[:] + [t[0]])
        
        #uncompute constant
        for j in range(n):
            if (const >> j) & 1:
                qc.ccx(ctrl[0], y[i], a[j])
                
    # swap y and work register
    for i in range(n):
        qc.cswap(ctrl[0], y[i], b[i])
        
    # uncompute work register via inverse modular adder
    """ for i in range(n):
        const = (k_inv * (1 << i)) % N_val
        
        #load  constant
        for j in range(n):
            if (const >> j) & 1:
                qc.ccx(ctrl[0], y[i], a[j])
                
        # accumulate subtraction into work register
        qc.append(mod_sub, a[:] + b[:] + c[:] + N[:] + [t[0]])
        
        # uncompute  constant
        for j in range(n):
            if (const >> j) & 1:
                qc.ccx(ctrl[0], y[i], a[j]) """
                
    for i in reversed(range(n)):
        const = (k * (1 << i)) % N_val

        # load constant
        for j in range(n):
            if (const >> j) & 1:
                qc.ccx(ctrl[0], y[i], a[j])

        # inverse of mod_add
        qc.append(mod_sub, a[:] + b[:] + c[:] + N[:] + [t[0]])

        # unload constant
        for j in range(n):
            if (const >> j) & 1:
                qc.ccx(ctrl[0], y[i], a[j])


    return qc.to_gate()
  