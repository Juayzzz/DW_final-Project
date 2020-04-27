# Digital-World-Project
SPONGEBOB BULLET HELL
------
This game is a combination of your bullet hell game and spongebob.
In the game, you are playing as Spongebob(Player), and using the power of bubblesbullet) to defeat the jellyfish(enemy)
The aim of this game is to get the highest score possible!
I used python 3 and the 3 key libraries used are:
1. Kivy
2. Random

HOW TO PLAY?
------
Once you run the code the game will begin. 
You have 3 available buttons to press which are:
1. 'w' key
2. 's' key
3. 'spacebar' key

| Keys          | Action        |
| :-----------: |:-------------:| 
| 'w'           | right-aligned | 
| 's'           | centered      |   
| 'spacebar'    | are neat      |   

The aim is to reach the highest score possible. For the fun,you challenge your friend to see who can get the highest score.

CODE DESCRIPTION
------

There are 8 Main class and I only use kivy and random to create this game

THE 8 MAIN CLASS
------
1. MyApp(App)
* It is the base for creating kivy applications.


2. GameWidget(Widget)
* Using kivy.uix.widget.
* The Widget class is the base class required for creating Widgets. 
* I used this to initialise a keyboard(for my movement and shooting), label for my score, label for my life, canvas for background, play sound and finally create a time interval(so that movement for my character is the same for every computer).
* I also def my spawn enemy rates here, def my getter and setter for both score and life, def my add_entity and remove_entity, and finally my collision entities.


3. GameOver(Popup)
* The Popup widget is used to create modal popups. 
* Used when the user loses the game


4. Entity(object)
* This is to ensure that all my Player(SPongebob), Enemy(Jellyfish) and bullet(bubble) have the same initial position, size, source and instruction which can be changed


5. Bullet(Entity)
* Initialise my Bullet to have sound,speed, pos and source.
* def stop_callbacks to stop it from moving
* def move_step to control its speed, check whether it is out of the screen and check whether it colliding with the enemy. When collides. When collide, it will remove the entity, while adding the explosion entity and adding score


6. Enemy(Entity)
* Initialise speed, pos, source
* def stop_callbacks to stop it from moving
* def move_step to check whether if out of bound, to check if there is collision with player and to control its speed


7. Explosion(Entity)
* Initialise pos, sound playing and schedule it to be removed after a specific time


8. Player(Entity)
* Initialise source, shootin, pos, movement
* def stopcallbacks to remove shooting and movement
* def shootstep so that when 'spacebar' is pressed, Player will shoot bullet, calling the bullet to spawn at a specific location and calling the class bullet⋅* def closeapp to close my window when Player press the button on the popup to show game has ended
* def movestep for movement using 's' and 'w' keys, checking of collision, minus life if collides
* created a global variable for gameWidget so can place a starting position of my player at a specific position


LINKS
------
Here are where I got my sound and picture:
* [PixelMaker](http://pixelartmaker.com/) is what I used to draw my pixel art of spongebob, jellyfish and bubble popping 
* [Fesliyanstudios](https://www.fesliyanstudios.com/royalty-free-music/downloads-c/action-music/9) is where I got my intense background music
* [Zapsplat](https://www.zapsplat.com/page/2/?s=bubble+popping&post_type=music&sound-effect-category-id) is where I got my bubble popping sound effect
* [Google](https://www.google.com/url?sa=i&url=https%3A%2F%2Fpngimage.net%2Fspongebob-background-png-4%2F&psig=AOvVaw3NHbAStm8MasfLgT_ft58C&ust=1587832370087000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCOC9_9mbiOkCFQAAAAAdAAAAABAD) is where I got my spongebob background
* [My video about the game](https://youtu.be/Yj11rsfllSA) Watch this to find out about my game! :)

*GAME ON!*
