import tkinter as tk
import math
import random
import time

fps = 60
game_speed = round(1000 / fps)
width = 1024
height = 768
speed = 16
pong_speed = 14

# Create a class for the game
class Pong(tk.Canvas):
    def __init__(self):
        super().__init__(
            width=width, height=height, bg="black", highlightthickness=0
        )
        self.time = time.time()
        
        self.player_position = height/2
        self.player_score = 0
        self.player_action = {'Up':0,'Down':0,'w':0,'s':0}

        self.computer_position = height/2
        self.computer_score = 0

        self.pack(anchor=tk.CENTER, expand=True)
        self.bind_all("<KeyPress>", self.on_keypress)
        self.bind_all("<KeyRelease>", self.on_keyrelease)

        self.create_objects()
        self.recreate_pong()

        self.after(game_speed, self.perform_actions)
    
    def on_keypress(self, e):
        if e.keysym in ["Up"]:
            self.player_action['Up'] = 1
        elif e.keysym in ["Down"]:  
            self.player_action['Down'] = 1
        if e.keysym in ["w"]:
            self.player_action['w'] = 1
        if e.keysym in ['s']:
            self.player_action['s'] = 1

    def on_keyrelease(self, e):
        if e.keysym in ["Up"]:
            self.player_action['Up'] -= 1
        if e.keysym in ["Down"]:
            self.player_action['Down'] -= 1
        if e.keysym in ["w"]:
            self.player_action['w'] -= 1
        if e.keysym in ['s']:
            self.player_action['s'] -= 1

    def create_objects(self):
        self.create_text(
            (width/2- 100, 35),
            text = self.player_score,
            fill = 'white',
            font = "terminal 40 bold",
            tag='player_score'
        )

        self.create_text(
            (width/2 + 100, 35),
            text = self.computer_score,
            fill = 'white',
            font = "terminal 40 bold",
            tag='computer_score'
        )
        
        for i in range(8):
            dashed_width = 8
            dashed_height = 60
            space = 37
            self.create_rectangle(
                (width/2 - dashed_width/2, 
                 15 + i*(dashed_height + space), 
                 width/2 + dashed_width/2, 
                 15 + dashed_height + i*(dashed_height + space)),
                fill = 'white'
            )
        
        self.paddle_height = 60
        paddle_width = 15
        paddle_offset = 40
        self.create_rectangle(
            (paddle_offset, self.player_position-self.paddle_height/2, 
             paddle_offset+paddle_width, self.player_position+self.paddle_height/2),
            fill = 'white',
            tag="player"
        )

        self.create_rectangle(
            (width-paddle_offset, self.computer_position-self.paddle_height/2, 
             width-paddle_offset-paddle_width, self.computer_position+self.paddle_height/2),
            fill = 'white',
            tag="computer"
        )

        self.pong_size = 10
        self.create_rectangle(
            (width/2-self.pong_size/2, height/2-self.pong_size/2, 
             width/2+self.pong_size/2, height/2+self.pong_size/2),
            fill = 'white',
            tag="pong"
        )

    def recreate_pong(self):
        pong = self.find_withtag('pong')
        self.moveto(pong, width/2, height/2)
        pong_angle = random.uniform(-math.pi * 1 / 4, math.pi * 1 / 4)
        self.pong_x = pong_speed * math.cos(pong_angle) * random.choice([-1, 1])
        self.pong_y = pong_speed * -math.sin(pong_angle) 
        


    def perform_actions(self):
        self.move_player()
        if time.time() - self.time > 1:
            self.move_pong()
        self.move_computer()
        self.after(game_speed, self.perform_actions)

    def move_player(self):
        player = self.find_withtag("player")
        player_speed = 0
        if self.player_action['Up'] or self.player_action['w']:
            player_speed -= speed
        if self.player_action['Down'] or self.player_action['s']:
            player_speed += speed
        if (self.coords(player)[1] > 0 or player_speed > 0) and (self.coords(player)[3] < height or player_speed < 0):
            self.move(player, 0, player_speed)
    
    def move_pong(self):
        self.pong_delay = False
        pong = self.find_withtag("pong")
        # If pong touches the top or bottom while moving further towards them, reverse it's y speed
        if (self.coords(pong)[1] < 0 and self.pong_y < 0) or (self.coords(pong)[3] > height and self.pong_y > 0):
            self.pong_y = -self.pong_y

        # Logic for detecting a win or a loss
        if self.coords(pong)[0] > width:
            self.win()
        
        if self.coords(pong)[2] < 0:
            self.lose()
        # Logic for detecting collision with the player paddle
        player = self.find_withtag("player")
        if self.coords(pong)[3] > self.coords(player)[1] and\
            self.coords(pong)[1] < self.coords(player)[3] and\
            self.coords(pong)[0] <= self.coords(player)[2] and\
            self.coords(pong)[0] >= self.coords(player)[0] and\
            self.pong_x < 0:
            # Find out where pong collided relative to paddle
            player_middle = (self.coords(player)[1] + self.coords(player)[3]) / 2 
            pong_middle = (self.coords(pong)[3] + self.coords(pong)[1]) / 2
            hit_distance = pong_middle-player_middle

            self.calculate_angle(hit_distance, 1)

        # Logic for detecting collision with the computer paddle
        computer = self.find_withtag('computer')
        if self.coords(pong)[3] > self.coords(computer)[1] and\
            self.coords(pong)[1] < self.coords(computer)[3] and\
            self.coords(pong)[2] <= self.coords(computer)[2] and\
            self.coords(pong)[2] >= self.coords(computer)[0] and\
            self.pong_x > 0:
            # Find out where pong collided relative to paddle
            computer_middle = (self.coords(computer)[1] + self.coords(computer)[3]) / 2 
            pong_middle = (self.coords(pong)[3] + self.coords(pong)[1]) / 2
            hit_distance = pong_middle-computer_middle

            self.calculate_angle(hit_distance, -1)

        self.move(pong, self.pong_x, self.pong_y)

    def calculate_angle(self, hit_distance, direction):
        max_hit_distance = (self.pong_size + self.paddle_height) / 2
        # Normalize hit distance to a value between 1 and -1
        normalized_hit_distance = hit_distance / max_hit_distance
        # Adapt the angle to the normalized hit distance, with a maximum angle of 60 degrees
        pong_angle = (math.pi * 1 / 3) * normalized_hit_distance
        self.pong_x = pong_speed * math.cos(pong_angle) * direction
        self.pong_y = pong_speed * math.sin(pong_angle) 

    def move_computer(self):
        computer = self.find_withtag("computer")
        pong = self.find_withtag("pong")

        computer_speed = 0

        computer_middle = (self.coords(computer)[1] + self.coords(computer)[3]) / 2 
        pong_middle = (self.coords(pong)[3] + self.coords(pong)[1]) / 2

        if computer_middle - pong_middle > self.paddle_height/2:
            computer_speed = -speed * 0.65
        elif computer_middle - pong_middle  < -self.paddle_height/2:
            computer_speed = speed * 0.65

        if (self.coords(computer)[1] > 0 or computer_speed > 0) and (self.coords(computer)[3] < height or computer_speed < 0):
            self.move(computer, 0, computer_speed)
    
    def win(self):
        player_score_text = self.find_withtag('player_score')
        self.player_score += 1
        self.itemconfigure(player_score_text, text=self.player_score)
        self.reset()
    
    def lose(self):
        computer_score_text = self.find_withtag('computer_score')
        self.computer_score += 1
        self.itemconfigure(computer_score_text, text=self.computer_score)
        self.reset()

    def reset(self):
        self.time = time.time()
        self.recreate_pong()
        


    
# Set up root screen
root = tk.Tk()
root.title('Pong')

window_width = 1024
window_height = 768

# # get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# # find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# # set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)

# Always display screen on top
root.attributes('-topmost', 1)

game = Pong()

root.mainloop()