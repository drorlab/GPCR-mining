import pytest
import os
import importlib
import gpcrmining.gpcrdb as db

receptor='adrb1_human'

def test_stub():
    _ = db.get_residue_info(receptor)
    assert 4 == 4
    pass

