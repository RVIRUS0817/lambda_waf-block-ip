# Waf_block_ip

<img width="798" alt="2018-10-02 18 33 31" src="https://user-images.githubusercontent.com/5633085/46341322-d2341480-c672-11e8-9642-7f9c1a173680.png">

https://blog.adachin.me/archives/8936  
It is a program that uses Slack to notify the attacked IP using the AWS WAF Rate-based rule.

## Use AWS

・Lambda   
・IAM  
・SNS  
・CloudWatch   
・Python 3.6.2  

## How to use

1.build  

```
$ cd waf_block-ip
$ pip install -r requirements.txt -t .
```

2. zip directory

```
$ zip -r ../upload.zip ./*
```

3.upload Lambda


<img width="668" alt="_2018-10-02_18_32_37" src="https://user-images.githubusercontent.com/5633085/46341356-de1fd680-c672-11e8-8ee7-d7c3dcaac84e.png">
