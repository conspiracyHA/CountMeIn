from UserManager import user_manager
from Utility.Logger import log_manager
from linebot.models import TextSendMessage
from settings import line_bot_api
from ReturnText import follow_text, join_text

logger = log_manager(__file__)


def handle_follow_event(event):
    source_type = event.source.type
    print(f'follow event, source_type: {source_type}')
    user_profile = line_bot_api.get_profile(event.source.user_id)
    user_manager.add_user(user_profile, True)
    line_bot_api.reply_message(
        event.reply_token, follow_text
    )


def handle_unfollow_event(event):
    user_name = user_manager.add_unfollow_user(event.source.user_id)
    if user_name is not None:
        logger.info(f'{user_name} 不想加加了')


def handle_join_event(event):
    user_manager.add_group(line_bot_api.get_group_summary(event.source.group_id))
    line_bot_api.reply_message(event.reply_token, join_text)


def handle_member_join_event(event):
    user_profile = line_bot_api.get_profile(event.source.user_id)
    group_summary = line_bot_api.get_group_summary(event.source.group_id)
    user_manager.add_user(user_profile)
    user_manager.add_group(group_summary)
    user_manager.add_user_into_group(user_profile.user_id, group_summary.group_id)


def handle_member_left_event(event):
    user_manager.del_user_from_group(event.source.user_id, event.source.group_id)
    pass

