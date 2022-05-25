from linebot.models import FlexSendMessage
import json
import time


def _get_cancel_act_data():
    postback_id = str(time.time()).replace('.', '')
    result = json.dumps({
        'type': 'cancel_activity',
        'data': {
            'cancel': True,
        },
        'postback_id': postback_id,
        'timeout_type': 'always'
    }, ensure_ascii=False)
    return result


def get_group_act_flex(
        act_name, creator, act_details, deadline,
        yes_data, no_data, alt_text='群組活動邀請'):
    postback_id = str(time.time()).replace('.', '')
    yes_data.update({
        'postback_id': postback_id,
        'timeout_type': 'timeout'
    })
    no_data.update({
        'postback_id': postback_id,
        'timeout_type': 'timeout'
    })
    yes_data = json.dumps(yes_data, ensure_ascii=False)
    no_data = json.dumps(no_data, ensure_ascii=False)
    result = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "flex": 0,
            "contents": [
                {
                    "type": "text",
                    "text": act_name,
                    "weight": "bold",
                    "size": "xl",
                    "color": "#010101FF",
                    "align": "center",
                    "gravity": "center",
                    "margin": "none",
                    "wrap": False,
                    "contents": [],
                    "decoration": "none"
                }
            ],
            "paddingAll": "lg",
            "paddingBottom": "md"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "發起人",
                                    "align": "start",
                                    "gravity": "center",
                                    "style": "italic",
                                    "contents": []
                                },
                                {
                                    "type": "text",
                                    "text": creator,
                                    "weight": "regular",
                                    "align": "end",
                                    "gravity": "center",
                                    "contents": []
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "活動資訊",
                                    "contents": [],
                                    "style": "italic"
                                },
                                {
                                    "type": "text",
                                    "text": act_details,
                                    "color": "#000000",
                                    "align": "center",
                                    "gravity": "center",
                                    "margin": "md",
                                    "wrap": True,
                                    "contents": [],
                                    "weight": "regular"
                                }
                            ]
                        },
                        {
                            "type": "separator"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "截止時間",
                                    "color": "#AAAAAA",
                                    "contents": [],
                                    "style": "italic"
                                },
                                {
                                    "type": "text",
                                    "text": deadline,
                                    "color": "#AAAAAA",
                                    "contents": [],
                                    "style": "italic"
                                }
                            ]
                        },
                        {
                            "type": "separator"
                        }
                    ]
                }
            ],
            "borderWidth": "none",
            "paddingTop": "none"
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "參加",
                        "data": yes_data
                    },
                    "color": "#905C44",
                    "height": "sm",
                    "style": "primary",
                    "margin": "none"
                },
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "不參加",
                        "data": no_data
                    },
                    "color": "#905C44",
                    "height": "sm",
                    "style": "primary",
                    "margin": "lg"
                }
            ],
            "paddingAll": "xl",
            "paddingTop": "none"
        }
    }
    return FlexSendMessage(alt_text=alt_text, contents=result)


def get_private_act_flex(
        act_name, creator, act_details, deadline,
        yes_data, no_data, block_group_data, block_user_data, alt_text='活動邀請'):
    postback_id = str(time.time()).replace('.', '')
    yes_data.update({
        'postback_id': postback_id,
        'timeout_type': 'timeout'
    })
    no_data.update({
        'postback_id': postback_id,
        'timeout_type': 'timeout'
    })
    block_group_data.update({
        'postback_id': postback_id,
        'timeout_type': 'always'
    })
    block_user_data.update({
        'postback_id': postback_id,
        'timeout_type': 'always'
    })
    yes_data = json.dumps(yes_data, ensure_ascii=False)
    no_data = json.dumps(no_data, ensure_ascii=False)
    block_group_data = json.dumps(block_group_data, ensure_ascii=False)
    block_user_data = json.dumps(block_user_data, ensure_ascii=False)
    result = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "flex": 0,
            "contents": [
                {
                    "type": "text",
                    "text": act_name,
                    "weight": "bold",
                    "size": "xl",
                    "color": "#010101FF",
                    "align": "center",
                    "gravity": "center",
                    "margin": "none",
                    "wrap": False,
                    "contents": [],
                    "decoration": "none"
                }
            ],
            "paddingAll": "lg",
            "paddingBottom": "md"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "發起人",
                                    "align": "start",
                                    "gravity": "center",
                                    "style": "italic",
                                    "contents": []
                                },
                                {
                                    "type": "text",
                                    "text": creator,
                                    "weight": "regular",
                                    "align": "end",
                                    "gravity": "center",
                                    "contents": []
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "活動資訊",
                                    "contents": [],
                                    "style": "italic"
                                },
                                {
                                    "type": "text",
                                    "text": act_details,
                                    "color": "#000000",
                                    "align": "center",
                                    "gravity": "center",
                                    "margin": "md",
                                    "wrap": True,
                                    "contents": [],
                                    "weight": "regular"
                                }
                            ]
                        },
                        {
                            "type": "separator"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "截止時間",
                                    "color": "#AAAAAA",
                                    "contents": [],
                                    "style": "italic"
                                },
                                {
                                    "type": "text",
                                    "text": deadline,
                                    "color": "#AAAAAA",
                                    "contents": [],
                                    "style": "italic"
                                }
                            ]
                        },
                        {
                            "type": "separator"
                        }
                    ]
                }
            ],
            "borderWidth": "none",
            "paddingTop": "none"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "參加",
                                "data": yes_data
                            },
                            "color": "#905C44",
                            "height": "sm",
                            "style": "primary",
                            "margin": "none"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "不參加",
                                "data": no_data
                            },
                            "color": "#905C44",
                            "height": "sm",
                            "style": "primary",
                            "margin": "lg"
                        }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "封鎖來自這個群組的邀請",
                                "data": block_group_data
                            },
                            "color": "#905C44",
                            "height": "sm",
                            "style": "primary",
                            "margin": "none"
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "封鎖來自這個使用者的邀請",
                                "data": block_user_data
                            },
                            "color": "#905C44",
                            "height": "sm",
                            "style": "primary",
                            "margin": "lg"
                        }
                    ]
                }
            ],
            "paddingAll": "xl",
            "paddingTop": "none"
        }
    }
    return FlexSendMessage(alt_text=alt_text, contents=result)


def get_act_result_flex(act_name, attending, declining, alt_text='活動統計結果'):
    result = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "flex": 0,
            "contents": [
                {
                    "type": "text",
                    "text": act_name,
                    "weight": "bold",
                    "size": "xl",
                    "color": "#010101FF",
                    "align": "center",
                    "gravity": "center",
                    "margin": "none",
                    "wrap": False,
                    "contents": [],
                    "decoration": "none",
                    "style": "normal"
                },
                {
                    "type": "text",
                    "text": "已經統計完畢",
                    "align": "center",
                    "color": "#AAAAAA",
                    "size": "sm"
                }
            ],
            "paddingAll": "lg",
            "paddingBottom": "md"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "參加",
                            "weight": "bold",
                            "size": "lg"
                        },
                        {
                            "type": "text",
                            "text": attending,
                            "wrap": True,
                            "offsetStart": "sm"
                        }
                    ]
                },
                {
                    "type": "separator"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "不參加",
                            "weight": "bold",
                            "size": "lg"
                        },
                        {
                            "type": "text",
                            "text": declining,
                            "wrap": True,
                            "offsetStart": "sm"
                        }
                    ]
                }
            ],
            "borderWidth": "none",
            "paddingTop": "none"
        }
    }
    if not attending:
        tmp = {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "參加",
                    "weight": "bold",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": "沒有人QQ",
                    "wrap": True,
                    "offsetStart": "sm",
                    "style": "italic",
                    "color": "#AAAAAA"
                }
            ]
        }
        result['body']['contents'][0] = tmp

    if not declining:
        result['body']['contents'] = [result['body']['contents'][0]]
    # print(json.dumps(result, ensure_ascii=False, indent=2))
    return FlexSendMessage(alt_text=alt_text, contents=result)


def wake_up_response(group=True):
    pass


# 決定要創活動，準備輸入活動名稱 (或取消)
def get_create_act_flex(group_name):
    result = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "活動名稱",
                    "style": "normal",
                    "weight": "bold",
                    "align": "center",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": f"你即將在[{group_name}]中創建活動",
                    "size": "sm",
                    "align": "center",
                    "color": "#AAAAAA"
                }
            ],
            "margin": "none",
            "spacing": "none",
            "paddingAll": "none",
            "paddingTop": "lg"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "請輸入活動名稱 (30字以內)",
                    "wrap": True,
                    "align": "start"
                },
                {
                    "type": "text",
                    "text": "或點擊[取消]已取消活動",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "align": "start"
                }
            ],
            "paddingAll": "sm",
            "paddingStart": "md"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "取消",
                        "data": _get_cancel_act_data()
                    }
                }
            ],
            "flex": 0,
            "paddingAll": "xs"
        }
    }
    return FlexSendMessage(alt_text=f'在[{group_name}]中創建活動', contents=result)


# 確認活動名稱(或取消)
def get_confirm_flex(title, group_name, content, yes_data, no_data):
    postback_id = str(time.time()).replace('.', '')
    yes_data.update({
        'postback_id': postback_id,
        'timeout_type': 'always'
    })
    no_data.update({
        'postback_id': postback_id,
        'timeout_type': 'always'
    })
    yes_data = json.dumps(yes_data, ensure_ascii=False)
    no_data = json.dumps(no_data, ensure_ascii=False)
    result = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "style": "normal",
                    "weight": "bold",
                    "align": "center",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": f"你即將在[{group_name}]中創建活動",
                    "size": "sm",
                    "align": "center",
                    "color": "#AAAAAA"
                }
            ],
            "margin": "none",
            "spacing": "none",
            "paddingAll": "none",
            "paddingTop": "lg"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "wrap": True,
                    "align": "center",
                    "contents": [],
                    "text": content,
                    "size": "lg",
                    "weight": "bold"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "或點擊[取消]以取消活動",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "align": "start"
                }
            ],
            "paddingAll": "md",
            "paddingStart": "md",
            "paddingBottom": "sm"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "沒錯",
                                "data": yes_data,
                            }
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "我要改",
                                "data": no_data,
                            }
                        }
                    ]
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "取消",
                        "data": _get_cancel_act_data()
                    }
                }
            ],
            "flex": 0,
            "paddingAll": "xs"
        }
    }
    return FlexSendMessage(alt_text=title, contents=result)


def get_ask_for_things_flex(thing_type, group_name):
    thing_type2title = {
        'deadline': '截止時間',
        'details': '活動資訊',
    }
    thing_type2alt_text = {
        'deadline': '請輸入截止時間',
        'details': '請輸入活動資訊',
    }
    thing_type2description = {
        'deadline': '好的 請輸入統計截止時間\n'
                    '格式為"2021.01.01 19:00"\n',
        'details': '請輸入活動資訊\n'
                   '字數上限為150個字',
    }

    result = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": thing_type2title[thing_type],
                    "style": "normal",
                    "weight": "bold",
                    "align": "center",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": f"你即將在[{group_name}]中創建活動",
                    "size": "sm",
                    "align": "center",
                    "color": "#AAAAAA"
                }
            ],
            "margin": "none",
            "spacing": "none",
            "paddingAll": "none",
            "paddingTop": "lg"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": thing_type2description[thing_type],
                    "wrap": True,
                    "align": "start"
                },
                {
                    "type": "text",
                    "text": "或點擊[取消]已取消活動",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "align": "start"
                }
            ],
            "paddingAll": "sm",
            "paddingStart": "md"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "取消",
                        "data": _get_cancel_act_data()
                    }
                }
            ],
            "flex": 0,
            "paddingAll": "xs"
        }
    }
    return FlexSendMessage(alt_text=f'在[{group_name}]中創建活動\n' +
                                    thing_type2alt_text[thing_type],
                           contents=result)


def get_ask_for_invitation_method_flex(group_name):
    postback_id = str(time.time()).replace('.', '')
    group_data = {
        'type': 'invitation_method',
        'data': {
            'invitation_method': 'group'
        },
        'postback_id': postback_id,
        'timeout_type': 'always'
    }
    private_data = {
        'type': 'invitation_method',
        'data': {
            'invitation_method': 'private'
        },
        'postback_id': postback_id,
        'timeout_type': 'always'
    }
    group_data = json.dumps(group_data, ensure_ascii=False)
    private_data = json.dumps(private_data, ensure_ascii=False)

    result = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "私訊v.s群組",
                    "style": "normal",
                    "weight": "bold",
                    "align": "center",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": f"你即將在[{group_name}]中創建活動",
                    "size": "sm",
                    "align": "center",
                    "color": "#AAAAAA"
                }
            ],
            "margin": "none",
            "spacing": "none",
            "paddingAll": "none",
            "paddingTop": "lg"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "想要透過私訊發送邀請\n還是透過群組發送邀請",
                    "wrap": True,
                    "align": "start"
                },
                {
                    "type": "text",
                    "text": "或點擊[取消]已取消活動",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "align": "start"
                }
            ],
            "paddingAll": "sm",
            "paddingStart": "md"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "私訊",
                                "data": private_data
                            }
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "postback",
                                "label": "群組",
                                "data": group_data
                            }
                        }
                    ]
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "取消",
                        "data": _get_cancel_act_data()
                    }
                }
            ],
            "flex": 0,
            "paddingAll": "xs"
        }
    }
    return FlexSendMessage(alt_text=f'在[{group_name}]中創建活動\n請選擇透過群組或是私訊邀請',
                           contents=result)


def get_which_info_to_change_flex(group_name):
    postback_id = str(time.time()).replace('.', '')
    name_data = {
        'type': 'change_act_info',
        'data': {
            'change_act_info': 'name'
        },
        'postback_id': postback_id,
        'timeout_type': 'always',
    }
    deadline_data = {
        'type': 'change_act_info',
        'data': {
            'change_act_info': 'deadline'
        },
        'postback_id': postback_id,
        'timeout_type': 'always',
    }
    details_data = {
        'type': 'change_act_info',
        'data': {
            'change_act_info': 'details'
        },
        'postback_id': postback_id,
        'timeout_type': 'always',
    }
    invitation_method_data = {
        'type': 'change_act_info',
        'data': {
            'change_act_info': 'invitation_method'
        },
        'postback_id': postback_id,
        'timeout_type': 'always',
    }
    name_data = json.dumps(name_data)
    deadline_data = json.dumps(deadline_data)
    details_data = json.dumps(details_data)
    invitation_method_data = json.dumps(invitation_method_data)
    result = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "修改哪個項目?",
                    "style": "normal",
                    "weight": "bold",
                    "align": "center",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": f"你即將在[{group_name}]中創建活動",
                    "size": "sm",
                    "align": "center",
                    "color": "#AAAAAA"
                }
            ],
            "margin": "none",
            "spacing": "none",
            "paddingAll": "none",
            "paddingTop": "lg"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "wrap": True,
                    "align": "center",
                    "contents": [],
                    "text": "請點選要修改的項目",
                    "size": "lg",
                    "weight": "bold"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "text",
                    "text": "或點擊[取消]以取消活動",
                    "size": "sm",
                    "color": "#AAAAAA",
                    "align": "start"
                }
            ],
            "paddingAll": "md",
            "paddingStart": "md",
            "paddingBottom": "sm"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "活動名稱",
                        "data": name_data
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "截止時間",
                        "data": deadline_data
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "活動資訊",
                        "data": details_data
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "邀請方式",
                        "data": invitation_method_data
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": "取消",
                        "data": _get_cancel_act_data()
                    }
                }
            ],
            "flex": 0,
            "paddingAll": "xs"
        }
    }
    return FlexSendMessage(alt_text='修改哪個項目', contents=result)


def get_which_group_to_launch_activity(group_list):
    postback_id = str(time.time()).replace('.', '')
    footer_content = [{
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
            "type": "postback",
            "label": group_dict['name'],
            "data": json.dumps({
                'type': 'choose_group_to_launch',
                'data': {
                    'group_id': group_dict['group_id']
                },
                'postback_id': postback_id,
                'timeout_type': 'always',
            })
        }
    } for group_dict in group_list]
    result = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "要在哪個群組創建活動?",
                    "style": "normal",
                    "weight": "bold",
                    "align": "center",
                    "size": "lg"
                }
            ],
            "margin": "none",
            "spacing": "none",
            "paddingAll": "none",
            "paddingTop": "lg"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "wrap": True,
                    "align": "center",
                    "contents": [],
                    "text": "請點選群組",
                    "size": "lg",
                    "weight": "bold"
                }
            ],
            "paddingAll": "md",
            "paddingStart": "md",
            "paddingBottom": "sm"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": footer_content,
            "flex": 0,
            "paddingAll": "xs"
        }
    }
    return FlexSendMessage(alt_text='要在哪個群組創建活動?', contents=result)


def get_lauching_act(act_list):
    postback_id = str(time.time()).replace('.', '')
    footer_content = [{
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
            "type": "postback",
            "label": act_dict['activity']['name'],
            "data": json.dumps({
                'type': 'show_act',
                'data': {'act_id': act_dict['act_id']},
                'postback_id': postback_id,
                'timeout_type': 'always',
            })
        }
    } for act_dict in act_list]
    result = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "發起活動",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": footer_content,
            "flex": 0
        }
    }
    return FlexSendMessage(alt_text='目前發起的活動，想要查看哪個活動?', contents=result)


def get_act_bubble(act_id, name, details, deadline, creator):
    postback_id = str(time.time()).replace('.', '')
    result = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": name,
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": details,
                            "wrap": True
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "截止時間"
                                },
                                {
                                    "type": "text",
                                    "text": deadline,
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "發起人"
                                },
                                {
                                    "type": "text",
                                    "text": creator,
                                    "align": "end"
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "postback",
                        "label": '查看參加情形',
                        "data": json.dumps({
                            'type': 'show_act_attending',
                            'data': {'act_id': act_id},
                            'postback_id': postback_id,
                            'timeout_type': 'always',
                        })
                    }
                }
            ],
            "flex": 0
        }
    }
    return result


def compose_bubble_to_carousel(bubble_list, alt_text='carousel'):
    result = {
      "type": "carousel",
      "contents": bubble_list
    }
    return FlexSendMessage(alt_text=alt_text, contents=result)


def get_ban_user_bubble(ban_user_list):
    postback_id = str(time.time()).replace('.', '')
    footer_content = [
        {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "postback",
                "label": x['user_name'],
                "data": json.dumps({
                    'type': 'cancel_ban_user',
                    'data': {'user_id': x['user_id']},
                    'postback_id': postback_id + str(i),  # 讓他們可以一次解除封鎖很多人
                    'timeout_type': 'always',
                })
            }
        } for i, x in enumerate(ban_user_list)
    ]
    result = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "被封鎖的人",
                    "style": "normal",
                    "weight": "bold",
                    "align": "center",
                    "size": "lg"
                }
            ],
            "margin": "none",
            "spacing": "none",
            "paddingAll": "none",
            "paddingTop": "lg"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "wrap": True,
                    "align": "center",
                    "contents": [],
                    "text": "點擊已取消封鎖",
                    "size": "lg",
                    "weight": "bold"
                }
            ],
            "paddingAll": "md",
            "paddingStart": "md",
            "paddingBottom": "sm"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": footer_content,
            "flex": 0,
            "paddingAll": "xs"
        }
    }
    return result


def get_ban_group_bubble(ban_group_list):
    postback_id = str(time.time()).replace('.', '')
    footer_content = [
        {
            "type": "button",
            "style": "link",
            "height": "sm",
            "action": {
                "type": "postback",
                "label": x['group_name'],
                "data": json.dumps({
                    'type': 'cancel_ban_group',
                    'data': {'group_id': x['group_id']},
                    'postback_id': postback_id + str(i),  # 讓他們可以一次解除封鎖很多人
                    'timeout_type': 'always',
                })
            }
        } for i, x in enumerate(ban_group_list)
    ]
    result = {
        "type": "bubble",
        "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "被封鎖的人",
                    "style": "normal",
                    "weight": "bold",
                    "align": "center",
                    "size": "lg"
                }
            ],
            "margin": "none",
            "spacing": "none",
            "paddingAll": "none",
            "paddingTop": "lg"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "wrap": True,
                    "align": "center",
                    "contents": [],
                    "text": "點擊已取消封鎖",
                    "size": "lg",
                    "weight": "bold"
                }
            ],
            "paddingAll": "md",
            "paddingStart": "md",
            "paddingBottom": "sm"
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": footer_content,
            "flex": 0,
            "paddingAll": "xs"
        }
    }
    return result


def get_manual():
    return FlexSendMessage(alt_text='指令說明', contents={
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "創建活動",
                            "size": "lg"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "1. 先加我為好友",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": "在群組中說「加加可以嗎」以創建活動",
                            "contents": [
                                {
                                    "type": "span",
                                    "text": "2. 在群組中說 ",
                                    "size": "md"
                                },
                                {
                                    "type": "span",
                                    "text": "加加可以嗎",
                                    "weight": "bold"
                                }
                            ],
                            "margin": "none"
                        },
                        {
                            "type": "text",
                            "text": "2. 私訊我說 ",
                            "contents": [
                                {
                                    "type": "span",
                                    "text": "2. 或私訊我說 "
                                },
                                {
                                    "type": "span",
                                    "text": "創建活動",
                                    "weight": "bold"
                                }
                            ]
                        }
                    ]
                }
            },
            {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "查看資訊",
                            "size": "lg"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "在群組中說「加加可以嗎」以創建活動",
                            "contents": [
                                {
                                    "type": "span",
                                    "text": "1. 查看自己的活動 ",
                                    "size": "md"
                                },
                                {
                                    "type": "span",
                                    "text": "查看發布",
                                    "weight": "bold"
                                }
                            ],
                            "margin": "none"
                        },
                        {
                            "type": "text",
                            "text": "2. 私訊我說 ",
                            "contents": [
                                {
                                    "type": "span",
                                    "text": "2. 查看封鎖 "
                                },
                                {
                                    "type": "span",
                                    "text": "查看封鎖",
                                    "weight": "bold"
                                }
                            ]
                        },
                        {
                            "type": "text",
                            "text": "在群組中說「加加可以嗎」以創建活動",
                            "contents": [
                                {
                                    "type": "span",
                                    "text": "3. 查看現在活動 ",
                                    "size": "md"
                                },
                                {
                                    "type": "span",
                                    "text": "查看活動",
                                    "weight": "bold"
                                }
                            ],
                            "margin": "none"
                        }
                    ]
                }
            },
            {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "其他指令",
                            "size": "lg"
                        }
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "在群組中說「加加可以嗎」以創建活動",
                            "contents": [
                                {
                                    "type": "span",
                                    "text": "把我踢出群組 ",
                                    "size": "md"
                                },
                                {
                                    "type": "span",
                                    "text": "加加你滾",
                                    "weight": "bold"
                                }
                            ],
                            "margin": "none"
                        }
                    ]
                }
            }
        ]
    })


"""
{
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "創建活動",
            "size": "lg"
          }
        ]
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "先加我為好友 ",
            "wrap": true
          },
          {
            "type": "text",
            "text": "在群組中說「加加可以嗎」以創建活動",
            "contents": [
              {
                "type": "span",
                "text": "在群組中說 ",
                "size": "md"
              },
              {
                "type": "span",
                "text": "加加可以嗎",
                "weight": "bold"
              },
              {
                "type": "span",
                "text": " 以創建活動"
              }
            ],
            "margin": "none"
          }
        ]
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": []
      }
    }
  ]
}
"""