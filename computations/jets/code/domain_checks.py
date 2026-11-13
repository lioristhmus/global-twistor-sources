"""Container-only structural audit of the universal Gaussian input domain."""
from itertools import combinations_with_replacement,product
import jet_gaussian as j
from report import emit

def audit_jet_domain(order):
    pairs=list(combinations_with_replacement(range(1,4),2))
    first={j.dg(i,k,a) for i,k in pairs for a in range(4)}
    second={j.ddg(i,k,a,b) for i,k in pairs for a,b in combinations_with_replacement(range(4),2)}
    if len(first)!=24 or len(second)!=60 or first&second:
        raise RuntimeError('Metric-jet symbols are not independent')
    if not all(x.is_Symbol for x in first|second):
        raise RuntimeError('Non-symbolic metric derivative')
    if any(j.dg(0,i,a)!=0 for i,a in product(range(4),repeat=2)):
        raise RuntimeError('Gaussian time metric is not constant')
    if any(j.ddg(i,k,a,b)!=j.ddg(k,i,b,a) for i,k,a,b in product(range(1,4),range(1,4),range(4),range(4))):
        raise RuntimeError('Jet symmetry mismatch')
    result={'record':'jet-domain','first':len(first),'second':len(second),'metric_entries':6,'coordinates':4}
    if order==3:
        from third_gaussian import dddg
        third={dddg(i,k,a,b,c) for i,k in pairs for a,b,c in combinations_with_replacement(range(4),3)}
        if len(third)!=120 or (first|second)&third or not all(x.is_Symbol for x in third):
            raise RuntimeError('Third-jet symbols are not independent')
        result['third']=len(third)
    if not all(j.zero(j.ric4(i,k)-j.ric4(k,i)) for i in range(4) for k in range(4)):
        raise ArithmeticError('Ricci symmetry failed')
    result['ricci_symmetry']='PASS'
    emit(result)
