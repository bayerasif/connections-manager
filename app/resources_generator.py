import random
import string


class ResourcesGenerator:
    def __init__(self, max_amount):
        self.count = 0
        self.max_amount = max_amount
        self.pool = set()

    def create_resource(self):
        resource = {
            'ip': '127.0.5.{}'.format(self.count),
            'username': 'user{}'.format(self.count),
            'password': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        }
        return resource

    def get_resource(self):
        if self.count == self.max_amount:
            return None
        self.count += 1
        if not self.pool:
            resource = self.create_resource()
        else:
            ip, username, password = self.pool.pop()
            resource = {'ip': ip, 'username': username, 'password': password}
        return resource

    def release_resource(self, resource):
        data = (resource['ip'],  resource['username'], resource['password'])
        self.pool.add(data)

