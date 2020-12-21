#Jonah Dabu, Parshva Parikh
#2020/10/26
#ICS 4U
#Asterpocalypse - Shoot and maneuver around moving objects (asteroids) with collision objects (lasers) sent from a user
#                 controlled object (spaceship) that is linked to keyboard and mouse events

from tkinter import Tk, Canvas, PhotoImage, messagebox
from Spaceship import Spaceship
from Asteroid import Asteroid
from Laser import Laser         #import necessary modules and classes and objects
import random
import time

root = Tk()     #create the window

# set vars
rock = 0    #asteroid list index
shots = 0      #laser list index
points = 0
lives = 3
health = 10
ship = True     #if the ship is safe or not (decides if user can shoot)


def exit_program():
    global spawnid, asteroids
    for a in range(20):             #cycle through every asteroid object and delete
        asteroids[a].deleteAsteroid()
    root.after_cancel(spawnid)          #cancel the asteroid spawner
    messagebox.showinfo('Asterpocalypse', "Thank you for playing!")
    exit()


def background_timer():     #set the background so it moves
    global btid
    for i in range(len(background_list)):
        canvas.coords(background_list[i], xpos[i] - 5, 0)
        xpos[i] -= 5

    btid = root.after(50, lambda: background_timer())
    root.update()

    if xpos[0] + imgBackground.width() <= 0:
        xpos[0] = xpos[1] + imgBackground.width()
    if xpos[1] + imgBackground.width() <= 0:
        xpos[1] = xpos[0] + imgBackground.width()


def onmousemove(event):         #set the ship object to move with the cursor
    global ship, player
    if ship:                            #if the ship hasn't exploded, move let it move
        player.move(event.x, event.y)
    else:               #if it has exploded don't move it
        pass


def shoot(event):           #fire a laser at each space bar click
    global lasers, shots, player

    if event.char == ' ':      #if the space bar button is clicked, fire
        lasers[shots] = Laser(canvas, player.getRightSide(), player.getTopSide() + player.getHeight() // 2)     #create the laser at the front of the ship
        #######################################laser sound#############################
        lasers[shots].shoot()       #animate the laser forward
        shots += 1
        if shots == 10:         #reset the laser object list index
            shots = 0


def spawnasteroid():            #randomly spawn asteroids
    global asteroids, rock, points, spawnid
    if 0 <= points < 200:
        t, speed = 1400, 2
    elif 200 <= points < 500:
        t, speed = 900, 3               #set the difficulty of the game depending on the player's points
    elif 500 <= points < 700:            #increase the rate of the asteroids spawning and the speed of them
        t, speed = 500, 4
    else:
        t, speed = 400, 5

    spawnid = canvas.after(t, spawnasteroid)        #timer that repeats the spawning
    #create the asteroid object
    asteroids[rock] = Asteroid(canvas, random.randint(0, 2), x=canvas.winfo_reqwidth() + 50, y=random.randint(60, canvas.winfo_reqheight() - 80), speed = speed)
    asteroids[rock].move()      #animate the asteroid
    rock += 1
    if rock == 20:      #reset the index of the asteroid list
        rock = 0


def hit_asteroid():         #laser-asteroid collision detection
    global hitid, points

    for s in range(10):         #cycle through each laser and asteroid
        for a in range(20):
            if lasers[s].getRightSide() >= asteroids[a].getLeftSide()+50 and lasers[s].getLeftSide() <= asteroids[a].getRightSide():
                if lasers[s].getTopSide() <= asteroids[a].getBottomSide() and lasers[s].getBottomSide() >= asteroids[a].getTopSide():

                    if asteroids[a].getImg() == 0:      #if the asteroid hasn't exploded, delete the laser
                        lasers[s].deleteLaser()

                        size = asteroids[a].getSize()       #get asteroids size to decide how many hits it takes to destroy it
                        if size == 0:
                            points += 10                    #+10 points for a small one
                            explode_asteroid(asteroids[a], size)        #explode
                        elif size == 1:
                            if asteroids[a].getHits() == 0:
                                asteroids[a].setHits(1)             #if the asteroid has been hit once, wait for second hit
                            elif asteroids[a].getHits() == 1:
                                points += 20                    #+20 points for medium one
                                explode_asteroid(asteroids[a], size)        #explode
                        else:
                            if asteroids[a].getHits() == 0:
                                asteroids[a].setHits(1)         #if the asteroid has been hit once, wait for second hit
                            elif asteroids[a].getHits() == 1:
                                asteroids[a].setHits(2)         #if the asteroid has been hit twice, wait for third hit
                            elif asteroids[a].getHits() == 2:
                                points += 30                        #+30 points for large one
                                explode_asteroid(asteroids[a], size)        #explode

                        canvas.itemconfig(showPoints, text=str(points))     #update points
                        #print('WORKED' + ' ' + str(a) + ' ' + str(s) + ' ' + str(time.time()))     #error handling and performance
                    else:
                        pass        #if the asteroid has exploded, the laser is not effected

                    root.after_cancel(hitid)        #timer handling
            else:
                pass
    hitid = root.after(1, hit_asteroid)         #timer to constantly check for collision


def explode_asteroid(asteroid, size):   #explode the asteroid
    asteroid.setImage()             #change the image to an explosion
    ##################################################################asteroid destroy#################
    canvas.after(500, lambda: delete_asteroid(asteroid))        #delete the exploded object after some time


def delete_asteroid(asteroid):
    asteroid.deleteAsteroid()       #delete the asteroid


def hit_ship():             #ship-asteroid collision detection
    global hitsid, player

    for a in range(20):     #cycle through every asteroid
        if player.getRightSide() >= asteroids[a].getLeftSide() + 15 and player.getLeftSide() <= asteroids[a].getRightSide()-15:
            if player.getTopSide() <= asteroids[a].getBottomSide()-15 and player.getBottomSide() >= asteroids[a].getTopSide()+15:

                if asteroids[a].getImg() == 0:      #if the asteroid hasn't exploded
                    if player.getImg() == 0:            #if the ship has exploded, it doesn't collide with anything
                        pass
                    else:                       #if ship hasn't exploded, collide and change player lives
                        #print('SHIP HIT')
                        explode_ship()
                        configureHealth(0)
                else:
                    pass

                root.after_cancel(hitsid)       #timer handling

    hitsid = root.after(1, hit_ship)        #constantly check for collision


def explode_ship(): #change ship image to explosion and delete the object
    global ship
    player.setImage()   #change img
    ##################################################destroy player#############################
    ship = False        #ship doesn't exist, can't shoot at space bar click
    canvas.after(1500, lambda: player.deleteShip())     #remove the img after a couple of seconds


def delete_ship(player):        #delete the ship
    player.deleteShip()


def lose_health():          #check if asteroids get past the ship and remove health bars
    global asteroids, lhid
    for a in range(20):             #check each asteroid
        if asteroids[a].getRightSide() <= 0:        #if it goes past the left side of the screen, delete it
            asteroids[a].deleteAsteroid()           #and remove a health bar
            configureHealth(1)
        else:
            pass

    lhid = root.after(250, lose_health)     #constantly check for this event


def configureHealth(reason):        #change user health and life values according to event the user went through
    global health, imgHealth, showHealth, lives, imgLives, showLives, spawnid, ship, points, player
    if reason == 0:                 #if user hit an asteroid
        canvas.after_cancel(spawnid)    #stop spawning asteroids
        for a in range(20):
            asteroids[a].deleteAsteroid()       #delete all the asteroids
        lives -= 1      #take away and life and tell the user what happened
        messagebox.showinfo('Asterpocalypse', "You're dead!\nEither your health has depleted or you crashed into an asteroid!\nYou have " + str(lives) + ' lives remaining.')
        time.sleep(0.5)     #add a little wait time so the ships explosion has time to disappear
        if lives == 0:          #if lives become 0, restart the game or exit
            canvas.delete(showLives)        #show amount of lives and prompt user for choice
            answer = messagebox.askyesno('Asterpocalypse', "GAME OVER!\nYou finished with " + str(points) + " points.\nWould you like to play again?")
            if answer:      #if user wants to restart, reset all values
                time.sleep(0.5)
                ship, points, lives, health = True, 0, 3, 10
                showLives = canvas.create_image(canvas.winfo_reqwidth() - imgLives[0].width() + 5, 50, image=imgLives[lives - 1])
                canvas.itemconfig(showHealth, image = imgHealth[health])
                root.bind("<Motion>", onmousemove)
                canvas.itemconfig(showPoints, text = str(points))
                spawnasteroid()
            else:       #otherwise, exit the game
                exit_program()
        else:   #if user still has lives, reset the ship, health asteroids
            ship, health = True, 10
            canvas.itemconfig(showLives, image=imgLives[lives - 1])     #show amount of remaining lives
            canvas.itemconfig(showHealth, image = imgHealth[health])
            root.bind("<Motion>", onmousemove)
            spawnasteroid()

    elif reason == 1:       #if user loses all health, take away a life
        health -= 1
        canvas.itemconfig(showHealth, image=imgHealth[health])
        if health == 0:
            explode_ship()
            configureHealth(0)


root.config(cursor="none")  # hide the cursor
root.title('Asterpocalypse')
root.protocol('WM_DELETE_WINDOW', exit_program)     #window handling

imgBackground = PhotoImage(file='images/space_background.png')      #imgs for game screen
imgTitle = PhotoImage(file='images/asterpocalypse.png')

root.geometry("%dx%d+%d+%d" % (
imgBackground.width(), imgBackground.height(), root.winfo_screenwidth() // 2 - imgBackground.width() // 2,
root.winfo_screenheight() // 2 - imgBackground.height() // 2))      #size of game screen

canvas = Canvas(root, width=imgBackground.width(), height=imgBackground.height())     #canvas to put imgs, widgets and objects on
canvas.pack()

background_list = [0] * 2       #background properties and handling
xpos = [0, imgBackground.width()]

for i in range(len(background_list)):
    background_list[i] = canvas.create_image(xpos[i], 0, image=imgBackground, anchor='nw')

canvas.create_image(canvas.winfo_reqwidth() // 2 - imgTitle.width() // 2, 10, image=imgTitle, anchor='nw')

imgHealth = [0] * 11        #list to hold health imgs, set them on the canvas
for num in range(len(imgHealth)):
    imgHealth[num] = PhotoImage(file="images/health" + str(num) + ".png")

showHealth = canvas.create_image(canvas.winfo_reqwidth() - imgHealth[health].width() + 25, 20, image=imgHealth[health])

imgLives = [0] * 3          #list to hold lives imgs, set them on the canvas
for number in range(len(imgLives)):
    imgLives[number] = PhotoImage(file="images/lives" + str(number + 1) + ".png")

showLives = canvas.create_image(canvas.winfo_reqwidth() - imgLives[0].width() + 5, 50, image=imgLives[lives - 1])
#text showing points
showPoints = canvas.create_text(30, 10, text='Spacebar', font="neuropol.ttf 30", fill="orange", anchor="nw")

background_timer()      #background animation timer

player = Spaceship(canvas)      #create a player spaceship object
lasers = [Laser(canvas)] * 10       #list of laser objects
asteroids = [Asteroid(canvas)] * 20     #list of asteroid objects
spawnasteroid()

root.bind("<Motion>", onmousemove)      #event handling for cursor movement and keyboard clicks
root.bind("<KeyRelease>", shoot)

hit_asteroid()      #collision detection and health loss detection
hit_ship()
lose_health()

root.mainloop()     #loop the game window to keep it on
