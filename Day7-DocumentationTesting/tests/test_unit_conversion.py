"""
Test astropy unit conversion
"""
import astropy.units as u

def test_km_to_m():
    km_in_m = u.km.to(u.m)

    assert(km_in_m == 1000)


def test_nm_to_m():
    nm_in_m = u.nm.to(u.m)

    assert(nm_in_m == 1e-9)