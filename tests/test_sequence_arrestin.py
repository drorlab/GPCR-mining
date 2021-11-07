import pytest
import os
import importlib
import gpcrmining.gpcrdb as db

arr_name = 'arrs_human'
seq_num = [15, 23, 166, 234]
gen_num = ['N.ns1.15', 'N.s1s2.03', 'N.s9s10.08', 'C.s14s15.02']

def test_get_residue_info():
    res_info = db.get_residue_info(arr_name)
    assert len(res_info) == 405
    assert res_info[0] == ['ns1', 1, 'M', 'N.ns1.01']
    assert res_info[99] == ['s6h1', 100, 'A', 'N.s6h1.07']
    pass

def test_gpcrdb_to_sequential():
    seq = db.gpcrdb_to_sequential(arr_name, gen_num)
    assert seq == seq_num
    pass
    
def test_sequential_to_gpcrdb():
    gen = db.sequential_to_gpcrdb(arr_name, seq_num)
    assert gen == gen_num
    pass
    
