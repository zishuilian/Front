from Core.getDatabase import getDatabase

# 存储用户个人信息表，包括username和password

class AccountTable():
    def __init__(self):
        pass

    def exist(self, username):
        client, cursor = getDatabase('account_collections')
        if cursor.find_one({'username': username}) == None:
            client.close()
            return False
        else:
            client.close()
            return True


    def insert_account(self, username, password, level):
        client, cursor = getDatabase('account_collections')
        cursor.insert_one({'username': username, 'password': password, 'level': level})
        client.close()

    def getLevel(self, username):
        assert username is not None
        client, cursor = getDatabase('account_collections')
        a = cursor.find_one({'username': username})
        client.close()
        return a['level']

    def login(self, username, password):
        client, cursor = getDatabase('account_collections')
        if cursor.find_one({'username': username}) == None:
            return 0    #不存在账号
        else:
            if cursor.find_one({'username': username, 'password': password}) == None:
                client.close()
                return 1    #密码错误
            else:
                client.close()
                return 2    #登陆成功

