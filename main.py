#!/usr/bin/python3
#basic imports
import pygame #load pygame

import argparse #needed to work with command line arguments
import framework.assetManager
import framework.buttonAPI
import framework.layers
import framework.eventSystem
#load our framework
#import assetManager
#import buttonAPI
#...

#this will get a list of all our minions+minigames
from minigames.minigames import getGames
gameList,minionList = getGames()
print(gameList)
print("\n")
print(minionList)
#read the command line arguments
#Set a nice description for the help
parser = argparse.ArgumentParser(description='Starts the mini dungeon')
#Adds the --minigame argument.
#This can be used to start another minigame instead of the dungeon
parser.add_argument(
    '-m','--minigame',                       #flag names
    type     = str,                          #type of the value
    help     = 'Sets the starting minigame', #Help message of the argument
    required = False,                        #Makes it optional
    default  = 'Dungeon'                     #Sets the default value
)
#Adds the --level argument.
#This can be used to set the starting level of the dungeon
parser.add_argument(
    '-l','--level',
    type     = int,
    default  = 1,
    required = False,
    help     = 'Sets the starting level'
)
#These 2 may be removed in the future once we decided on an FPS and screen size.
parser.add_argument(
    '-s','--size',
    type     = int,
    default  = [800,600],
    nargs    = 2,    #The amount of values it expects
    required = False,
    help     = 'Sets the resolution of the game. First width, then height'
)
parser.add_argument(
    '-f','--frames',
    type     = int,
    default  = 30,
    required = False,
    help     = 'Sets the amount of frames that gets displayed every second.'
)
args = parser.parse_args()
#Now, its time to setup our environment
pygame.init()
pygame.display.set_mode(args.size)
screen = pygame.display.get_surface()
clock  = pygame.time.Clock()

#init the minigame
if not args.minigame in gameList:
    print(args.minigame + " is not a valid minigame :(.")
    pygame.quit()
    quit()
layers   = framework.layers.Layer(screen,pygame)
buttons  = framework.buttonAPI.ButtonAPI(pygame)
eventAPI = framework.eventSystem.Event(pygame)

minigame = gameList[args.minigame]({
    "gameList"   : gameList,
    "minionList" : minionList,
    "pygame"     : pygame,
    "asset"  : framework.assetManager.AssetManager(args.minigame,pygame),
    "button" : buttons,
    "layer"  : layers,
    "event"  : eventAPI, 

    #rest of the framework
})

stopped = False
while not stopped:
    lastFrame = clock.tick(args.frames) #get the time since last frame and set the FPS correctly
    #call update here.
    stopped = bool(minigame.update(lastFrame))
    #draw all the elements to the screen
    buttons.updateClicked(lastFrame)
    stopped=eventAPI.keyCheck(lastFrame)
    layers.draw()
    pygame.display.update()
    #pygame.display.flip() #create the frame
#clean exit
pygame.quit()
quit()

