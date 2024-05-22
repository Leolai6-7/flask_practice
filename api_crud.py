#導入模組
from flask import Flask, request
from flask_restful import Api, Resource

#將app實體化並包入api中
app = Flask(__name__)
api = Api(app)

#創建一個放置使用者資料的list
user_list = []

#創建user的資源
class User(Resource):
    def post(self, username):
        user = {
        'username': username,
        'email': request.get_json().get('email')
               }
        user_list.append(user)
        return user
    def get(self, username):
        for user in user_list:
            if user['username'] == username:
                return user
        return {'username': None}, 404
    def delete(self, username):
        for ind, user in enumerate(user_list):
            if user['username'] == username:
                deleted_user = user_list.pop(ind)
                print(deleted_user)
                return {'note': 'successfully delete'}
            return {'username': None}, 404
    def put(self, username):
        user_find = None
        for user in user_list:
            if user['username'] == username:
                user_find = user
        if user_find:
            user_list.remove(user_find)
            user_find['email'] = request.get_json().get('email')
            user_list.append(user_find)
            return user_find
        return {'username': None}, 404

class UserList(Resource):
    """會員列表 """
    def get(self):
        return {'user_list': user_list}

api.add_resource(User, '/user/<string:username>')
api.add_resource(UserList, '/users')

if __name__ == '__main__':
    app.run()