"""Verified TV inpainting by preconditioned Douglas-Rachford splitting.

    from tvinpaint import pdr_inpaint
    result = pdr_inpaint(f, known)      # result.u satisfies u == f on the known pixels exactly

`pdr_inpaint(..., legacy=True).u_dr` reproduces the historical notebooks bit for bit.
"""
from .solver import PDRResult, pdr_inpaint

__all__ = ["pdr_inpaint", "PDRResult"]
