#
    anonymous = False
    if user is None and password is None:
        anonymous = True
                        if anonymous:
                        else:
                            if payload == user:
                                cl.sendall("331 User name okay, need password.\r\n")
                            else:
                                cl.sendall("430 Invalid username or password.\r\n")
                    elif command == "PASS":
                        if payload == password:
                            cl.sendall("230 Logged in.\r\n")
                        else:
                            cl.sendall("430 Invalid username or password.\r\n")                      
                        cl.sendall('257 "{}"\r\n'.format(cwd))
# ftpserver('root', '12345')