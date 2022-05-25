from linebot.models import TextSendMessage


sorry_text = TextSendMessage(text='抱歉打擾了')

already_pm = TextSendMessage(text=f'已私訊您')

invitation_sent = TextSendMessage(text=f'已發送邀請')

need_to_follow = TextSendMessage(text=f'請先加我好友\n才能創建活動唷！')

cancel_text = TextSendMessage(text='好的 已為您取消')

name_too_long = TextSendMessage(text='不好意思超過30字唷\n請再輸入一遍')

cannot_read_time = TextSendMessage(text='不好意思，我看不懂這個時間\n'
                                        '請重新輸入\n'
                                        '格式為"2021.01.02 19:00"')

time_passed = TextSendMessage(text='不好意思，您輸入的時間已經過了\n'
                                   '請重新輸入\n'
                                   '格式為"2021.01.02 19:00"')

details_too_long = TextSendMessage(text='不好意思超過150字唷\n請再輸入一遍')

function_not_designed = TextSendMessage(text='不好意思，這個功能還沒被設計出來')

activity_name_text = TextSendMessage(
    text='請輸入活動名稱(少於30字)\n'
         '或輸入"取消":'
)
activity_deadline_text = TextSendMessage(
    text='好的 請輸入統計截止時間\n'
         '格式為"2021.01.02 19:00"\n'
         '請重新輸入'
)
activity_details_text = TextSendMessage(
    text='好的 請輸入活動資訊\n'
         '字數上限為150個字'
)


follow_text = TextSendMessage(
    text='您好，歡迎你使用加加可以嗎\n'
         '能的話最好不要靜音我\n'
         '我能夠通知你群組內的任何活動\n'
         '請用「加加可以嗎」來呼喚我\n\n'
         '如果需要有人幫忙統計參加人數的話\n'
         '就把我加到群組吧！'
)

join_text = TextSendMessage(
    text='大家好\n'
         '我可以幫助大家統計活動人數\n'
         '請用「加加可以嗎」來呼喚我\n'
         '注意：如果要接到通知的話要在群組裡講過話唷'
)

leave_group_text = TextSendMessage(
    text='謝謝大家這段時間的照顧，再會'
)

