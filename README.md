
# B-Ball Roll Call

The one-click reply "app" for our Sunday b-ball game.

-----------------------------------------------------
## Two Goals:

1. One click to reply
2. Do so via text

This does not exist in any existing service I can find.
So I made this little bootleg one.

Still not really sure how I had to make this for myself.

---
## How to Use This

If you made your way here, you are probably part of the game.
Your name is then also in the super-secret Google Sheet which serves as our "player database".


You will receive receive 3 links from a weird number (12674777207)
They will look like this:

![](txt.jpg)

---
## Why Make This Anyway

Something like:

* 50% because it's better than pestering you by email.  (You never check your effing email.)
* 50% because I realized I knew how to make 85% of it, and figured figuring out the other 15% would be interesting enough.
* 10% because it ain't all that hard.  (See below.)

---
# How TF Does This Work

There's about a hundred lines of python code running this.
A handful of services make this pretty easy:

* The "site" uses [Flask](http://flask.pocoo.org/).
* [Heroku]() makes running it really easy, and free.
* [gspread](https://github.com/burnash/gspread) makes reading and writing the Google Sheet easy
* [Twilio]() sends the SMS messages, for a small fee.
* Twilio also
  * [Shout-out ](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)

---
## Is This Secure?

I think so.
It's not really my area of expertise.
My area of expertise is really limited to eating pizza.

Any links to the underlying spreadsheets are secured in Heroku's secret variables.
Are your cell number and email safe in that spreadsheet?
Or are you going to start getting spam, get your identity stolen, or have some other major problem?

Probably not as safe as if you, say, kept them hidden under your bed.
But yeah, safe.

Either way - don't put your credit card, social security number, or any other high-risk stuff in here.

---
# Copyright

TODO: link to the "do what the fuck you want" license.
