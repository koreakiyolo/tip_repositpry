#!/usr/bin/env python3

# formal lib
import argparse
from argparse import RawTextHelpFormatter
from more_itertools import consume
# my lib
from surface_model import SimpleSlabMaker


if __name__ == "__main__":
    msg = "this program make simple suraface model and "\
          "surface with adsorbates."
    parser = argparse.ArgumentParser(
                                description=msg,
                                fromfile_prefix_chars="@",
                                formatter_class=RawTextHelpFormatter)
    req_args_grp = parser.add_argument_group("required arguments group")
    opt_args_grp = parser.add_argument_group("optional arguments group")
    req_args_grp.add_argument("--symbol", type=str, nargs="?",
                              required=True)
    req_args_grp.add_argument("--crystal_type", type=str, nargs="?",
                              choices=["bcc", "fcc"], required=True)
    req_args_grp.add_argument("--millar_indices", type=str, nargs="?",
                              default="111")
    opt_args_grp.add_argument("--size", type=int, nargs=3,
                              default=[1, 1, 1])
    opt_args_grp.add_argument("--a_axis", type=float, nargs="?",
                              default=None)
    opt_args_grp.add_argument("--vacuum", type=float, nargs="?",
                              default=8.0)
    opt_args_grp.add_argument("--orthogonal", action="store_true",
                              default=False)
    subparsers = parser.add_subparsers(dest="subopt")
    ssurface_parser = subparsers.add_parser("simple_surface")
    adsorp_parser = subparsers.add_parser("adsorption")
    all_ad_parser = subparsers.add_parser("all_adsorption")
    # make the especial surface model
    ssurface_parser.add_argument("--oposcar", type=str, nargs="?",
                                 required=True)
    # make the especial surface model with adsobates.
    adsorp_parser.add_argument("--oposcar", type=str, nargs="?",
                               required=True)
    adsorp_parser.add_argument("--adsorbates", type=str, nargs="?",
                               default="H")
    adsorp_parser.add_argument("--adtype", type=str, nargs="?",
                               default="top",
                               choices=["ontop", "hollow",
                                        "fcc", "hcp", "bridge",
                                        "shortbridge", "longbridge"])
    adsorp_parser.add_argument("--height", type=float, nargs="?",
                               default=1.5)
    # make the especial surface models with eacch adsobate types.
    all_ad_parser.add_argument("--adsorbates", type=str, nargs="?",
                               required=True)
    all_ad_parser.add_argument("--multi_obase", type=str, nargs="?",
                               required=True)
    all_ad_parser.add_argument("--height", type=float, nargs="?",
                               default=1.5)
    args = parser.parse_args()
    SYMBOL = args.symbol
    CRYSTAL_TYPE = args.crystal_type
    MILLAR_INDICES = args.millar_indices
    A_AXIS = args.a_axis
    SIZE = args.size
    VACUUM = args.vacuum
    SUBOPT = args.subopt
    ORTHOGONAL = args.orthogonal
    # make the simple surface model.
    if SUBOPT == "simple_surface":
        OPOSCAR = args.oposcar
        sslab_maker = SimpleSlabMaker(
                                SYMBOL, MILLAR_INDICES,
                                SIZE, A_AXIS, CRYSTAL_TYPE,
                                VACUUM, orthogonal=ORTHOGONAL)
        sslab_maker.write_poscar(OPOSCAR)
    # make the surface model with adsorbates.
    elif SUBOPT == "adsorption":
        OPOSCAR = args.oposcar
        ADSORBATES = args.adsorbates
        ADTYPE = args.adtype
        HEIGHT = args.height
        sslab_maker = SimpleSlabMaker(
                            SYMBOL, MILLAR_INDICES,
                            SIZE, A_AXIS, CRYSTAL_TYPE,
                            VACUUM, orthogonal=ORTHOGONAL)
        sslab_maker.set_adsorbent_and_height(
                                    ADSORBATES, HEIGHT)
        sslab_maker.write_poscar(OPOSCAR)
    # make the surface models with muliple type adsortion positions.
    elif SUBOPT == "all_adsorption":
        MULTI_OBASE = args.multi_obase
        ADSORBATES = args.adsorbates
        HEIGHT = args.height
        sslab_maker = SimpleSlabMaker(
                                SYMBOL, MILLAR_INDICES,
                                SIZE, A_AXIS, CRYSTAL_TYPE,
                                VACUUM, orthogonal=ORTHOGONAL)
        sslab_maker.set_adsorbent_and_height(
                                    ADSORBATES, HEIGHT)
        write_iter = sslab_maker.coroutine_write_poscar(MULTI_OBASE)
        consume(write_iter)
    else:
        raise AssertionError("")
