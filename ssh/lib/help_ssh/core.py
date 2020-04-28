#!/usr/bin/env python3


import paramiko
from paramiko import SSHClient
from scp import SCPClient
import sys
import os


class AdminSshClient(object):
    def __init__(self, hostip, username,
                 pkey_fpath=None, access_port=22,
                 password=None,
                 confirm_secure_host=False):
        self.hostip = hostip
        self.access_port = access_port
        self.username = username
        self.pkey_fpath = pkey_fpath
        self.password = password
        self.confirm_secure_host = confirm_secure_host
        self._start_client()

    def _start_client(self):
        self._set_internal_sshclient()
        self._access_through_ssh()

    def _set_internal_sshclient(self):
        self.internal_sshclient = SSHClient()
        if self.confirm_secure_host:
            self.internal_sshclient.set_missing_host_key_policy(
                                                paramiko.WarningPolicy())
        else:
            self.internal_sshclient.load_system_host_keys()

    def _access_through_ssh(self):
        self.internal_sshclient.connect(
                                    self.hostip,
                                    port=self.access_port,
                                    username=self.username,
                                    password=self.password,
                                    key_filename=self.pkey_fpath)

    @property
    def transport(self):
        if not hasattr(self, "_transport"):
            self._transport = self.internal_sshclient.get_transport()
        return self._transport

    def scp_put(self, put_flist, remotepath):
        put_flist = [os.path.normpath(fpath)
                     for fpath in put_flist]
        with SCPClient(self.transport) as scpc:
            scpc.put(put_flist, remotepath,
                     recursive=True)

    def scp_get(self, remote_flist, local_fpath):
        remote_flist = [os.path.normpath(fpath)
                        for fpath in remote_flist]
        with SCPClient(self.transport) as scpc:
            scpc.get(
                  remote_flist, local_fpath,
                  recursive=True)

    def excec(self, args_li, silent=False):
        if type(args_li) == list:
            cmd = " ".join(args_li)
        elif type(args_li) == str:
            cmd = args_li
        else:
            raise AssertionError("command is invalid type.")
        stdin, stdout, stderr = self.internal_sshclient.exec_command(
                                                                    cmd)
        if silent:
            pass
        else:
            sys.stdout.writelines(stdout)
            sys.stdout.flush()
            sys.stderr.writelines(stderr)
            sys.stderr.flush()

    def excec_from_file(self, cmd_file):
        with open(cmd_file, "r") as read:
            for cmd in read:
                cmd = cmd.strip()
                self.excec(cmd)

    def set_current_dir(self, cwd):
        self.current_dir = cwd
        cmd = "cd {}".format(cwd)
        sin, sout, serr = self.internal_sshclient.exec_command(cmd)
        err_li = serr.readlines()
        if len(err_li) != 0:
            emes = "unknown host path: {}".format(cwd)
            raise AssertionError(emes)

    def excec_act_cwd(self, args_li, silent=False):
        if not hasattr(self, "current_dir"):
            emes = "in advance, you must set current_dir."
            raise AttributeError(emes)
        cd_cmd = "cd {};".format(self.current_dir)
        if type(args_li) == list:
            cmd = " ".join(args_li)
        elif type(args_li) == str:
            cmd = args_li
        else:
            raise AssertionError("command is invalid type.")
        tot_cmd = cd_cmd + cmd
        stdin, stdout, stderr = self.internal_sshclient.exec_command(
                                                               tot_cmd)
        if silent:
            pass
        else:
            sys.stdout.writelines(stdout)
            sys.stdout.flush()
            sys.stderr.writelines(stderr)
            sys.stderr.flush()

    def excec_from_file_act_cwd(self, cmd_file):
        with open(cmd_file, "r") as read:
            for cmd in read:
                cmd = cmd.strip()
                self.excec_act_cwd(cmd)
