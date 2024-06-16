# Top Traded Stocks - implementation notes

## Overview

On the highest level, the solution works the following way:
1. Maintain a mapping from OrderID to symbol (by recording AddOrder events)
2. Record traded shares quantity by symbol for all trades (from OrderExecuted and Trade messages, using symbol from the mapping for the former)
3. Aggregate the records and retrieve top stocks by volume 

For the solution to be scalable, I implemented this steps in SQL database, using Python's built-in SQLite driver.

## Running

The solution script is in `top_traded_stocks.py` file. It can read from STDIN or from a file with `-i` option and automatically decompress gzip archives with `-g` flag.

The number of top stocks to show can be also adjusted with the `-n` option. To explore the created SQLite database, you can output it to a file with `-f`.

Example run command:
```shell
python3 top_traded_stocks.py -i pitch_example_data.gz -n 10 -g
```

It's equivalent to
```shell
gzip -cd pitch_example_data.gz | python3 top_traded_stocks.py -n 10
```

## PITCH parsing

For parsing **PITCH** messages, I've created a little framework, contained in `pitch` Python package. The core of its API is `parse_message` function that consumes a Python synchronous byte-reader interface (which is implemented by `open()` in read-binary mode). The function optionally takes start and end sentinels for a message, allowing me to skip **S** characters and newlines.

**PITCH** data types and message definitions are present in `pitch.basic_types` and `pitch.data_model`. I implemented only 4 message types but this can be easily extended. For simplicity, all datatypes are based on alphanumeric strings. Letter case is ignored.

The folder `tests` contains a couple of unit tests for `pitch` library using **pytest**. To run them, install `pytest` and run it as a CLI in the root folder.

Many things that are very important for production code, like logging and functional tests, are not included due to limited time. Other production code concerns are concurrent access, asynchrony and error handling, but they require much more specific requirements.

## Error handling

I tried to avoid raising exceptions and return `None` in nasty cases, but this error handling is far from perfect.


# Original task wording

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
