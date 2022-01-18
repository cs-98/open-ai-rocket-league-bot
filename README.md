# Hack Technology / Project Attempted 

  

## What technology you wanted to explore 

  

I wanted to explore the python API RLGym which is an api that makes it easier to interact with the Rocket League game environment and code an ai using reinforcement learning. It is an api that connects with the game and attempts to control the speed of the physics engine in-game to make reinforcement learning faster and creating an ai a bit more of a feasible task.  

  

## What you thought you might need the technology for 

The solution I wanted to go forward with was a combination of the solutions I discussed with the person I interviewed. Essentially I wanted to create a better Rocket League AI then what is availible in-game and ones that you can download externally. Then I wanted to try to figure out a way to insert this AI into Rocket League's Training Mode and/or Free Mode to add to the player experience within these game modes. To accomplish this, I first needed to find a way to make a better AI and the idea was to attempt an AI that uses reinforncement learning. This technology would stream line this process and make everything significantly easier. My current plan would be to create a basic reforcement learning agent using the api’s built-in commands and then from there create my own custom reward function or import functions from other libraries. 

## Whether you think the technology would be a good fit for that based on the thing you hacked 

I think the technology would be ideal for what I want to do. The program allows for various customizations that make it easy to create my own custom verison of a Rocket League reforcement learning ai. The program appeared to work or at the very least affect the state of the game.

## What the thing you hacked is supposed to do 

To run the program you need a Windows 10 PC, to download Rocket League on steam/epic games store, download Bakkesmod from bakkesmod.com, and must be running python 3.7 or later. Then pip install rlgym.

If you launch Bakkesmod and then run the program “rlgym_program.py” on the command, it should start up Rocket League and enter a match on it’s own. From there, the player should play on their and slowly learn to hit the ball and put the ball in the opponents net. From what I can see, it looks like it is slowly starting to learn to touch the ball after a few iterations and I am getting some information back each iteration in the console. If I set it to a higher speed, it looks like it is hitting it in the net but I cannot tell. It is hard to see due to the speed. Regardless, it appears to be affecting the state of the game and trying to learn over multiple episodes.

[Screenshot of Commmand Line and Program when ran](program_screenshot.png) 


## Author 

  

Jacob Werzinsky 

  

## Acknowledgments 

  

https://rlgym.github.io/docs-page.html#tutorials 

 
