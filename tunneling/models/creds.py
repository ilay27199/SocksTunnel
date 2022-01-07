class Creds:
    def __init__(self, cred_type):
        self.cred_type = cred_type

    def to_json(self):
        return {
            'type': 'creds',
            'creds_type': self.cred_type
        }


class UsernamePasswordCreds(Creds):
    TYPE = 'username_password_creds'

    def __init__(self, username, password):
        super().__init__(UsernamePasswordCreds.TYPE)
        self.username = username
        self.password = password

    def to_json(self):
        creds_dict = super().to_json()
        creds_dict['username'] = self.username
        creds_dict['password'] = self.password
        return creds_dict

    @staticmethod
    def from_json(username_password_creds):
        return UsernamePasswordCreds(
            username=username_password_creds['username'],
            password=username_password_creds['password']
        )
