import json

dic = {'other_link' : ['立即注册(GDPR)',   
                        '退订',
                        '订阅',
                        '访问官网',
                        '法律披露',
                        '版权',
                        '隐私',
                        '点击加入',
                        '在线联系SAP',
                        'SAP官网',
                        '商标',
                        '取消订阅',
                        'SAP 天天事',
                        'GDPR_F立即选择',
                        'UnSubscribe1',
                        '访问SAP.com',
                        'Unsubscribe link',   
                        'Unsubscribe',
                        'UnSubscribe ',
                        'Legal Disclosure',
                        'Facebook',
                        'YouTube',
                        'LinkedIn',
                        'Privacy',
                        'Slideshare',
                        'SAP',
                        'Subscribe',
                        'Twitter',
                        'local country numbers',
                        'Contact Us',
                        'Copyright',
                        'Visit SAP.com',
                        '隱私權',
                        '專員線上洽談',
                        '訂閱',
                        '取消訂閱',
                        '按此',
                        '立即訂閱 ►',
                        '法定揭露事項',
                        '版權',
                        '造訪'],
        'local_path':{'tracker_path' : r'C:\Users\C5293427\Desktop\MA\Request_Tracker.xlsx',
            'simple_tracker_path' : r'C:\Users\C5293427\Desktop\MA\Simple_Tracker_V3.xlsx',
            'report_template' : r'C:\Users\C5293427\Desktop\MA\report\Report_template.xlsx',
            'report_save' : r'C:/Users/C5293427/Desktop/MA/report/'}
    }
print(dic['local_path'])

with open("config.json", "w", encoding='utf-8') as f:
    # indent 超级好用，格式化保存字典，默认为None，小于0为零个空格
    #f.write(json.dumps(dic))
    json.dump(dic,f, indent=4)  # 传入文件描述符，和dumps一样的结果