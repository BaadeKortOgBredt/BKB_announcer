BKB robot of time!
==================

This bot has the responsibility of notifying social media about our activities 3 days in advance.

Features
--------

The bot performs these functions
- Reads a .ical file containing all activities
	- Handles recurrent activities. Yearly, monthly, weekly
- Uses the Discord API
	- *<Future Feature>* Facebook API

Methods
-------

> `reminder(today: datetime.datetime) -> none`

This function takes "Today"'s date as an `datetime.datetime` type. 

> `time_sim(a: datetime.datetime, b: datetime.datetime) -> none`

This function simulates a interval $[a,b]\quad a,b\in \mathbb{R}^3$ without affecting memory. 

> `main() -> none`

We don't talk about main...
