from flask import Flask, request, abort
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, PostbackEvent, FollowEvent, UnfollowEvent,
    JoinEvent, MemberJoinedEvent, MemberLeftEvent,
    TextSendMessage
)
from bin.Utility.Logger import log_manager
from bin.settings import line_bot_api, handler
from bin.MessageHandler import handle_message_event
from bin.PostbackHandler import handle_postback_event
from bin.FollowHandler import handle_follow_event, handle_unfollow_event, \
    handle_join_event, handle_member_join_event, handle_member_left_event
import traceback

app = Flask(__name__)

logger = log_manager(__file__)
my_id = ''

# https://plusplease.azurewebsites.net/callback


@app.route("/", methods=['GET'])
def root():
    print('this is CountMeIn')
    return 'this is CountMeIn'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    except BaseException as e:
        line_bot_api.push_message(
            my_id, 
            TextSendMessage(text=f'你GG了!!\n{traceback.format_exc()}')
        )
        raise e

    return 'OK'


@handler.add(PostbackEvent)
def handle_postback(event, destination):
    handle_postback_event(event)


@handler.add(MessageEvent)
def handle_message(event, destination):
    handle_message_event(event)


@handler.add(FollowEvent)
def handle_follow(event, destination):
    handle_follow_event(event)


@handler.add(UnfollowEvent)
def handle_follow(event, destination):
    handle_unfollow_event(event)


@handler.add(JoinEvent)
def handle_join(event, destination):
    handle_join_event(event)


@handler.add(MemberJoinedEvent)
def handle_member_join(event, destination):
    handle_member_join_event(event)


@handler.add(MemberLeftEvent)
def handle_member_join(event, destination):
    handle_member_left_event(event)


if __name__ == "__main__":
    app.run()