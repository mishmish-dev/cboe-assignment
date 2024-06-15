# Solution notes

For the solution, I've created a little framework for parsing PITCH messages, contained in `pitch` Python package. It's used by the `main` module that solves the initial task. Data and message types definitions are present in `pitch/basic_types.py` and `pitch/data_model.py` and can be easily extended. 

The folder `tests` contains a couple of unit tests for `pitch` library, for an example.

In in the solution, I ignored OrderCancel messages for the sake of simplicity. The output of the program is `answer.txt`.


# Task

Hi Mishmish,

Thank you again for speaking with me about a position on our DPE Software Engineering Team.  

As discussed we have all software engineering candidates complete a coding exercise before moving to the next stage in our interview process.  When you return your coding exercise, if you do not hear back from me in a few days, please contact the recruiting team to make sure the email filters did not suppress the email.

Using the PITCH specification, write a program which reads PITCH data from standard input and, at the end of the input, shows a table of the top ten symbols by executed volume. For example, your table should look something like this:

```
SPY   24486275
QQQQ  15996041
XLF   10947444
IWM    9362518
MSFT   8499146
DUG    8220682
C      6756932
F      6679883
EDS    6673983
QID    6526201
```

In short, you'll need to read Add Order messages and remember what orders are open so you can apply Order Cancel and Order Executed messages. Trade Messages are sent for orders which were hidden. You'll need to use both Order Executed and Trade Messages to compute total volume. For simplicity, ignore any Trade Break and long messages (‘B’, ‘r’, ‘d’).

I've included a portion of live PITCH data in a file named pitch_example_data.gz. (Note that each line in the sample file begins with an extra character, 'S', not mentioned in the specification. This character is not part of the message and should be skipped by your program.)

Take as much or as little time solving the problem as you need to. We want to see production quality code, so keep in mind all the things you would need to do and what you'd need to think about before releasing your code to production - what makes your code 'production ready'?  - This is your opportunity to show us what you can do, and that you can write code that meets our expectations.

Finally, we ask that you don’t post your solution on any public source repositories (i.e. GitHub, etc.) – instead, please upload everything to the Proofpoint system.

If you have any questions about the problem or data set, feel free to email me, or the recruiting team.