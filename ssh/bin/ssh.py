#!/usr/bin/rnv python3

# formal lib
from argparse import RawTextHelpFormatter
import argparse
import os
# my lib
from help_ssh import AdminSshClient


def fnmstr(path_str):
    if not os.path.exists(path_str):
        mes = "{} is not file.".format(
                                    path_str
                                      )
        raise OSError(mes)
    return path_str


if __name__ == "__main__":
    msg = "this program helps "
    parser = argparse.ArgumentParser(
                            description=msg,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument("host_ip", type=str, nargs="?")
    parser.add_argument("--username", type=str, nargs="?", required=True)
    parser.add_argument("--private_fkey", type=fnmstr, nargs="?",
                        required=True)
    parser.add_argument("--port", type=int, nargs="?", default=22)
    parser.add_argument("--confirm_secture_host", action="store_true",
                        default=False)
    subparsers = parser.add_subparsers(dest="subopt")
    scpput_parser = subparsers.add_parser("scp_put")
    scpget_parser = subparsers.add_parser("scp_get")
    exec_parser = subparsers.add_parser("excec")
    # excec command args
    exec_parser.add_parser("--cmd", type=str, nargs="+", required=True)
    exec_parser.add_parser("--cwd", type=str, nargs="?", default=None)
    # scpput command args
    scpput_parser.add_parser("--local_srcs", type=fnmstr, nargs="+",
                             required=True)
    scpput_parser.add_parser("--remote_dst", type=str, nargs="?",
                             required=True)
    # scpget command args
    scpget_parser.add_parser("--remote_srcs", type=str, nargs="+",
                             required=True)
    scpget_parser.add_parser("--local_dst", type=str, nargs="?",
                             required=True)
    # definitions of arguments.
    args = parser.parse_args()
    HOST_IP = args.host_ip
    USERNAME = args.usernam
    PORT = args.port
    PRIVATE_FKEY = args.private_fkey
    CONFIRM_SECTURE_HOST = args.confirm_secture_host
    SUBOPT = args.subopt
    if SUBOPT == "exec":
        CMD = args.cmd
        CWD = args.cwd
        adminssh_ins = AdminSshClient(HOST_IP, USERNAME, PRIVATE_FKEY,
                                      PORT, CONFIRM_SECTURE_HOST)
        if CWD is not None:
            adminssh_ins.set_current_dir(CWD)
            adminssh_ins.excec_act_cwd(CMD)
        else:
            adminssh_ins.excec(CMD)
    elif SUBOPT == "scpput":
        LOCAL_SRCS = args.local_srcs
        REMOTE_DST = args.remote_dst
        adminssh_ins = AdminSshClient(HOST_IP, USERNAME, PRIVATE_FKEY,
                                      PORT, CONFIRM_SECTURE_HOST)
        adminssh_ins.scp_put(LOCAL_SRCS, REMOTE_DST)
    elif SUBOPT == "scpget":
        REMOTE_SRCS = args.remote_srcs
        LOCAL_DST = args.local_dst
        adminssh_ins = AdminSshClient(HOST_IP, USERNAME, PRIVATE_FKEY,
                                      PORT, CONFIRM_SECTURE_HOST)
        adminssh_ins.scp_get(REMOTE_SRCS, LOCAL_DST)
    else:
        raise AssertionError("")
