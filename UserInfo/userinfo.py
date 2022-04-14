info_list = {"user_name": "", "user_password": "", "session": 0}


def showinfo():
    return info_list


def write_user_name(info):
    info_list.update({"user_name": info})


def write_user_password(info):
    info_list.update({"user_password": info})


def write_session(info):
    info_list.update({"session": info})
