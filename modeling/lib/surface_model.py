#!/usr/bin/env python3


# formal lib
from ase.build import fcc100, fcc110, fcc111
from ase.build import bcc100, bcc110, bcc111
from ase.build import add_adsorbate
from ase.io import write as ase_write
from ase.visualize import view as ase_view
from copy import deepcopy
# my lib
BCC_AD_DICT = {}
BCC_100_ADSORPTION_TYPES = ["ontop", "hollow", "bridge"]
BCC_110_ADSORPTION_TYPES = ["ontop", "hollow", "shortbridge",
                            "longbridge"]
BCC_111_ADSORPTION_TYPES = ["ontop", "hollow"]
BCC_AD_DICT["100"] = BCC_100_ADSORPTION_TYPES
BCC_AD_DICT["110"] = BCC_110_ADSORPTION_TYPES
BCC_AD_DICT["111"] = BCC_111_ADSORPTION_TYPES
BCC_FACE_MAKER_DICT = {}
BCC_FACE_MAKER_DICT["100"] = bcc100
BCC_FACE_MAKER_DICT["110"] = bcc110
BCC_FACE_MAKER_DICT["111"] = bcc111
# BCC bridge?
FCC_AD_DICT = {}
FCC_100_ADSORPTION_TYPES = ["ontop", "hollow", "bridge"]
FCC_110_ADSORPTION_TYPES = ["ontop", "hollow", "shortbridge",
                            "longbridge"]
FCC_111_ADSORPTION_TYPES = ["ontop", "bridge", "fcc", "hcp"]
FCC_AD_DICT["100"] = FCC_100_ADSORPTION_TYPES
FCC_AD_DICT["110"] = FCC_110_ADSORPTION_TYPES
FCC_AD_DICT["111"] = FCC_111_ADSORPTION_TYPES
FCC_FACE_MAKER_DICT = {}
FCC_FACE_MAKER_DICT["100"] = fcc100
FCC_FACE_MAKER_DICT["110"] = fcc110
FCC_FACE_MAKER_DICT["111"] = fcc111
# Global Variables
SLAB_TYPES = ["fcc", "bcc"]


def confirm_type_list(target_li, type_ob=str):
    for ob in target_li:
        if type(ob) != type_ob:
            emes_base = "ob must be invalid type:{}"
            emes = emes_base.format(type_ob)
            raise TypeError(emes)


def confirm_attributions(tg_ins, attrs):
    emes_base = "{} doesn's have {} as a attribute."
    for atr in attrs:
        if not hasattr(tg_ins, atr):
            emes = emes_base.format(tg_ins, atr)
            raise AttributeError(emes)


class SimpleSlabMaker(object):
    def __init__(self, symbol, millar_indices, size=(1, 1, 1),
                 a_axis=None, crystal_type="fcc", vacuum=10.0,
                 orthogonal=False):
        self._set_symbol(symbol)
        self._set_millar_indices(millar_indices)
        self._set_crystal_type(crystal_type)
        self._set_size(size)
        self._set_adsorption_types()
        self.a_axis = a_axis
        self.orthogonal = orthogonal
        self.internal_geometry = None
        self._set_slab_maker()
        self._set_vacuum(vacuum)
        self._set_internal_geometry()

    def _set_symbol(self, symbol):
        if type(symbol) != str:
            raise TypeError(
                    "invalid symbol is entered")
        self.symbol = symbol

    def _set_millar_indices(self, millar_indices):
        all_indices = ["100", "110", "111"]
        cond1 = type(millar_indices) != str
        cond2 = millar_indices not in all_indices
        if cond1 and cond2:
            raise TypeError(
                   "millar_indices must be 100, 110, or 111")
        self.millar_indices = millar_indices

    def _set_crystal_type(self, crystal_type):
        target_crystal_types = ["fcc", "bcc"]
        if crystal_type not in target_crystal_types:
            raise TypeError(
                    "crystal type must be fcc or bcc, "
                    "but:{}".format(crystal_type))
        self.crystal_type = crystal_type

    def _set_size(self, size):
        confirm_type_list(size, int)
        self.size = size

    def _set_adsorption_types(self):
        if self.crystal_type == "fcc":
            self.adsoption_types = FCC_AD_DICT[
                                    self.millar_indices]
        elif self.crystal_type == "bcc":
            self.adsoption_types = BCC_AD_DICT[
                                    self.millar_indices]
        else:
            raise AssertionError("")

    def _set_slab_maker(self):
        if self.crystal_type == "fcc":
            slab_maker = FCC_FACE_MAKER_DICT[self.millar_indices]
        elif self.crystal_type == "bcc":
            slab_maker = BCC_FACE_MAKER_DICT[self.millar_indices]
        else:
            raise AssertionError("")
        self.slab_marker = slab_maker

    def _set_vacuum(self, vacuum=10):
        self.vacuum = vacuum

    def _set_internal_geometry(self):
        self.internal_geometry = self.slab_marker(
                                            self.symbol,
                                            size=self.size,
                                            vacuum=self.vacuum,
                                            a=self.a_axis,
                                            orthogonal=self.orthogonal)

    def set_adsorbent_and_height(self, adsorbent, height):
        self.adsorbent = adsorbent
        self.height = height

    def add_adsorbent(self, adsorbent, height, ad_type):
        self.set_adsorbent_and_height(adsorbent, height)
        add_adsorbate(self.internal_geometry, self.add_adsorbent,
                      self.height, position=ad_type)
        self.ad_type = ad_type

    def reset_geometry(self):
        self.internal_geometry = self.base_geometry

    def coroutine_adsorbed_geometry(self, re_addvacuum=True):
        confirm_attributions(self, ["adsorbent",
                                    "vacuum", "height"])
        for ad_type in self.adsoption_types:
            add_adsorbate(self.internal_geometry, self.adsorbent,
                          self.height,
                          position=ad_type)
            self.ad_type = ad_type
            if re_addvacuum:
                self.internal_geometry.center(
                                            vacuum=self.vacuum,
                                            axis=2)
            yield ad_type
            self._set_internal_geometry()

    def coroutine_write_poscar(self, base_ofnm,
                               re_addvacuum=True):
        for ad_type in self.coroutine_adsorbed_geometry(
                                                re_addvacuum):
            ofnm = base_ofnm + "_" + ad_type
            self.write_poscar(ofnm)
            yield

    @property
    def surface_stat(self):
        if self.ad_type is None:
            ad_type = ""
        stat = "{},{},{}".format(self.crystal_type,
                                 self.millar_indices,
                                 ad_type)
        return stat

    def __next__(self):
        if not hasattr(self, "internal_coroutine"):
            self.internal_coroutine = self.coroutine_adsorbed_geometry()
        next(self.internal_coroutine)

    def __iter__(self):
        return self.coroutine_adsorbed_geometry()

    def write_poscar(self, oposcar, oformat="vasp"):
        ase_write(oposcar, self.internal_geometry,
                  format=oformat)

    def view_geo(self):
        ase_view(self.internal_geometry,
                 viewer="VMD")
