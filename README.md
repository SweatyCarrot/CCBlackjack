# CCBlackjack
Designed to fulfill CodeCademy's Portfolio Project: Python Terminal Game 

### Intro
This feels like my first _real_ project in coding. While I have done a Rock Paper Scissors clone in the past, this is certainly a step above that. It draws on everything I have learned so far and has required me to look to outside resources to learn new things to tackle various problems. It is not perfect, and I'm sure there are many bugs/oddities I have not found in testing. However, I am proud of what I have accomplished with this project and consider it "done" enough to publish. There's a lot of the more niche Blackjack features missing like insurance, splitting, and doubling down, but the core gameplay is there. With a few more lines of code, you could even make the game support multiple human players (not bug tested, venture with caution)! I tried to code everything with scalability in mind. While that made things take more time, I am overall happier with the end result because of it.

### About the Code
The goal of this project was to build a terminal based game in Python utilizing the Object Oriented Programming paradigm. This was my first stab at making a full project utilizing OOP, and I tried to follow the project's guidelines as closely as possible. Because of that, you will likely find some things unnecessarily OOPy. 

The code structure itself is pretty straight forward. Outside of Main(), everything is encapsulated into a class. GameState() is a general helper class that facilitates global gameplay. Player() and Dealer() are exactly how they sound and inherit from Person(). Person() was an attempt to condense common methods/attributes into one parent class. It was my first attempt at inheritance, and I think I did a decent job with it. Though small, the Player_Actions() enum simplifies input validation and provides the ground work for future enhancements.

The gameplay loop is as follows:

Initialize game environment
    Get the player's name
    Get the player's wallet amount
Until the player's wallet is empty
    Take bet
    Deal cards
    Unless the player has a Blackjack, they hit until they bust or choose to stay
    Dealer attempts to beat the player
    Winner is determined and round is paid out

There is no win condition. This is because ~~gambling is a one sided endeavor and the house always wins~~ I was too lazy to add one.

There is nothing hard-coded for only one player. With the addition of a loop at line 275, the game would theoretically support multiple players. However, I did not try this as I knew it would open a whole new can of worms to troubleshoot, refactor, and attempt to perfect.

### Challenges and Lessons Learned
Below are some of the most notable challenges I faced, how I resolved them, and what I learned as a result!

__Scope Creep:__ A few weeks before starting this project, I had tried to create somewhat of a text based rogue-like game. This quickly flopped due to me not having a clue how I was going to structure classes, how objects would interact with each other, and what all would be included in the game. To avoid falling into the same trap with Blackjack, I spent time researching the best way to structure code using OOP. I learned about getters and setters and general tips for mapping things out before writing a single line. I started with good ol' pen and paper, then digitized things in Notion for easy reference. While no outline will ever be all-encompassing, having concrete boundaries made it a lot easier for me to focus on what needed to be done and not waste time going down rabit holes.

__Try/Except:__ One of the concepts I knew I wanted to employ in this project was try/except. My initial goal was to use this to handle user input. I had heard it can make user input handling easier, and I was desparate for a way to get away from countless if/else statements. My initial implementations of this were sloppy (see main prior to commit 6e96d3e). I had nearly bare excepts, and it was an overall poor implementation. I moved back to using if/else, and I learned to handle input more cleanly as a result. Try/except is still used in the final result, just not to handle user input. It is used in GameState.return_bets() to creatively get around some issues with the dealer winning. I learned a good deal about try/except, and I think I can employ it better in the future!

__List Comprehension:__ This is a simple one, but I got much better at using list comprehension as a result of this project! I didn't really understand them when CodeCademy introduced the concept, so I tried to stay away from them. However, I forced myself to learn how to use them in this project, and I am in love with them as a result! Of course they aren't always the best option, but there's so many places where it is easier and more convenient to create a new list in one line! winner_names in GameState.calculate_winner() is a good example of this.

__Score Calculation:__ While this doesn't seem too difficult at first, this was easily the biggest challenge I came up against. Simply totalling up the numeric value of a hand is easy, but then comes the dreaded ace. My first iteration of Person.get_hand_value() converted Aces into 11's, then added each number in the hand one by one, switching 11's to 1's if the player was going to go over by adding an 11. This algorithim was very flawed as it did not allow for going _back_ and switching 11's to 1's if needed, so players would commonly bust with completely valid hands. A friend of mine pointed out this could be resolved by hacing Aces be calculated last. I created a new method to sort the hand so Aces would be last, then fed that into my original one-by-one adding algorithim.

I thought this would be the end of my struggles, and so I moved on. But, a few days later I got to thinking and found a major flaw. What if a player's hand was [10, A, A]? This is a valid hand with a value of 12, but my algorithim would end up calculating it as being 22 and cause the player to bust. At this point, I used Google like any good developer does. I found several examples, and I settled on the simplest I could find. This one uses sum() and then replaces 11's with 1's as applicable.

__Gameplay Speed:__ Since each hand takes several lines to play out, having everything spat out into the terminal immediately made gameplay feel quite jarring. I would constantly have to scroll or expand the terminal to get a feel for how a round played out, and that was annoying both from a development standpoint and a player standpoint. I hadn't had this problem before since everything I had coded prior was much simpler. I knew adding small waits between gameplay actions would help things feel more natural, and I was able to find that capability in Python's time.sleep() function. After a few minutes of tweaking wait times, I was able to get gameplay feeling more relaxed and fun. It's not perfect, and I am sure there are some odd and inconsistent feeling sections, but it gets the job done so I am happy with it.

### Conclusion

There are a few people I'd like to thank for helping me along this journey: My friend Carl for helping me work through the score calculation algorithm, my partner for being a rubber duck when needed, and my friend Brandon for making a pull request to help me see things I could be doing differently/better. I would not have ended up with the result I did without their help.

From here, I am looking forward to continuing on in my learning and seeing what I do next!
