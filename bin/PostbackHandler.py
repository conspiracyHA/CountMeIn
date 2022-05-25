from Utility.Logger import log_manager
from UserManager import user_manager
from ActivityManager import act_manager
from FlexMessage import *
from ReturnText import *
from DatetimeParser import true_dt_format, get_readable
from settings import line_bot_api
from linebot.models import TextSendMessage, TemplateSendMessage, \
    MessageAction, PostbackAction, ConfirmTemplate, URIAction, \
    ButtonsTemplate, FlexSendMessage
from datetime import datetime, timedelta
import json
import inspect
import time

logger = log_manager(__file__)

POSTBACK_TIMEOUT_TIMEDELTA = timedelta(seconds=10)

postback_event = {
    "mode": "active",
    "postback": {
        "data": "action=buy&itemid=1"
    },
    "replyToken": "9471a33404e349a3818d224c3f797083",
    "source": {
        "type": "user",
        "userId": "U5d86872dc301a38a805a7dd59f7c1cf2"
    },
    "timestamp": 1609332894770,
    "type": "postback"
}


class PostbackTimeoutManager:
    def __init__(self):
        # _postback_id2user_id2time
        self.always = dict()
        self.timeout = dict()

    def add_always(self, postback_id, user_id):
        if postback_id in self.always:
            if user_id in self.always[postback_id]:
                return False
            self.always[postback_id][user_id] = True
            return True
        self.always[postback_id] = {user_id: True}
        return True

    def add_timeout(self, postback_id, user_id):
        if postback_id in self.timeout:
            if user_id in self.timeout[postback_id]:
                if datetime.now() > self.timeout[postback_id][user_id] + POSTBACK_TIMEOUT_TIMEDELTA:
                    self.timeout[postback_id][user_id] = datetime.now()
                    return True
                return False
            self.timeout[postback_id][user_id] = datetime.now()
            return True
        self.timeout[postback_id] = {user_id: datetime.now()}
        return True

    def add_postback(self, data, user_id):
        if 'postback_id' not in data:
            logger.error(f'postback_id not found in data: {data}')
            return False
        if 'timeout_type' not in data:
            logger.error(f'timeout_type not found in data: {data}')
            return False
        postback_id = data['postback_id']
        timeout_type = data['timeout_type']
        if timeout_type == 'always':
            return self.add_always(postback_id, user_id)
        elif timeout_type == 'timeout':
            return self.add_timeout(postback_id, user_id)


postback_timeout_manager = PostbackTimeoutManager()


class GroupHandler:
    def __init__(self, event):
        self.event = event
        self.user_profile = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id)
        self.group_summary = line_bot_api.get_group_summary(event.source.group_id)
        user_manager.add_user(self.user_profile)
        user_manager.add_group(self.group_summary)
        user_manager.add_user_into_group(
            self.user_profile.user_id, self.group_summary.group_id)
        self._parse_data(event.postback.data)

    def _parse_data(self, postback_data):
        data = json.loads(postback_data)
        if postback_timeout_manager.add_postback(data, self.user_profile.user_id) is False:
            return
        data_type = data.get('type')
        if data_type is None:
            logger.error(
                f'[{self.__class__.__name__}].' + inspect.stack()[0][3] +
                'postback_data does not have type!! event:\n' +
                json.dumps(
                    json.loads(
                        str(self.event)
                    ), ensure_ascii=False, indent=4
                )
            )
            return
        elif data_type == 'activity_invitation':
            self._handle_activity_invitation(data.get('data'))

    def _handle_activity_invitation(self, data):
        confirm = data.get('confirm')
        if confirm is None:
            logger.warning(
                f'[{self.__class__.__name__}].' + inspect.stack()[0][3] +
                'no confirm in data!! data:\n' +
                json.dumps(data, ensure_ascii=False, indent=4)
            )
        if confirm:
            act_id = data.get('act_id')
            act_manager.attend(act_id, self.user_profile.user_id)
        else:
            act_id = data.get('act_id')
            act_manager.decline(act_id, self.user_profile.user_id)


class UserHandler:
    def __init__(self, event):
        self.event = event
        self.user_profile = line_bot_api.get_profile(event.source.user_id)
        user_manager.add_user(self.user_profile)
        self._parse_data(event.postback.data)

    def _parse_data(self, postback_data):
        data = json.loads(postback_data)
        if postback_timeout_manager.add_postback(data, self.user_profile.user_id) is False:
            return
        data_type = data.get('type')
        if data_type is None:
            logger.error(
                f'[{self.__class__.__name__}].' + inspect.stack()[0][3] +
                'postback_data does not have type!! event:\n' +
                json.dumps(
                    json.loads(
                        str(self.event)
                    ), ensure_ascii=False, indent=4
                )
            )
            return
        if data_type == 'cancel_activity':
            self._handle_cancel_activity(data.get('data'))
            return

        if data_type == 'choose_group_to_launch':
            self._handle_choose_group_to_launch(data.get('data'))
            return

        if data_type == 'confirm_activity_name':
            self._handle_activity_name(data.get('data'))
            self._ask_for_activity_info()
            return
        if data_type == 'confirm_activity_deadline':
            self._handle_activity_deadline(data.get('data'))
            self._ask_for_activity_info()
            return
        if data_type == 'confirm_activity_details':
            self._handle_activity_details(data.get('data'))
            self._ask_for_activity_info()
            return
        if data_type == 'invitation_method':
            self._handle_activity_invitation_method(data.get('data'))
            self._ask_for_activity_info()
            return

        if data_type == 'send_invitation':
            self._handle_send_invitation(data.get('data'))
            return
        if data_type == 'change_act_info':
            self._handle_change_act_info(data.get('data'))
            self._ask_for_activity_info()
            return

        if data_type == 'activity_invitation':
            self._handle_activity_invitation(data.get('data'))

        if data_type == 'show_act':
            self._handle_show_act(data.get('data'))
        if data_type == 'show_act_attending':
            self._handle_show_act_attending(data.get('data'))
        if data_type == 'cancel_ban_user':
            self._handle_cancel_ban_user(data.get('data'))
        if data_type == 'cancel_ban_group':
            self._handle_cancel_ban_group(data.get('data'))

    def _ask_for_activity_info(self):
        user_status = user_manager.get_status(self.user_profile.user_id)
        if user_status.get('launching_activity'):
            group_id = user_manager.get_status(self.user_profile.user_id)['launching_activity']['group_id']
            group_name = line_bot_api.get_group_summary(group_id).group_name
            if user_status['launching_activity'].get('name') is None:
                self._ask_for_name(group_name)
            elif user_status['launching_activity'].get('deadline') is None:
                self._ask_for_deadline(group_name)
            elif user_status['launching_activity'].get('details') is None:
                self._ask_for_details(group_name)
            elif user_status['launching_activity'].get('invitation_method') is None:
                self._ask_for_invitation_method(group_name)
            else:
                self._ask_if_send_invitation()

    def _ask_for_name(self, group_name):
        line_bot_api.reply_message(
            self.event.reply_token,
            get_create_act_flex(group_name)
        )

    def _ask_for_deadline(self, group_name):
        line_bot_api.reply_message(
            self.event.reply_token,
            get_ask_for_things_flex('deadline', group_name)
        )

    def _ask_for_details(self, group_name):
        line_bot_api.reply_message(
            self.event.reply_token,
            get_ask_for_things_flex('details', group_name)
        )

    def _ask_for_invitation_method(self, group_name):
        line_bot_api.reply_message(
            self.event.reply_token,
            get_ask_for_invitation_method_flex(group_name)
        )

    def _ask_if_send_invitation(self):
        group_id = user_manager.get_status(self.user_profile.user_id)['launching_activity']['group_id']
        group_name = line_bot_api.get_group_summary(group_id).group_name
        activity = user_manager.get_status(self.user_profile.user_id).get('launching_activity')
        invitation_method_text = '私訊' if activity['invitation_method'] == 'private' else '群組'
        text = f'您即將發起一個活動\n' \
               f'活動名稱: {activity["name"]}\n' \
               f'活動資訊:\n{activity["details"]}\n' \
               f'截止時間: {activity["deadline"]}\n\n' \
               f'這則邀請將透過[{invitation_method_text}]發送\n\n' \
               f'確定要發送邀請嗎?'

        line_bot_api.reply_message(
            self.event.reply_token,
            get_confirm_flex(
                title="確定發送活動邀請?",
                group_name=group_name,
                content=text,
                yes_data={
                    'type': 'send_invitation',
                    'data': {
                        'confirm': True
                    }
                },
                no_data={
                    'type': 'send_invitation',
                    'data': {
                        'confirm': False
                    }
                }
            )
        )

    def _handle_cancel_activity(self, data):
        cancel = data.get('cancel')
        if cancel:
            user_manager.delete_status(
                self.user_profile.user_id, 'launching_activity'
            )
            line_bot_api.reply_message(
                self.event.reply_token,
                sorry_text
            )
            return
        logger.warning(f'in create_activity, weird data received:\ndata')

    def _handle_choose_group_to_launch(self, data):
        group_id = data.get('group_id')
        if group_id is None:
            logger.warning(
                f'[{self.__class__.__name__}].' + inspect.stack()[0][3] +
                'no group_id in data!! data:\n' +
                json.dumps(data, ensure_ascii=False, indent=4)
            )
            return
        user_manager.update_status(
            self.user_profile.user_id,
            'launching_activity',
            {
                'name': None,
                'deadline': None,
                'details': None,
                'max_participant': None,
                'invitation_method': None,
                'options': ['參加', '不參加'],
                'group_id': group_id
            }
        )
        line_bot_api.reply_message(
            self.event.reply_token,
            get_create_act_flex(line_bot_api.get_group_summary(group_id).group_name)
        )

    def _handle_activity_name(self, data):
        confirm = data.get('confirm')
        if confirm is None:
            logger.warning(
                f'[{self.__class__.__name__}].' + inspect.stack()[0][3] +
                'no confirm in data!! data:\n' +
                json.dumps(data, ensure_ascii=False, indent=4)
            )
        if confirm:
            user_manager.update_status(
                self.user_profile.user_id,
                'launching_activity',
                'name',
                data.get('name')
            )

    def _handle_activity_deadline(self, data):
        confirm = data.get('confirm')
        if confirm is None:
            logger.warning(
                f'[{self.__class__.__name__}].' + inspect.stack()[0][3] +
                'no confirm in data!! data:\n' +
                json.dumps(data, ensure_ascii=False, indent=4)
            )
        if confirm:
            user_manager.update_status(
                self.user_profile.user_id,
                'launching_activity',
                'deadline',
                data.get('deadline')
            )

    def _handle_activity_details(self, data):
        confirm = data.get('confirm')
        if confirm is None:
            logger.warning(
                f'[{self.__class__.__name__}].' + inspect.stack()[0][3] +
                'no confirm in data!! data:\n' +
                json.dumps(data, ensure_ascii=False, indent=4)
            )
        if confirm:
            user_manager.update_status(
                self.user_profile.user_id,
                'launching_activity',
                'details',
                data.get('details')
            )

    def _handle_activity_invitation_method(self, data):
        invitation_method = data.get('invitation_method')
        if invitation_method is None:
            logger.warning(
                f'[{self.__class__.__name__}].' + inspect.stack()[0][3] +
                'no invitation_method in data!! data:\n' +
                json.dumps(data, ensure_ascii=False, indent=4)
            )
        user_manager.update_status(
            self.user_profile.user_id,
            'launching_activity',
            'invitation_method',
            invitation_method
        )

    def _handle_send_invitation(self, data):
        confirm = data.get('confirm')
        if confirm is None:
            logger.warning(
                f'[{self.__class__.__name__}].' + inspect.stack()[0][3] +
                'no confirm in data!! data:\n' +
                json.dumps(data, ensure_ascii=False, indent=4)
            )
        if confirm:
            activity_info = user_manager.get_status(self.user_profile.user_id)['launching_activity']
            user_manager.delete_status(self.user_profile.user_id, 'launching_activity')
            group_info = user_manager.get_group_info(activity_info['group_id'])
            member_list = group_info['members']
            group_name = group_info['name']
            act_id = act_manager.create_act(
                self.user_profile.user_id, activity_info, member_list
            )
            member_list = user_manager.filter_invite_members(
                activity_info['group_id'], self.user_profile.user_id, member_list
            )

            creator = self.user_profile.display_name
            dt = datetime.strptime(activity_info['deadline'], true_dt_format)
            deadline = get_readable(dt)
            gggg_flex = get_private_act_flex(
                        activity_info["name"],
                        creator,
                        activity_info["details"],
                        deadline,
                        yes_data={
                            'type': 'activity_invitation',
                            'data': {
                                'act_id': act_id,
                                'confirm': True
                            }
                        },
                        no_data={
                            'type': 'activity_invitation',
                            'data': {
                                'act_id': act_id,
                                'confirm': False
                            }
                        },
                        block_group_data={
                            'type': 'activity_invitation',
                            'data': {
                                'act_id': act_id,
                                'confirm': False,
                                'block': 'group'
                            }
                        },
                        block_user_data={
                            'type': 'activity_invitation',
                            'data': {
                                'act_id': act_id,
                                'confirm': False,
                                'block': 'user'
                            }
                        },
                        alt_text=f'來自[{group_name}] {self.user_profile.display_name} 的邀請'
                    )
            if activity_info['invitation_method'] == 'private':
                newline = '\n'
                logger.info(f'multicast invitation to:\n{newline.join(member_list)}')
                line_bot_api.multicast(
                    member_list,
                    gggg_flex
                )
            elif activity_info['invitation_method'] == 'group':
                line_bot_api.push_message(
                    activity_info['group_id'],
                    get_group_act_flex(
                        activity_info["name"],
                        creator,
                        activity_info["details"],
                        deadline,
                        yes_data={
                            'type': 'activity_invitation',
                            'data': {
                                'act_id': act_id,
                                'confirm': True
                            }
                        },
                        no_data={
                            'type': 'activity_invitation',
                            'data': {
                                'act_id': act_id,
                                'confirm': False
                            }
                        },
                        alt_text=f'來自 {self.user_profile.display_name} 的邀請'
                    )
                )
            line_bot_api.reply_message(
                self.event.reply_token,
                invitation_sent
            )
        else:
            group_id = user_manager.get_status(self.user_profile.user_id)['launching_activity']['group_id']
            group_name = line_bot_api.get_group_summary(group_id).group_name
            # user_manager.delete_status(self.user_profile.user_id, 'launching_activity')
            line_bot_api.reply_message(
                self.event.reply_token,
                get_which_info_to_change_flex(group_name)
                # TODO 了解為何size會超過500
            )

    def _handle_change_act_info(self, data):
        change_act_info = data.get('change_act_info')
        if change_act_info is None:
            logger.warning(
                f'[{self.__class__.__name__}].' + inspect.stack()[0][3] +
                'no change_act_info in data!! data:\n' +
                json.dumps(data, ensure_ascii=False, indent=4)
            )
        if change_act_info == 'name':
            user_manager.update_status(
                self.user_profile.user_id,
                'launching_activity',
                'name',
                None
            )
        if change_act_info == 'deadline':
            user_manager.update_status(
                self.user_profile.user_id,
                'launching_activity',
                'deadline',
                None
            )
        if change_act_info == 'details':
            user_manager.update_status(
                self.user_profile.user_id,
                'launching_activity',
                'details',
                None
            )
        if change_act_info == 'invitation_method':
            user_manager.update_status(
                self.user_profile.user_id,
                'launching_activity',
                'invitation_method',
                None
            )

    def _handle_activity_invitation(self, data):
        confirm = data.get('confirm')
        text = '收到'
        if confirm is None:
            logger.warning(
                f'[{self.__class__.__name__}].' + inspect.stack()[0][3] +
                'no confirm in data!! data:\n' +
                json.dumps(data, ensure_ascii=False, indent=4)
            )
        if confirm:
            act_id = data.get('act_id')
            act_manager.attend(act_id, self.user_profile.user_id)
            text = '收到，已幫您紀錄'
        else:
            act_id = data.get('act_id')
            act_manager.decline(act_id, self.user_profile.user_id)
            block = data.get('block')
            if block is None:
                text = '收到，已幫您紀錄'
            if block == 'user':
                act_info = act_manager.get_activity(act_id)
                user_manager.ban_user(self.user_profile.user_id, act_info['creator'])
                text = '收到 以後將不會再傳送由此使用者發布的邀請'
            elif block == 'group':
                act_info = act_manager.get_activity(act_id)
                user_manager.ban_group(self.user_profile.user_id, act_info['group_id'])
                text = '收到 以後將不會再傳送此群組的邀請'
        line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(text=text)
        )

    def _handle_show_act(self, data):
        act_id = data.get('act_id')
        bubble = act_manager.get_act_bubble(act_id)
        line_bot_api.reply_message(
            self.event.reply_token,
            compose_bubble_to_carousel([bubble], alt_text='活動資訊')
        )

    def _handle_show_act_attending(self, data):
        act_id = data.get('act_id')
        line_bot_api.reply_message(
            self.event.reply_token,
            act_manager.get_act_result_flex(act_id)
        )

    def _handle_cancel_ban_user(self, data):
        user_manager.cancel_ban_user(self.user_profile.user_id, data.get('user_id'))
        line_bot_api.reply_message(
            self.event.reply_token,
            cancel_text
        )

    def _handle_cancel_ban_group(self, data):
        user_manager.cancel_ban_group(self.user_profile.user_id, data.get('group_id'))
        line_bot_api.reply_message(
            self.event.reply_token,
            cancel_text
        )



def handle_postback_event(event):
    source_type = event.source.type
    if source_type == 'group':
        GroupHandler(event)
    if source_type == 'user':
        UserHandler(event)
