#!/usr/bin/env python3

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
                            formatter_class=RawTextHelpFormatter,
                            fromfile_prefix_chars="@")
    parser.add_argument("--host_ip", type=str, nargs="?", required=True)
    parser.add_argument("--username", type=str, nargs="?", required=True)
    parser.add_argument("--password", type=str, nargs="?", default=None)
    parser.add_argument("--private_fkey", type=fnmstr, nargs="?",
                        default=None)
    parser.add_argument("--port", type=int, nargs="?", default=22)
    parser.add_argument("--confirm_secture_host", action="store_true",
                        default=False)
    subparsers = parser.add_subparsers(dest="subopt")
    scpput_parser = subparsers.add_parser("scpput")
    scpget_parser = subparsers.add_parser("scpget")
    exec_parser = subparsers.add_parser("excec")
    # excec command args
    exec_parser.add_argument("--cmd", type=str, nargs="+", required=True)
    exec_parser.add_argument("--cwd", type=str, nargs="?", default=None)
    # scpput command args
    scpput_parser.add_argument("--local_srcs", type=fnmstr, nargs="+",
                               required=True)
    scpput_parser.add_argument("--remote_dst", type=str, nargs="?",
                               required=True)
    # scpget command args
    scpget_parser.add_argument("--remote_srcs", type=str, nargs="+",
                               required=True)
    scpget_parser.add_argument("--local_dst", type=str, nargs="?",
                               required=True)
    # definitions of arguments.
    args = parser.parse_args()
    HOST_IP = args.host_ip
    USERNAME = args.username
    PORT = args.port
    PRIVATE_FKEY = args.private_fkey
    CONFIRM_SECTURE_HOST = args.confirm_secture_host
    PASSWORD = args.password
    SUBOPT = args.subopt
    if SUBOPT == "excec":
        CMD = args.cmd
        CWD = args.cwd
        adminssh_ins = AdminSshClient(
                                HOST_IP, USERNAME, PRIVATE_FKEY,
                                PORT, PASSWORD, CONFIRM_SECTURE_HOST)
        if CWD is not None:
            adminssh_ins.set_current_dir(CWD)
            adminssh_ins.excec_act_cwd(CMD)
        else:
            adminssh_ins.excec(CMD)
    elif SUBOPT == "scpput":
        LOCAL_SRCS = args.local_srcs
        REMOTE_DST = args.remote_dst
        adminssh_ins = AdminSshClient(HOST_IP, USERNAME, PRIVATE_FKEY,
                                      PORT, PASSWORD,
                                      CONFIRM_SECTURE_HOST)
        adminssh_ins.scp_put(LOCAL_SRCS, REMOTE_DST)
    elif SUBOPT == "scpget":
        REMOTE_SRCS = args.remote_srcs
        LOCAL_DST = args.local_dst
        adminssh_ins = AdminSshClient(HOST_IP, USERNAME,
                                      PRIVATE_FKEY, PORT,
                                      PASSWORD, CONFIRM_SECTURE_HOST)
        adminssh_ins.scp_get(REMOTE_SRCS, LOCAL_DST)
    else:
        raise AssertionError("")
