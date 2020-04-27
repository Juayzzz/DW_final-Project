from kivy.app import App
from kivy.uix.widget import Widget #to create widget
from kivy.graphics import Rectangle  #for my canvas to draw background
from kivy.core.window import Window
from kivy.clock import Clock   #to execute a function every frame
from kivy.core.audio import SoundLoader #play sound
from kivy.uix.label import CoreLabel #to draw text on canvas
from kivy.uix.popup import Popup #for pop up
from kivy.uix.button import Button
from kivy.factory import Factory
import random


class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #to use keyboard to play
        self._keyboard = Window.request_keyboard(
            self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self._score_label = CoreLabel(text="Score: 0",font_size=20) #init score label
        self._score_label.refresh()  #so can update score
        self._score = 0 #initial score

        self._life_label = CoreLabel(text="Life: 10",font_size=20) #init life lbel
        self._life_label.refresh()  #so can update life
        self._life = 10 #initial life

        self.register_event_type("on_frame")  

        with self.canvas:
            #my background
            Rectangle(source="assets/background.png", pos=(0, 0),
                      size=(Window.width, Window.height))
            #my score text on top left
            self._score_instruction = Rectangle(texture=self._score_label.texture, pos=(
                0, Window.height - 50), size=self._score_label.texture.size)
            #life text top left
            self._life_instruction = Rectangle(texture=self._life_label.texture, pos=(
                0, Window.height - 75), size=self._life_label.texture.size)

        self.keysPressed = set()
        self._entities = set()

        Clock.schedule_interval(self._on_frame, 0)

        self.sound = SoundLoader.load("assets/music.WAV")
        self.sound.play()

        Clock.schedule_interval(self.spawn_enemies, 1.5) #to spawn enemies every 1.5secs

    def spawn_enemies(self, dt):
        if self._score>-1 and self._score<15:
            for i in range(self._score+int(2)):
                random_y = random.randint(10, Window.height-100)
                x = Window.width
                random_speed = random.randint(150, 400) #to spawn  enemies with a random speed between 150 to 400
                self.add_entity(Enemy((x, random_y), random_speed))
        elif self._score>14 and self._score<100:
            for i in range(15):
                random_y = random.randint(10, Window.height-100)
                x = Window.width
                random_speed = random.randint(350, 500)
                self.add_entity(Enemy((x, random_y), random_speed))
        elif self._score>99 and self._score<200:
            for i in range(14):
                random_y = random.randint(10, Window.height-100)
                x = Window.width
                random_speed = random.randint(450, 600)
                self.add_entity(Enemy((x, random_y), random_speed))
        elif self._score>199:
            for i in range(10):
                random_y = random.randint(10, Window.height-100)
                x = Window.width
                random_speed = random.randint(650, 800)
                self.add_entity(Enemy((x, random_y), random_speed))
        elif self._score<0 and self._score>-50:
            for i in range(10):
                random_y = random.randint(10, Window.height-100)
                x = Window.width
                random_speed = random.randint(800, 900)
                self.add_entity(Enemy((x, random_y), random_speed))
        elif self._score<-49:
            for i in range(15):
                random_y = random.randint(10, Window.height-100)
                x = Window.width
                random_speed = random.randint(800, 1000)
                self.add_entity(Enemy((x, random_y), random_speed))
            

    def _on_frame(self, dt):
        self.dispatch("on_frame", dt) 

    def on_frame(self, dt):
        pass

    @property
    def score(self):  #score getter
        return self._score 

    @score.setter
    def score(self, value):  #score setter
        self._score = value #set private attribute of score
        self._score_label.text = "Score: " + str(value) #to add a value to 'score'
        self._score_label.refresh() #update label text
        self._score_instruction.texture = self._score_label.texture #update texture of instruction
        self._score_instruction.size = self._score_label.texture.size #update size of instruction

    @property
    def life(self):  #life getter
        return self._life 

    @life.setter
    def life(self, lifes):  #life setter
        self._life = lifes #set private attribute of score
        self._life_label.text = "Life: " + str(lifes) #to add a value to 'score'
        self._life_label.refresh() #update label text
        self._life_instruction.texture = self._life_label.texture #update texture of instruction
        self._life_instruction.size = self._life_label.texture.size #update size of instruction

    def add_entity(self, entity):
        self._entities.add(entity)
        self.canvas.add(entity._instruction)

    def remove_entity(self, entity):
        if entity in self._entities:
            self._entities.remove(entity)
            self.canvas.remove(entity._instruction)

    def collides(self, e1, e2):  #axis aligned bounding box collision pos,0 position is xvalue,1 position is yvalue
        r1x = e1.pos[0]
        r1y = e1.pos[1]
        r2x = e2.pos[0]
        r2y = e2.pos[1]
        r1w = e1.size[0]
        r1h = e1.size[1]
        r2w = e2.size[0]
        r2h = e2.size[1]

        if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
            return True
        else:
            return False

    def colliding_entities(self, entity): #takes in an entity and see if it collides with our entity.
        result = set() #empty set
        for e in self._entities:
            if self.collides(e, entity) and e != entity: #the entity we checking for will also be in entity list, so we must have !, to show not equal.if not will show self collision
                result.add(e)
        return result

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keysPressed.add(keycode[1])

    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

class GameOver(Popup): #popup to show you have lost:(
    def open(self, text, btn_text='Retry!'):
        self.dismiss_btn = Button(text=btn_text, on_press=self.closeApp)
        self.popup = Popup(title=text, content = self.dismiss_btn, size_hint = (1, 0.2))
        self.popup.open()
    pass


class Entity(object):
    def __init__(self):
        self._pos = (0, 0)
        self._size = (100, 100) #size of my player(spongebob) and enemy(jellyfish) and bullet(bubble)
        self._source = "random.png"  #just something random that will be change using property
        self._instruction = Rectangle(
            pos=self._pos, size=self._size, source=self._source)  #initial instruction

#when position,size and source change, we change instruction, so entity is in sync with visual representation instruction in canvas
    @property
    def pos(self): #getter pos
        return self._pos

    @pos.setter
    def pos(self, value): #setter pos
        self._pos = value #private variable
        self._instruction.pos = self._pos 

    @property
    def size(self): #getter size
        return self._size

    @size.setter
    def size(self, value): #setter size
        self._size = value
        self._instruction.size = self._size

    @property
    def source(self): #getter source
        return self._source

    @source.setter
    def source(self, value): #setter source
        self._source = value
        self._instruction.source = self._source

class Bullet(Entity):
    def __init__(self, pos, speed=300):
        super().__init__()
        sound = SoundLoader.load("assets/pop.WAV")
        sound.play()
        self._speed = speed #init speed
        self.pos = pos #init pos
        self.source = "assets/bubble.png"
        game.bind(on_frame=self.move_step)  

    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)

    def move_step(self, sender, dt):
        # check for collision/out of bounds
        if self.pos[0] > Window.width: #out of bound
            self.stop_callbacks()
            game.remove_entity(self)
            return
        for e in game.colliding_entities(self):  #to check collision
            if isinstance(e, Enemy):
                game.add_entity(Explosion(self.pos))
                self.stop_callbacks()
                game.remove_entity(self) #bullet disappear
                e.stop_callbacks()
                game.remove_entity(e)  #enemy will die
                game.score += 1 #add score
                return
        

        # move in consistent rate, no matter what system its on
        step_size = self._speed * dt
        new_x = self.pos[0]+ step_size
        new_y = self.pos[1] 
        self.pos = (new_x, new_y)


class Enemy(Entity):
    def __init__(self, pos, speed=80):
        super().__init__()
        self._speed = speed
        self.pos = pos
        self.source = "assets/jellyfish.png"
        game.bind(on_frame=self.move_step)

    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)
        
    def move_step(self, sender, dt):
        # check for collision/out of bounds
        if self.pos[0] < 0:   #out of bound and remove bullet
            self.stop_callbacks()
            game.remove_entity(self)
            game.score -= 10 #lose pts
            return
        
        for e in game.colliding_entities(self):  #collision with player
            if e == game.player:
                game.add_entity(Explosion(self.pos))
                self.stop_callbacks()
                game.remove_entity(self)
                game.score -= 1
                

        # move
        step_size = self._speed * dt
        new_x = self.pos[0]- step_size
        new_y = self.pos[1] 
        self.pos = (new_x, new_y)


class Explosion(Entity): # animation when enemy dies
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        sound = SoundLoader.load("assets/pop.WAV")
        self.source = "assets/burst.png"
        sound.play()
        Clock.schedule_once(self._remove_me, 0.1)

    def _remove_me(self, dt):
        game.remove_entity(self)


done = False


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.source = "assets/player.png"
        game.bind(on_frame=self.move_step)
        self._shoot_event = Clock.schedule_interval(self.shoot_step, 0.13)
        self.pos = (0, 400)

    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)
        self._shoot_event.cancel()

    def shoot_step(self, dt):
        # shoot
        if "spacebar" in game.keysPressed:
            x = self.pos[0]+ 70
            y = self.pos[1] 
            game.add_entity(Bullet((x, y)))

    def closeApp(self,value):
        App.get_running_app().stop()
        Window.close()

    def move_step(self, sender, dt):  #to move and shoot for player. 's' to move down, 'w' to move up. 'spacebar' to shoot
        for e in game.colliding_entities(self):  #to check collision
            if isinstance(e, Enemy):
                game.add_entity(Explosion(self.pos))
                game.remove_entity(Enemy) #enemy disappear
                game.life -= 1 #minus life
                if game.score<-100:
                    game.life -= 1 #minus life
                if game.life<0 or game.life==0:
                    GameOver.open(self,'Good try! Retry?:)')  # to show you have lost :(
                return
           
        #movement and to ensure player don't go out of the screen       
        step_size = 400 * dt
        newx = self.pos[0]
        newy = self.pos[1]
        if "s" in game.keysPressed:
            if newy>0:
                newy -= step_size
            else:
                pass
                
        if "w" in game.keysPressed:
            if newy<Window.height-100:
                newy += step_size
            else:
                pass
        self.pos = (newx, newy)


game = GameWidget()   #making a global variable
game.player = Player()
game.player.pos = (0,Window.height/2) #starting point for player. which is middle of screen
game.add_entity(game.player)


class MyApp(App):
    def build(self):
        return game

if __name__ == "__main__":
    app = MyApp()
    app.run()

