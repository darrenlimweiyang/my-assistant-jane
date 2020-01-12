# my-assistant-jane
---

## Objective 
I aim to brush up on my python skills while making my life easier. With that in mind, I decided to try and come up with a personal assistant on telegram. (Especially since I have spent so much time on telegram) With that in mind, I aim to create a telegram bot that will accompany me while studying, hitting the gym(?) and other functions not yet thought off.

Acknowledgements: https://github.com/python-telegram-bot/python-telegram-bot
PS. The telegram group is great as well!

## Function outline

- [x] echo 

- [x] pomodoro timer

- [x] schedule text

- [ ] to-do list

---
## File Description

- jane.py is the bot
- test_func.py contains a list of basic functions created, while starting out
- quickstart.py contains a snipper used to obtain credentials to access googlecalendar api
---

#### echo
- echos every single message

#### pomodoro
- texts at every 25/5 minutes chunks, for 25minute study chunks and breaks
- The pomodoro timer has been done for now - making use of time.sleep() for now
- further customizations would be to allow for input of study & break time

#### schedule text
- when called, the bot will send a message containing today's schedule

#### to-do list
- possibly connect with [todoist](https://developer.todoist.com/sync/v8/)
- separate todo list inside the bot, will require a way of storing information

---


# What's next

- [ ] being able to run the bot on cloud

- [ ] creating a to-do list function

- [ ] implementing customised study_chunk: ability to set study & break duration

- [ ] implementing customised today_schedule: ability to set how many events to pull


cheers! feel free to [contact](darrenlimweiyang@gmail.com) me

