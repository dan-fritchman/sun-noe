
# B-Ball Roll Call

The one-click reply "app" for our Sunday b-ball game.

---
## Two Goals:

1. One click to reply
2. Do so via text

This does not exist in any existing service I can find.
So we made this little bootleg one.

---
## How to Use This

If you made your way here, you are probably part of the game.
Your name is then also in the super-secret Google Sheet which serves as our "player database".

You will receive receive 3 links from a weird number (12674777207)
They will look like this:

![](txt.jpg)

Those links are *personalized* for you, with an ID read from the Sheet, for example:

* http://sun-noe.herokuapp.com/**SOME_NICKNAME**/in

The nicknames are initially made by me - but can be edited just as easily in the Sheet, under the "ID" column:




---
## Why Make This Anyway

Something like:

* 50% because it's better than pestering you by email.  (You never check your effing email.)
* 50% because I realized I knew how to make 85% of it, and figured figuring out the other 15% would be interesting enough.
* 10% because it ain't all that hard.  (See below.)

---
## How TF Does This Work

There's about a hundred lines of python code running this.
A handful of services make this pretty easy:

* The "site" uses [Flask](http://flask.pocoo.org/).
* [Heroku]() makes running it really easy, and free.
* [gspread](https://github.com/burnash/gspread) makes reading and writing the Google Sheet easy
* [Twilio]() sends the SMS messages, for a small fee.
* Twilio also
  * [Shout-out ](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)

---
## Copyright

TODO: link to the "do what the fuck you want" license.
