from Utility.Path import path_join
from Utility.Logger import log_manager
from DatetimeParser import true_dt_format
from UserManager import user_manager
from FlexMessage import get_act_result_flex, get_act_bubble
from linebot.models import FlexSendMessage
from threading import Lock, Thread
from functools import wraps
from datetime import datetime
from settings import line_bot_api
import json
import time
import uuid

path = path_join('activity.json')
activity_info_lock = Lock()

logger = log_manager(__file__)


def lock_decorator(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        with activity_info_lock:
            return func(*args, **kwargs)
    return wrapped


class ActivityManager:
    def __init__(self):
        with open(path, 'r', encoding='utf-8') as f:
            self.act_info = json.load(f)
        Thread(target=self._main, name='ActivityManager.main').start()

    @lock_decorator
    def _save(self):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.act_info, f, indent=4, ensure_ascii=False)
        # print('user info saved')
        # print(self.user_info)

    @lock_decorator
    def _check_act_status(self):
        self._check_finished()
        self._check_expired()

    def _check_finished(self):
        to_finished = list()
        for act_id, act_dict in self.act_info['confirming'].items():
            if len(act_dict['undetermined']) == 0:
                to_finished.append(act_id)
        for act_id in to_finished:
            self._push_act_result(act_id, self.act_info['confirming'][act_id])
        self.act_info['finished'].update({
            act_id: self.act_info['confirming'][act_id]
            for act_id in to_finished
        })
        self.act_info['confirming'] = {
            k: v for k, v in self.act_info['confirming'].items()
            if k not in to_finished
        }
        new_line = "\n"
        if to_finished:
            logger.info(f'to finished:\n'
                        f'{new_line.join(to_finished)}')

    def _check_expired(self):
        to_expired = list()
        for act_id, act_dict in self.act_info['confirming'].items():
            dt_str = act_dict['activity']['deadline']
            if datetime.strptime(dt_str, true_dt_format) < datetime.now():
                to_expired.append(act_id)

        for act_id in to_expired:
            self._push_act_result(act_id, self.act_info['confirming'][act_id])

        self.act_info['expired'].update({
            act_id: self.act_info['confirming'][act_id]
            for act_id in to_expired
        })
        self.act_info['confirming'] = {
            k: v for k, v in self.act_info['confirming'].items()
            if k not in to_expired
        }
        to_expired = list()

        for act_id, act_dict in self.act_info['finished'].items():
            dt_str = act_dict['activity']['deadline']
            if datetime.strptime(dt_str, true_dt_format) < datetime.now():
                to_expired.append(act_id)

        self.act_info['expired'].update({
            act_id: self.act_info['finished'][act_id]
            for act_id in to_expired
        })
        self.act_info['finished'] = {
            k: v for k, v in self.act_info['finished'].items()
            if k not in to_expired
        }

    def _push_act_result(self, act_id, act_dict):
        logger.info(f'activity[{act_id}] pushed')
        act_result_flex = self.get_act_result_flex(act_id)
        line_bot_api.push_message(
            act_dict['activity']['group_id'],
            act_result_flex
        )

    def get_act_result_flex(self, act_id):
        if act_id in self.act_info['confirming']:
            target = self.act_info['confirming']
        elif act_id in self.act_info['finished']:
            target = self.act_info['finished']
        elif act_id in self.act_info['expired']:
            target = self.act_info['expired']
        act_dict = target[act_id]
        new_line = '\n'
        attending = [
            user_manager.get_user_name(user_id)
            for user_id in act_dict['attending']
        ]
        declining = [
            user_manager.get_user_name(user_id)
            for user_id in act_dict['declining']
        ]
        return get_act_result_flex(
            act_dict["activity"]["name"],
            attending=new_line.join(attending),
            declining=new_line.join(declining),
            alt_text=f'活動[{act_dict["activity"]["name"]}]'
        )

    def _main(self):
        while True:
            self._check_act_status()
            self._save()
            time.sleep(30)

    @lock_decorator
    def create_act(self, user_id, activity, member_list):
        act_id = str(uuid.uuid1())
        logger.info(f'activity[{act_id}] created by user[{user_id}]')
        self.act_info['confirming'].update({
            act_id: {
                'creator': user_id,
                'activity': activity,
                'attending': [],
                'declining': [],
                'undetermined': member_list
            }
        })
        return act_id

    @lock_decorator
    def attend(self, act_id, user_id):
        if act_id not in self.act_info['confirming']:
            logger.debug(f'activity[{act_id}] not in confirming')
            return
        logger.info(f'user[{user_id}] attends activity[{act_id}]')
        if user_id not in self.act_info['confirming'][act_id]['attending']:
            self.act_info['confirming'][act_id]['attending'].append(user_id)
        self.act_info['confirming'][act_id]['undetermined'] = [
            x for x in self.act_info['confirming'][act_id]['undetermined'] if x != user_id
        ]

    @lock_decorator
    def decline(self, act_id, user_id):
        logger.info(f'user[{user_id}] declines activity[{act_id}]')
        if user_id not in self.act_info['confirming'][act_id]['declining']:
            self.act_info['confirming'][act_id]['declining'].append(user_id)
        self.act_info['confirming'][act_id]['undetermined'] = [
            x for x in self.act_info['confirming'][act_id]['undetermined'] if x != user_id
        ]

    @lock_decorator
    def get_launching(self, user_id):
        act_list = [
            dict(act_id=act_id,
                 creator_name=user_manager.get_user_name(act_dict['creator']),
                 **act_dict)
            for act_id, act_dict in self.act_info['confirming'].items()
            if user_id == act_dict['creator']
        ]
        act_list += [
            dict(act_id=act_id, **act_dict)
            for act_id, act_dict in self.act_info['finished'].items()
            if user_id == act_dict['creator']
        ]
        return act_list

    @lock_decorator
    def get_user_act(self, user_id, get_type='current'):
        attending = [
            dict(act_id=act_id,
                 creator_name=user_manager.get_user_name(act_dict['creator']),
                 **act_dict)
            for act_id, act_dict in self.act_info['confirming'].items()
            if user_id in act_dict['attending']
        ]
        attending += [
            dict(act_id=act_id,
                 creator_name=user_manager.get_user_name(act_dict['creator']),
                 **act_dict)
            for act_id, act_dict in self.act_info['finished'].items()
            if user_id in act_dict['attending']
        ]
        undetermined = [
            dict(act_id=act_id,
                 creator_name=user_manager.get_user_name(act_dict['creator']),
                 **act_dict)
            for act_id, act_dict in self.act_info['confirming'].items()
            if user_id in act_dict['undetermined']
        ]
        undetermined += [
            dict(act_id=act_id,
                 creator_name=user_manager.get_user_name(act_dict['creator']),
                 **act_dict)
            for act_id, act_dict in self.act_info['finished'].items()
            if user_id in act_dict['undetermined']
        ]

    @lock_decorator
    def get_act_bubble(self, act_id):
        if act_id in self.act_info['confirming']:
            target = self.act_info['confirming']
        elif act_id in self.act_info['finished']:
            target = self.act_info['finished']
        elif act_id in self.act_info['expired']:
            target = self.act_info['expired']
        param = {
            k: v for k, v in target[act_id]['activity'].items()
            if k in ['name', 'deadline', 'details']
        }
        param.update({
            'creator': user_manager.get_user_name(target[act_id]['creator']),
            'act_id': act_id
        })
        return get_act_bubble(**param)



act_manager = ActivityManager()


