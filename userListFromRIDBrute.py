from cme.module import Module
from cme.helpers.logger import highlight
import re

class CMEModule(Module):
    name = 'extract_usernames'
    description = "Extract usernames from the --rid-brute output"
    supported_protocols = ['smb']
    opsec_safe = True  # This module does not make any changes to the target
    multiple_hosts = True  # This module can be run on multiple hosts

    def options(self, context, module_options):
        """
        FILE    Rid brute output file to parse
        """
        if 'FILE' not in module_options:
            context.log.error('FILE option is required!')
            context.log.error('Usage: cme smb <target> -u <username> -p <password> -M extract_usernames -o FILE=<rid_brute_output_file>')
            return

        self.file = module_options['FILE']

    def on_admin_login(self, context, smb_connection):
        """
        This method is called on an authenticated administrative session
        """
        try:
            with open(self.file, 'r') as file:
                rid_output = file.read()
                usernames = self.extract_usernames(rid_output)
                context.log.info(f"Extracted {len(usernames)} usernames:")
                for username in usernames:
                    highlight(username)
                    # Here you can add the username to the database or perform other actions
        except Exception as e:
            context.log.error(f'An error occurred: {e}')

    def extract_usernames(self, rid_output):
        """
        Extracts the usernames from the rid brute output
        """
        usernames = re.findall(r"\'username\': \'(.*?)\', \'sidtype\': \'SidTypeUser\'", rid_output)
        return usernames
    
#