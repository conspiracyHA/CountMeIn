from Utility.Path import path_join
from Utility.Logger import log_manager
from threading import Lock, Thread
from functools import wraps
from settings import line_bot_api
import json
import time
import copy

path = path_join('user_info.json')
user_info_lock = Lock()

logger = log_manager(__file__)


def lock_decorator(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        with user_info_lock:
            return func(*args, **kwargs)
    return wrapped


class UserManager:
    def __init__(self):
        with open(path, 'r', encoding='utf-8') as f:
            self.user_info = json.load(f)

        Thread(target=self._main, name='UserManager.main').start()

    @lock_decorator
    def _save(self):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.user_info, f, indent=4, ensure_ascii=False)
        # print('user info saved')
        # print(self.user_info)

    def _main(self):
        while True:
            self._save()
            time.sleep(5)

    @lock_decorator
    def add_group(self, group_summary):
        if group_summary.group_id in self.user_info['group']:
            self.user_info['group'][group_summary.group_id].update({
                'name': group_summary.group_name
            })
            return
        logger.info(f'add group[{group_summary.group_id}]')
        self.user_info['group'][group_summary.group_id] = {
            'name': group_summary.group_name,
            'members': []
        }
        # print('in add group', self.user_info)

    @lock_decorator
    def add_user_into_group(self, user_id, group_id):
        if user_id not in self.user_info['group'][group_id]['members']:
            logger.info(f'add user[{user_id}] into group[{group_id}]')
            self.user_info['group'][group_id]['members'].append(user_id)

        if group_id not in self.user_info['user'][user_id]['groups']:
            self.user_info['user'][user_id]['groups'].append(group_id)

    @lock_decorator
    def del_user_from_group(self, user_id, group_id):
        if user_id in self.user_info['group'][group_id]['members']:
            logger.info(f'delete user[{user_id}] from group[{group_id}]')
            self.user_info['group'][group_id]['members'] = [
                x for x in self.user_info['group'][group_id]['members']
                if x != user_id
            ]

        if group_id not in self.user_info['user'][user_id]['groups']:
            self.user_info['user'][user_id]['groups'] = [
                x for x in self.user_info['user'][user_id]['groups']
                if x != group_id
            ]

    @lock_decorator
    def add_user(self, user_profile, followed=False):
        if user_profile.user_id in self.user_info['user']:
            self.user_info['user'][user_profile.user_id].update({
                'name': user_profile.display_name
            })
            if followed:
                self.user_info['user'][user_profile.user_id].update({
                    'followed': True
                })

            return
        logger.info(f'add user[{user_profile.user_id}]')
        self.user_info['user'][user_profile.user_id] = {
            'name': user_profile.display_name,
            'groups': [],
            'followed': followed,
            'status': {},
            'ban_user': [],
            'ban_group': []
        }

    @lock_decorator
    def add_unfollow_user(self, user_id):
        if user_id in self.user_info['user']:
            logger.info(f'add unfollow user[{user_id}]')
            self.user_info['user'][user_id].update({
                'followed': False
            })
            return self.user_info['user'][user_id]['name']
        logger.error(f'沒有這個user啊!! => {user_id}')
        return None

    @lock_decorator
    def is_followed(self, user_id):
        if user_id in self.user_info['user']:
            return self.user_info['user'][user_id]['followed'] is True
        return False

    @lock_decorator
    def update_status(self, user_id, *args):
        target = self.user_info['user'][user_id]['status']
        while len(args) > 2:
            # print(args)
            key, args = args[0], args[1:]
            target = target[key]
        target.update({args[0]: args[1]})
        # print('update: ', {args[0]: args[1]})

    @lock_decorator
    def delete_status(self, user_id, status_key):
        if status_key in self.user_info['user'][user_id]['status']:
            del self.user_info['user'][user_id]['status'][status_key]
        else:
            logger.warning(
                'no such key in user status:\n'
                'key: [{status_key}]\n'
                'user_id:{user_id}'
            )

    @lock_decorator
    def get_status(self, user_id):
        return copy.deepcopy(self.user_info['user'][user_id]['status'])

    @lock_decorator
    def get_group_info(self, group_id):
        return copy.deepcopy(self.user_info['group'][group_id])

    @lock_decorator
    def ban_user(self, user_id, target):
        self.user_info['user'][user_id]['ban_user'].append(target)

    @lock_decorator
    def ban_group(self, user_id, target):
        self.user_info['user'][user_id]['ban_group'].append(target)

    @lock_decorator
    def get_user_name(self, user_id):
        return self.user_info['user'][user_id]['name']

    @lock_decorator
    def filter_invite_members(self, group_id, user_id, member_list):
        result = [
            member_id for member_id in member_list
            if user_id not in self.user_info['user'][member_id]['ban_user'] and
               group_id not in self.user_info['user'][member_id]['ban_group']
        ]
        return result

    @lock_decorator
    def get_group_list(self, user_id):
        result = [{
            'name': line_bot_api.get_group_summary(group_id).group_name,
            'group_id': group_id
        } for group_id in self.user_info['user'][user_id]['groups']]
        return result

    @lock_decorator
    def get_ban_group(self, user_id):
        return self.user_info['user'].get(user_id, {}).get('ban_group', [])

    @lock_decorator
    def get_ban_user(self, user_id):
        return self.user_info['user'].get(user_id, {}).get('ban_user', [])

    @lock_decorator
    def cancel_ban_user(self, user_id, ban_user_id):
        self.user_info['user'][user_id]['ban_user'] = [
            x for x in self.user_info['user'][user_id]['ban_user']
            if x != ban_user_id
        ]

    @lock_decorator
    def cancel_ban_group(self, user_id, ban_group_id):
        self.user_info['user'][user_id]['ban_user'] = [
            x for x in self.user_info['user'][user_id]['ban_group']
            if x != ban_group_id
        ]

    @lock_decorator
    def leave_group(self, group_id):
        del self.user_info['group'][group_id]
        for user_id, user_dict in self.user_info['user'].items():
            user_dict['groups'] = [x for x in user_dict['groups'] if x != group_id]


user_manager = UserManager()

