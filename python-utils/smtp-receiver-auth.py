# https://pypi.python.org/pypi/secure-smtpd/3.0.0
# virtualenv venv
# TODO Missing dependency six
# https://github.com/bcoe/secure-smtpd/blob/master/setup.py#L19
# venv/bin/pip install six
# venv/bin/pip install secure-smtpd
# venv/bin/python smtp-receiver-auth.py
from secure_smtpd import SMTPServer
from datetime import datetime
import os
import logging
import secure_smtpd

# Update the package
# https://github.com/bcoe/secure-smtpd/issues
# TODO Create a complete Hello World
# + add installation instructions
# https://github.com/bcoe/secure-smtpd/issues/30

# TODO Switch to http://aiosmtpd.readthedocs.io/en/latest/
# Cf https://github.com/aio-libs/aiosmtpd/blob/master/examples/server.py to include user
# https://speakerdeck.com/pycon2017/barry-warsaw-aiosmtpd-a-better-asyncio-based-smtp-server
# See https://stackoverflow.com/questions/1138425/add-smtp-auth-support-to-python-smtpd-library-cant-override-the-method
# and https://stackoverflow.com/questions/44028565/aiosmtpd-python-smtp-server

# Post new code sample (without auth) to
# https://stackoverflow.com/questions/2690965/a-simple-smtp-server

HOST = '0.0.0.0'
# PORT = 25
PORT = 2525

DIRECTORY = 'tmp/'
USERS = {
    'annon: 'coincoin'
}

class SmtpEmlDumperServer(SMTPServer):
    no = 0
    def process_message(self, peer, mailfrom, rcpttos, data):
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)
        print(peer)
        print(mailfrom)
        print(data)
        filename = DIRECTORY + '{}-{}.eml'.format(
            datetime.now().strftime('%Y%m%d%H%M%S'),
            self.no
        )
        f = open(filename, 'w')
        f.write(data)
        f.close
        print('{} saved.'.format(filename))
        self.no += 1

class CredentialValidator:
    def validate(self, username, password):
        logger = logging.getLogger( secure_smtpd.LOG_NAME )
        if username in USERS and USERS[username] == password:
            return True
        return False


def run():
    print('Starting server on {}:{}'.format(HOST, PORT))
    server = SmtpEmlDumperServer(
        (HOST, PORT),
        None,
        require_authentication=True,
        ssl=False,
        credential_validator=CredentialValidator()
    )
    try:
        server.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
	run()
