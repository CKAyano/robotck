from typing import List, Union
import sympy as sp
from .homomatrix import HomoMatrix, _round_homoMatirx, _convert_homomatrix_float_to_pi


class Links(list):
    def append(self, __object: HomoMatrix) -> None:
        if not isinstance(__object, HomoMatrix):
            raise TypeError("wrong type")
        return super().append(__object)

    def round(self, n: int):
        _round_links(self, n)

    def float_to_pi(self) -> None:
        _convert_links_float_to_pi(self)


def _round_links(links: Links, n: int):
    for m in links:
        _round_homoMatirx(m, n)


def _convert_links_float_to_pi(links: Links):
    for m in links:
        _convert_homomatrix_float_to_pi(m)
