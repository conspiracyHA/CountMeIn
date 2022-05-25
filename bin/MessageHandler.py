from linebot.models import TextSendMessage, TemplateSendMessage, \
    MessageAction, PostbackAction, ConfirmTemplate, URIAction
from Utility.Logger import log_manager
from UserManager import user_manager
from ActivityManager import act_manager
from DatetimeParser import parse_datetime, true_dt_format, get_readable
from FlexMessage import *
from ReturnText import *
from settings import line_bot_api
from datetime import datetime
import json

logger = log_manager(__file__)

message_event = {
    "message": {
        "id": "13294588780697",
        "text": "996",
        "type": "text"
    },
    "mode": "active",
    "replyToken": "adbbb2eef74e49f4a4676fe8010048cd",
    "source": {
        "type": "user",
        "userId": "U5d86872dc301a38a805a7dd59f7c1cf2"
    },
    "timestamp": 1609333262309,
    "type": "message"
}


class GroupHandler:
    def __init__(self, event):
        self.event = event
        self.user_profile = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id)
        self.group_summary = line_bot_api.get_group_summary(event.source.group_id)
        user_manager.add_user(self.user_profile)
        user_manager.add_group(self.group_summary)
        user_manager.add_user_into_group(
            self.user_profile.user_id, self.group_summary.group_id
        )
        self._parse_text(event.message.text)

    def _parse_text(self, text):
        if text == '加加可以嗎':
            self._launch_activity()
        elif text == '查看活動':
            self._check_current_activities()
        elif text == '加加你滾':
            self._leave_group()

    def _launch_activity(self):
        if user_manager.is_followed(self.user_profile.user_id):
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
                    'group_id': self.group_summary.group_id
                }
            )
            self._ask_for_act_name()
            line_bot_api.reply_message(
                self.event.reply_token,
                already_pm
            )
        else:
            line_bot_api.reply_message(
                self.event.reply_token,
                need_to_follow
            )

    def _ask_for_act_name(self):
        group_name = self.group_summary.group_name
        group_id = self.group_summary.group_id
        line_bot_api.push_message(
            self.user_profile.user_id, get_create_act_flex(group_name)
        )

    def _check_current_activities(self):
        line_bot_api.reply_message(
            self.event.reply_token,
            function_not_designed
        )

    def _leave_group(self):
        user_manager.leave_group(self.group_summary.group_id)
        line_bot_api.reply_message(
            self.event.reply_token, leave_group_text
        )
        line_bot_api.leave_group(self.group_summary.group_id)


class UserHandler:
    def __init__(self, event):
        self.event = event
        self.user_profile = line_bot_api.get_profile(event.source.user_id)
        user_manager.add_user(self.user_profile)
        if self._launching_activity():
            return
        self._parse_text()

    def _launching_activity(self):
        user_status = user_manager.get_status(self.user_profile.user_id)
        if user_status.get('launching_activity'):
            if user_status['launching_activity'].get('name') is None:
                self._handle_activity_name()
            elif user_status['launching_activity'].get('deadline') is None:
                self._handle_activity_deadline()
            elif user_status['launching_activity'].get('details') is None:
                self._handle_activity_details()
            # 應該不會有這個 因為是用postback
            # if user_status['launching_activity'].get('invitation_method') is None:
            #     self._handle_activity_name()
            # if user_status['launching_activity'].get('max_participant') is None:
            #     self._handle_activity_participants()
            # if user_status['launching_activity'].get('options') is None:
            #     self._handle_activity_options()
            return True
        return False

    def _handle_activity_name(self):
        activity_name = self.event.message.text
        if len(activity_name) > 30:
            line_bot_api.reply_message(
                self.event.reply_token,
                name_too_long
            )
            return
        group_id = user_manager.get_status(self.user_profile.user_id)['launching_activity']['group_id']
        group_name = line_bot_api.get_group_summary(group_id).group_name
        line_bot_api.reply_message(
            self.event.reply_token,
            get_confirm_flex(
                '確認活動名稱',
                group_name,
                activity_name,
                yes_data={
                    'type': 'confirm_activity_name',
                    'data': {
                        'confirm': True,
                        'name': activity_name
                    }
                },
                no_data={
                    'type': 'confirm_activity_name',
                    'data': {
                        'confirm': False,
                        'name': activity_name
                    }
                },
            )
        )

    def _handle_activity_deadline(self):
        dt_str = self.event.message.text
        dt = parse_datetime(dt_str)
        if dt is None:
            line_bot_api.reply_message(
                self.event.reply_token,
                cannot_read_time
            )
            return
        if dt < datetime.now():
            line_bot_api.reply_message(
                self.event.reply_token,
                time_passed
            )
            return
        readable_dt = get_readable(dt)
        group_id = user_manager.get_status(self.user_profile.user_id)['launching_activity']['group_id']
        group_name = line_bot_api.get_group_summary(group_id).group_name
        line_bot_api.reply_message(
            self.event.reply_token,
            get_confirm_flex(
                '確認截止時間',
                group_name,
                readable_dt,
                yes_data={
                    'type': 'confirm_activity_deadline',
                    'data': {
                        'confirm': True,
                        'deadline': dt.strftime(true_dt_format)
                    }
                },
                no_data={
                    'type': 'confirm_activity_deadline',
                    'data': {
                        'confirm': False,
                        'deadline': dt.strftime(true_dt_format)
                    }
                },
            )
        )

    def _handle_activity_details(self):
        activity_details = self.event.message.text
        if len(activity_details) > 150:
            line_bot_api.reply_message(
                self.event.reply_token,
                details_too_long
            )
            return
        group_id = user_manager.get_status(self.user_profile.user_id)['launching_activity']['group_id']
        group_name = line_bot_api.get_group_summary(group_id).group_name
        line_bot_api.reply_message(
            self.event.reply_token,
            get_confirm_flex(
                '確認活動資訊',
                group_name,
                activity_details,
                yes_data={
                    'type': 'confirm_activity_details',
                    'data': {
                        'confirm': True,
                        'details': activity_details
                    }
                },
                no_data={
                    'type': 'confirm_activity_details',
                    'data': {
                        'confirm': False,
                        'details': activity_details
                    }
                },
            )
        )

    def _parse_text(self):
        # TODO
        text = self.event.message.text
        if text == '創建活動':
            self._ask_for_which_group_to_launch()
        elif text == '查看發布':
            self._check_launching()
        elif text == '查看封鎖':
            self._check_blocked()
        elif text == '查看活動':
            self._check_current_activities()
        elif text == '給我join text':
            line_bot_api.reply_message(
                self.event.reply_token,
                join_text
            )
        elif text == '指令說明':
            line_bot_api.reply_message(
                self.event.reply_token,
                get_manual()
            )
        elif text == '現在版本':
            line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    text='2021.02.07'
                )
            )

    def _ask_for_which_group_to_launch(self):
        group_list = user_manager.get_group_list(self.user_profile.user_id)
        line_bot_api.reply_message(
            self.event.reply_token,
            get_which_group_to_launch_activity(group_list)
        )

    def _check_launching(self):
        act_list = act_manager.get_launching(self.user_profile.user_id)
        line_bot_api.reply_message(
            self.event.reply_token,
            get_lauching_act(act_list)
        )

    def _check_blocked(self):
        ban_group_list = user_manager.get_ban_group(self.user_profile.user_id)
        ban_user_list = user_manager.get_ban_user(self.user_profile.user_id)
        ban_group_list = [
            {
                'group_name': user_manager.get_group_info(x).get('name', ''),
                'group_id': x
            } for x in ban_group_list
        ]
        ban_user_list = [
            {
                'user_name': user_manager.get_user_name(x),
                'user_id': x
            } for x in ban_user_list
        ]
        bubble_list = [
            get_ban_user_bubble(ban_user_list),
            get_ban_group_bubble(ban_group_list)
        ]
        line_bot_api.reply_message(
            self.event.reply_token,
            compose_bubble_to_carousel(bubble_list, '封鎖資訊')
        )

    def _check_current_activities(self):
        act_list = act_manager.get_user_act(self.user_profile.user_id)
        line_bot_api.reply_message(
            self.event.reply_token,
            function_not_designed
        )


def handle_message_event(event):
    if event.message.type == 'sticker':
        return
    source_type = event.source.type
    if source_type == 'group':
        GroupHandler(event)
    if source_type == 'user':
        UserHandler(event)