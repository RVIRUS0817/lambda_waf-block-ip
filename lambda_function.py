import boto3
import json
import os
import requests
import re
from dns import reversename,resolver

def reverse_dns(ip):
    result_ip = re.sub('\/.*',"",ip)
    result_addr = reversename.from_address(result_ip)
    result_record = resolver.query(result_addr, "PTR")[0]
    return result_record

def notification_slack(ip, result_record):
    url = os.environ.get('SLACK_WEBHOOK_URL')
    title = ':warning:  本番ALBでDoS攻撃を検知しました！！！:warning: '
    text = "遮断したアクセス元 ```%s\n%s``` " % (ip, result_record)
    color = 'danger'
     payload = {
        'channel': 'bot_alerts',
        'username': 'waf',
        'attachments': [
            {
                'fallback': title + ' - ' + text,
                'color': color,
                'title': title,
                'text': text
            }
        ]
    }
    headers = {'content-type': 'application/json'}
    requests.post(url, data=json.dumps(payload), headers=headers)

def lambda_handler(event, context):
    ruleid = os.environ.get('RULEID')
    client = boto3.client('waf-regional')
    response = client.get_rate_based_rule_managed_keys(
    RuleId=ruleid
    )
    dict_ip = response.get("ManagedKeys")
    for ip in dict_ip:
        print(ip)
        result_record = reverse_dns(ip)
        notification_slack(ip, result_record)

