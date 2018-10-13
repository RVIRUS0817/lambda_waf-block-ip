import boto3
import json
import os
import requests
import re
from dns import reversename,resolver
from geoip import geolite2

def reverse_dns(ip):
    result_ip = re.sub('\/.*',"",ip)
    result_addr = reversename.from_address(result_ip)
    resolver.timeout = 30
    resolver.lifetime = 30
    result_record = resolver.query(result_addr, "PTR")[0]
    return result_record

def notification_slack(ip):
    url = os.environ.get('SLACK_WEBHOOK_URL')
    title = ':warning:  本番ALBでDoS攻撃を検知しました！！！:warning: '
    text = "遮断したアクセス元 ```%s\n``` " % (ip)
    color = 'danger'

    payload = {
        'channel': 'bot_alerts',
        'username': 'lancers-waf',
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
        notification_slack(ip)

