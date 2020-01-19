# How to serverless

One of the goals of this project is to actually value add to my life, through the pomodoro timer and scheduler. However, running it locally meant that I had to python main.py each time I wanted to use the bot. It wasn't very effective.

As such, I decided to find a way to have the bot keep running. The following steps are inspired by: https://hackernoon.com/serverless-telegram-bot-on-aws-lambda-851204d4236c

---

## Summary




---

#### 1. Installing node

Firstly, we need to have node.js installed. I used this [link](https://www.webucator.com/how-to/how-install-nodejs-on-mac.cfm) which was quite straightforward.

#### 2. Installing serverless

Once we have node installed, we need to install serverless. I believe it is somewhat similar to pip install concept. Use the following command.

```
$ npm install -g serverless
```
This installs serverless.

```
$ serverless create --template aws-python3 --path my-telegram-bot
```
This creates a template file, containing handler.py and serverless.yml. We will be editing them later.

#### 3. Obtaining AWS Credentials

- Go to AWS Console
- Username > My security Credentials
- Users > Add User
- python-telebot-test for Username
- Only Programmatic Access
- "Attach existing policies directly" > Adminstrator Access
- Copy Access key ID and Secret Key into telegram saved messages or notepad

Above, we have essentially created a user account inside our console - this will allow us to run our bot through this account.

Run the following commands, making sure that your working directory is inside my-telegram-bot

```
$ export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
$ export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCEXAMPLEKEY
```
Please take note that we do not use "" or ''


#### 4. Editing handler.py to creating telegram bot

Copy and paste the following code into handler.py

```
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./vendored"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)


def hello(event, context):
    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"]["first_name"]

        response = "Please /start, {}".format(first_name)

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)

    except Exception as e:
        print(e)

    return {"statusCode": 200}
```

Copy and paste the following into serverless.yml

```
service: serverless-telegram-bot

provider:
  name: aws
  runtime: python3.6
  stage: dev
  region: us-east-1
  environment:
    TELEGRAM_TOKEN: ${env:TELEGRAM_TOKEN}



functions:
  post:
    handler: handler.hello
    events:
      - http:
          path: my-custom-url
          method: post
          cors: true
```

Here, we have created a telegram bot to reply /start. The serverless.yml file is a config file for logging into AWS when you deploy the bot.

#### 5. Creating requirements.txt file

Create a requirements.txt file - this is needed when deploying the bot on serverless.

```
$ vim requirements.txt
```

Edit the txt file to include
```
requests
```

Now, we install the requirements file.

```
$ pip install -r requirements.txt -t vendored
```

If you get an error, consider

```
$ python -m pip install -r requirements.txt -t vendored
```

#### 6. Obtaining telegram token

We need an api key for our telegram bot. Go to [this guy](https://telegram.me/BotFather) and request for an api key

#### 7. Obtaining telegram url + file deployment

```
$ serverless deploy
```

Run the following command, which will push your working directory to aws as a zip file.

You should get
```
endpoints:
  POST - https://m2kb1rrh43.execute-api.us-east-1.amazonaws.com/dev/my-custom-url
```
Make sure to copy the url.

#### 8. Connecting backend to telegram

3 things left now.

Insert telegram api key and url into this command.

```
$ curl --request POST --url https://api.telegram.org/bot459903168:APHruyw7ZFj5qOJmJGeYEmfFJxil-z5uLS8/setWebhook --header 'content-type: application/json' --data '{"url": "https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/my-custom-url"}'
```

eg. Given
telegram api: aaa
telegram url: https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/my-custom-url

Run the following command

```
$ curl --request POST --url https://api.telegram.org/botaaa/setWebhook --header 'content-type: application/json' --data '{"url": "https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/my-custom-url"}'
```

You should receive the following

```
{
  "ok": true,
  "result": true,
  "description": "Webhook was set"
}
```

#### 9. Deploying bot

Run the final command

```
$ serverless deploy
```

## And we're done! Try sending /start to your bot :)
