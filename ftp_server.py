from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

ftp_directory = os.path.join(os.getcwd(), "ftp_files")
if not os.path.exists(ftp_directory):
    os.makedirs(ftp_directory)

authorizer = DummyAuthorizer()
authorizer.add_user("user", "password", ftp_directory, perm="elradfmw")
handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("127.0.0.1", 2121), handler)
print("FTP Server is running on 127.0.0.1:21")
server.serve_forever()