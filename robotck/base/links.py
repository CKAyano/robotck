from .dh_types import DHType
from .homomatrix import HomoMatrix, _convert_homomatrix_float_to_pi, _round_homoMatrix


class Links(list):
    def __init__(self, DH_Type: DHType) -> None:
        super().__init__()
        self.dh_type = DHType
        self.is_std: bool = True
        if self.dh_type == DH_Type.MODIFIED:
            self.is_std = False

    def __str__(self) -> str:
        return f"{self[-1]}"

    def __repr__(self) -> str:
        return f"{self[-1]}"

    def __getitem__(self, index) -> HomoMatrix:
        item = super().__getitem__(index)
        if not isinstance(item, HomoMatrix):
            raise TypeError(f"Item {item} is not of type HomoMatrix")
        return item

    @property
    def end_effector(self):
        return self[-1]

    def get_joint(self, num_joint: int) -> HomoMatrix:
        return self[num_joint - 1]

    def append(self, __object: HomoMatrix) -> None:
        if not isinstance(__object, HomoMatrix):
            raise TypeError(f"Item {__object} is not of type HomoMatrix")
        return super().append(__object)

    def round(self, n: int):
        _round_links(self, n)

    def float_to_pi(self) -> None:
        _convert_links_float_to_pi(self)


def _round_links(links: Links, n: int):
    for m in links:
        _round_homoMatrix(m, n)


def _convert_links_float_to_pi(links: Links):
    for m in links:
        _convert_homomatrix_float_to_pi(m)
