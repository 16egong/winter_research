class User:
    def __init__(self, real_name='', username='', uid=0):
        self.real_name = real_name
        self.username = username
        self.uid = uid
        
    def get_real_name(self):
        return self.real_name
    
    def get_username(self):
        return self.username
    
    def get_uid(self):
        return self.uid
    
#     def post(message):
#         row = {'username': self.username, 'real_name': self.real_name, 'uid': self.uid, 'message': message}
#         df = df.append(row, ignore_index=True)
#         return df
    