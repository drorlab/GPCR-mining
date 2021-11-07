import pytest
import os
import importlib
import gpcrmining.gpcrdb as db

gpcr_name = 'adrb1_human'
seq_num = [330, 232, 189, 228]
gen_num = ['6.41x41', '5.46x461', '4.56x56', '5.42x43']

def test_get_residue_info():
    res_info = db.get_residue_info(gpcr_name)
    assert len(res_info) == 477
    assert res_info[0] == ['N-term', 1, 'M', '']
    assert res_info[99] == ['TM2', 100, 'L', '2.46x46']
    pass

def test_gpcrdb_to_sequential():
    seq = db.gpcrdb_to_sequential(gpcr_name, gen_num)
    assert seq == seq_num
    pass
    
def test_sequential_to_gpcrdb():
    gen = db.sequential_to_gpcrdb(gpcr_name, seq_num)
    assert gen == gen_num
    pass
    
