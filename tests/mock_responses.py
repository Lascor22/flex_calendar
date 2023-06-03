class CommandRequest:
    def __init__(self, update_id: str, message_id: str, date: str, text: str):
        self.command = '{"ok":true,"result":[{"update_id":' + update_id + ',\n"message":{"message_id":' + message_id + \
                       ',"from":{"id":0,"is_bot":false,"first_name":"Tester","last_name":"Testeron",' \
                       '"username":"testeron","language_code":"en"},"chat":{"id":0,"first_name":"Tester",' \
                       '"last_name":"Testeron","username":"testeron","type":"private"},"date":' + date + ',"text":"' +\
                       text + '","entities":[{"offset":0,"length":' + str(len(text)) + ',"type":"bot_command"}]}}]}'


class TextMessage:
    def __init__(self, update_id: str, message_id: str, date: str, text: str):
        self.message = '{"ok":true,"result":[{"update_id":' + update_id + ',\n"message":{"message_id":' + message_id + \
                       ',"from":{"id":0,"is_bot":false,"first_name":"Tester","last_name":"Testeron",' \
                       '"username":"testeron","language_code":"en"},"chat":{"id":0,"first_name":"Tester",' \
                       '"last_name":"Testeron","username":"testeron","type":"private"},"date":' + date + ',"text":"' +\
                       text + '"}}]}'


DEFAULT_RESPONSE = '{"ok":true,"result":[]}'
GET_ME_RESPONSE = '{"ok":true,"result":{"id":5642038337,"is_bot":true,"first_name":"Calendar2",' \
                  '"username":"flexCalendar2Bot","can_join_groups":true,"can_read_all_group_messages":false,' \
                  '"supports_inline_queries":false}}'
START_REQUEST = CommandRequest("785553000", "0", "1685770630", "/start").command
HELP_REQUEST = CommandRequest("785553002", "1", "1685770638", "/help").command
NEW_EVENT_REQUEST = CommandRequest("785553003", "2", "1685770700", "/new_event").command
EVENT_NAME_MESSAGE = TextMessage("785553004", "3", "1685770740", "new event").message
VIEW_EVENTS_REQUEST = CommandRequest("785553008", "7", "1685770852", "/view_events").command

YEAR_RESPONSE = '{"ok":true,"result":[{"update_id":785553005,"callback_query":{"id":"1823702158425533129",' \
                '"from":{"id":0,"is_bot":false,"first_name":"Tester","last_name":"Testeron","username":"testeron",' \
                '"language_code":"en"},"message":{"message_id":4,"from":{"id":5642038337,"is_bot":true,' \
                '"first_name":"Calendar2","username":"flexCalendar2Bot"},"chat":{"id":0,"first_name":"Tester",' \
                '"last_name":"Testeron","username":"testeron","type":"private"},"date":1685770740,"text":"Select ' \
                'year","reply_markup":{"inline_keyboard":[[{"text":"2022","callback_data":"cbcal_0_s_y_2022_6_3"},' \
                '{"text":"2023","callback_data":"cbcal_0_s_y_2023_6_3"}],[{"text":"2024",' \
                '"callback_data":"cbcal_0_s_y_2024_6_3"},{"text":"2025","callback_data":"cbcal_0_s_y_2025_6_3"}],' \
                '[{"text":"<<","callback_data":"cbcal_0_g_y_2019_6_3"},{"text":" ","callback_data":"cbcal_0_n"},' \
                '{"text":">>","callback_data":"cbcal_0_g_y_2027_6_3"}]]}},"chat_instance":"-7777803022804384970",' \
                '"data":"cbcal_0_s_y_2023_6_3"}}]}'
MONTH_RESPONSE = '{"ok":true,"result":[{"update_id":785553006,"callback_query":{"id":"1823702159035255430",' \
                 '"from":{"id":0,"is_bot":false,"first_name":"Tester","last_name":"Testeron","username":"testeron",' \
                 '"language_code":"en"},"message":{"message_id":5,"from":{"id":5642038337,"is_bot":true,' \
                 '"first_name":"Calendar2","username":"flexCalendar2Bot"},"chat":{"id":0,"first_name":"Tester",' \
                 '"last_name":"Testeron","username":"testeron","type":"private"},"date":1685770740,' \
                 '"edit_date":1685770802,"text":"Select month","reply_markup":{"inline_keyboard":[[{"text":"Jan",' \
                 '"callback_data":"cbcal_0_s_m_2023_1_3"},{"text":"Feb","callback_data":"cbcal_0_s_m_2023_2_3"},' \
                 '{"text":"Mar","callback_data":"cbcal_0_s_m_2023_3_3"}],[{"text":"Apr",' \
                 '"callback_data":"cbcal_0_s_m_2023_4_3"},{"text":"May","callback_data":"cbcal_0_s_m_2023_5_3"},' \
                 '{"text":"Jun","callback_data":"cbcal_0_s_m_2023_6_3"}],[{"text":"Jul",' \
                 '"callback_data":"cbcal_0_s_m_2023_7_3"},{"text":"Aug","callback_data":"cbcal_0_s_m_2023_8_3"},' \
                 '{"text":"Sep","callback_data":"cbcal_0_s_m_2023_9_3"}],[{"text":"Oct",' \
                 '"callback_data":"cbcal_0_s_m_2023_10_3"},{"text":"Nov","callback_data":"cbcal_0_s_m_2023_11_3"},' \
                 '{"text":"Dec","callback_data":"cbcal_0_s_m_2023_12_3"}],[{"text":"<<",' \
                 '"callback_data":"cbcal_0_g_m_2022_6_3"},{"text":"2023","callback_data":"cbcal_0_g_y_2023_6_3"},' \
                 '{"text":">>","callback_data":"cbcal_0_g_m_2024_6_3"}]]}},"chat_instance":"-7777803022804384970",' \
                 '"data":"cbcal_0_s_m_2023_5_3"}}]}'
DAY_RESPONSE = '{"ok":true,"result":[{"update_id":785553007,"callback_query":{"id":"1823702158156884529",' \
               '"from":{"id":0,"is_bot":false,"first_name":"Tester","last_name":"Testeron","username":"testeron",' \
               '"language_code":"en"},"message":{"message_id":6,"from":{"id":5642038337,"is_bot":true,' \
               '"first_name":"Calendar2","username":"flexCalendar2Bot"},"chat":{"id":0,"first_name":"Tester",' \
               '"last_name":"Testeron","username":"testeron","type":"private"},"date":1685770740,' \
               '"edit_date":1685770805,"text":"Select day","reply_markup":{"inline_keyboard":[[{"text":"M",' \
               '"callback_data":"cbcal_0_n"},{"text":"T","callback_data":"cbcal_0_n"},{"text":"W",' \
               '"callback_data":"cbcal_0_n"},{"text":"T","callback_data":"cbcal_0_n"},{"text":"F",' \
               '"callback_data":"cbcal_0_n"},{"text":"S","callback_data":"cbcal_0_n"},{"text":"S",' \
               '"callback_data":"cbcal_0_n"}],[{"text":"1","callback_data":"cbcal_0_s_d_2023_5_1"},{"text":"2",' \
               '"callback_data":"cbcal_0_s_d_2023_5_2"},{"text":"3","callback_data":"cbcal_0_s_d_2023_5_3"},' \
               '{"text":"4","callback_data":"cbcal_0_s_d_2023_5_4"},{"text":"5",' \
               '"callback_data":"cbcal_0_s_d_2023_5_5"},{"text":"6","callback_data":"cbcal_0_s_d_2023_5_6"},' \
               '{"text":"7","callback_data":"cbcal_0_s_d_2023_5_7"}],[{"text":"8",' \
               '"callback_data":"cbcal_0_s_d_2023_5_8"},{"text":"9","callback_data":"cbcal_0_s_d_2023_5_9"},' \
               '{"text":"10","callback_data":"cbcal_0_s_d_2023_5_10"},{"text":"11",' \
               '"callback_data":"cbcal_0_s_d_2023_5_11"},{"text":"12","callback_data":"cbcal_0_s_d_2023_5_12"},' \
               '{"text":"13","callback_data":"cbcal_0_s_d_2023_5_13"},{"text":"14",' \
               '"callback_data":"cbcal_0_s_d_2023_5_14"}],[{"text":"15","callback_data":"cbcal_0_s_d_2023_5_15"},' \
               '{"text":"16","callback_data":"cbcal_0_s_d_2023_5_16"},{"text":"17",' \
               '"callback_data":"cbcal_0_s_d_2023_5_17"},{"text":"18","callback_data":"cbcal_0_s_d_2023_5_18"},' \
               '{"text":"19","callback_data":"cbcal_0_s_d_2023_5_19"},{"text":"20",' \
               '"callback_data":"cbcal_0_s_d_2023_5_20"},{"text":"21","callback_data":"cbcal_0_s_d_2023_5_21"}],' \
               '[{"text":"22","callback_data":"cbcal_0_s_d_2023_5_22"},{"text":"23",' \
               '"callback_data":"cbcal_0_s_d_2023_5_23"},{"text":"24","callback_data":"cbcal_0_s_d_2023_5_24"},' \
               '{"text":"25","callback_data":"cbcal_0_s_d_2023_5_25"},{"text":"26",' \
               '"callback_data":"cbcal_0_s_d_2023_5_26"},{"text":"27","callback_data":"cbcal_0_s_d_2023_5_27"},' \
               '{"text":"28","callback_data":"cbcal_0_s_d_2023_5_28"}],[{"text":"29",' \
               '"callback_data":"cbcal_0_s_d_2023_5_29"},{"text":"30","callback_data":"cbcal_0_s_d_2023_5_30"},' \
               '{"text":"31","callback_data":"cbcal_0_s_d_2023_5_31"},{"text":" ","callback_data":"cbcal_0_n"},' \
               '{"text":" ","callback_data":"cbcal_0_n"},{"text":" ","callback_data":"cbcal_0_n"},{"text":" ",' \
               '"callback_data":"cbcal_0_n"}],[{"text":"<<","callback_data":"cbcal_0_g_d_2023_4_3"},{"text":"May ' \
               '2023","callback_data":"cbcal_0_g_m_2023_5_3"},{"text":">>",' \
               '"callback_data":"cbcal_0_g_d_2023_6_3"}]]}},"chat_instance":"-7777803022804384970",' \
               '"data":"cbcal_0_s_d_2023_5_31"}}]}'
