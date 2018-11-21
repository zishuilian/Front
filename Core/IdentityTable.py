from Core.getDatabase import getDatabase

# 用来存储一个用户对应的多个身份证的关系：[用户账号(username)，身份证号(card)] 1:m

class IdentityTable():
    def __init__(self):
        pass

    # 返回一个用户所绑定的所有身份证
    def find(self, username):
        client, cursor = getDatabase('identity_collections')  # or cursor = db.test_collections auto create the collection
        _list = cursor.find({'username': username})
        client.close()
        return _list

    # 为一个用户添加一个身份证
    def insert(self, username, card, name, phone):
        client, cursor = getDatabase('identity_collections')

        if cursor.find_one({'username': username, 'card': card}) == None:
            cursor.insert_one({'username': username, 'card': card, 'name': name, 'phone': phone})
        client.close()

    # 为一个用户删除一个身份证
    def delete(self, username, card):
        client, cursor = getDatabase('identity_collections')
        b = cursor.find_one({'username': username, 'card' : card})

        if b == None:
            client.close()
            return False  # 该用户没绑定该身份证
        else:
            cursor.delete_one(b)
            client.close()
            return True  # 删除成功
