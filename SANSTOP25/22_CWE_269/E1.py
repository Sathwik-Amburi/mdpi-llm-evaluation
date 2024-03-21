def makeNewUserDir(username):
    if invalidUsername(username):
        print('Usernames cannot contain invalid characters')
        return False
    try:
        raisePrivileges()
    os.mkdir('/home/' + username)
    lowerPrivileges()
    
    except OSError:
    print('Unable to create new user directory for user:' + username)
    return False

return True