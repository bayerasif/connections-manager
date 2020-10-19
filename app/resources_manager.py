import random
import string
from collections import namedtuple

Resource = namedtuple("Resource", ["ip", "username", "password"])
JSON_FIELDS = {'IP': 'ip', 'USERNAME': 'username', 'PASSWORD': 'password'}


class ResourcesManager:
    def __init__(self, max_amount):
        self.count = 0
        self.max_amount = max_amount
        self.pool = set()
        self.busy = {}

    def get_resource(self):
        if self.pool:
            raw_resource = self.pool.pop()
            resource = {
                JSON_FIELDS['IP']: raw_resource.ip,
                JSON_FIELDS['USERNAME']: raw_resource.username,
                JSON_FIELDS['PASSWORD']: raw_resource.password
            }
        elif self.count == self.max_amount:
            return None
        else:
            resource = self._create_resource()
            self.count += 1

        self.busy[resource[JSON_FIELDS['IP']]] = (resource[JSON_FIELDS['USERNAME']],
                                                  resource[JSON_FIELDS['PASSWORD']])
        return resource

    def release_resource(self, resource):
        resource_ip = resource[JSON_FIELDS['IP']]
        username, password = self.busy[resource_ip]
        del self.busy[resource_ip]
        raw_resource = Resource(resource_ip, username, password)
        self.pool.add(raw_resource)

    def is_busy(self, address):
        if JSON_FIELDS['IP'] not in address.keys():
            return False
        return address[JSON_FIELDS['IP']] in self.busy

    def _create_resource(self):
        resource = {
            JSON_FIELDS['IP']: self._ip_generator(),
            JSON_FIELDS['USERNAME']: self._username_generator(),
            JSON_FIELDS['PASSWORD']: self._password_generator()
        }
        return resource

    @staticmethod
    def _password_generator():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    def _username_generator(self):
        return 'user{}'.format(self.count)

    def _ip_generator(self):
        return '127.0.5.{}'.format(self.count)

