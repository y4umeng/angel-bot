# angel-bot

Twitter bot (https://twitter.com/angel01bot) that web scrapes all the public posts of a blog on Substack (angelicism01 in this case), parses a random string, then tweets it using AWS Lambda.

Requirments to run:
  
  - Packages installed
  
  - Twitter dev account set up + keys are valid
  
  - "headers" is specified to your own system (I removed my own information)
  
  - "cookies" may also need to be initialized to work with AWS lambda
  
Program could run for theoretically any substack blog.

TODO:
  - fix bugs with the string parsing
  - allow the bot to tweet images as well
  
Similar project:

https://medium.com/@mahibhosain98/creating-a-lyrics-bot-on-twitter-with-python3-and-aws-lambda-1e22743dc3b7

  
