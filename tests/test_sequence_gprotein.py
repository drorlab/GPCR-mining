import pytest
import os
import importlib
import gpcrmining.gpcrdb as db

gp_name = 'gnal_human'
seq_num = [15, 23, 166, 234]
gen_num = ['G.HN.30', 'G.HN.38', 'H.HE.06', 'G.S4.05']

def test_get_residue_info():
    res_info = db.get_residue_info(gp_name)
    assert len(res_info) == 381
    assert res_info[0] == ['HN', 1, 'M', 'G.HN.01'] 
    assert res_info[99] == ['HA', 100, 'I', 'H.HA.29']
    pass

def test_gpcrdb_to_sequential():
    seq = db.gpcrdb_to_sequential(gp_name, gen_num)
    assert seq == seq_num
    pass
    
def test_sequential_to_gpcrdb():
    gen = db.sequential_to_gpcrdb(gp_name, seq_num)
    assert gen == gen_num
    pass
    
