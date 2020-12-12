import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from enum import IntEnum
import sys
import resource

class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class hougaku(IntEnum):
    FRONT = 0
    RIGHT = 1
    REAR = 2
    LEFT = 3

class Field():
    
    def __init__(self):
        self.GROUND = 0
        self.WALL = 1
        self.STATIC_WALL = 2
        self.START = 3
        self.GOAL = 4
        
        self.img = None
        self.is_show = False
        self.maze_height = 32
        self.maze_width = 32
        self.goal_coordinate_y = int(self.maze_height / 2)
        self.goal_coordinate_x = int(self.maze_width / 2)
        self.goal_y = self.goal_coordinate_y * 2 + 1
        self.goal_x = self.goal_coordinate_x * 2 + 1
        self.field_height = self.maze_height * 2 + 1
        self.field_width = self.maze_width * 2 + 1
        self.field = np.ones((self.field_height - 2, self.field_width - 2), dtype = int)
        self.field = np.pad(self.field, (1,1), 'constant', constant_values=(1))

        self.start_cells = []

    def create_maze(self):
        
        self.field[1,2] = self.STATIC_WALL
        self.field[1][1] = self.START

        for y in range(-1,2):
            for x in range(-1, 2):
                self.field[self.goal_y + y][self.goal_x + x] = self.STATIC_WALL
        self.field[self.goal_y][self.goal_x] = self.GOAL
        hole_direction = np.random.randint(0,3)
        
        if hole_direction == 0:
            self.field[self.goal_y][self.goal_x - 1] = self.WALL
        elif hole_direction == 1:
            self.field[self.goal_y + 1][self.goal_x] = self.WALL
        elif hole_direction == 2:
            self.field[self.goal_y][self.goal_x + 1] = self.WALL
        else:
            self.field[self.goal_y - 1][self.goal_x] = self.WALL
        
        self.dig_ground(self.goal_y, self.goal_x)

    def dig_ground(self, y, x):
        while(True):
            direction_candidate = []
            if 0 <= (x - 2) and (x - 2) < self.field_width and self.field[y][x - 1] != self.GROUND and self.field[y][x - 2] != self.GROUND and self.field[y][x - 1] != self.STATIC_WALL and self.field[y][x - 2] != self.STATIC_WALL:
                direction_candidate.append(Direction.LEFT)
                # print("LEFT")
            if 0 <= (y + 2) and (y + 2) < self.field_height and self.field[y + 1][x] != self.GROUND and self.field[y + 2][x] != self.GROUND and self.field[y + 1][x] != self.STATIC_WALL and self.field[y + 2][x] != self.STATIC_WALL:
                direction_candidate.append(Direction.DOWN)
                # print("UP")
            if 0 <= (x + 2) and (x + 2) < self.field_width and self.field[y][x + 1] != self.GROUND and self.field[y][x + 2] != self.GROUND and self.field[y][x + 1] != self.STATIC_WALL and self.field[y][x + 2] != self.STATIC_WALL:
                direction_candidate.append(Direction.RIGHT)
                # print("RIGHT")
            if 0 <= (y - 2) and (y - 2) < self.field_height and self.field[y - 1][x] != self.GROUND and self.field[y - 2][x] != self.GROUND and self.field[y - 1][x] != self.STATIC_WALL and self.field[y - 2][x] != self.STATIC_WALL:
                direction_candidate.append(Direction.UP)
                # print("DOWN")
            
            if len(direction_candidate) == 0:
                break

            self.set_start_coordinate(y, x)

            direction = np.random.randint(0, len(direction_candidate))

            if direction_candidate[int(direction)] == Direction.LEFT:
                x -= 1
                self.set_start_coordinate(y, x)
                x -= 1
                self.set_start_coordinate(y, x)
                # print("LEFT")
            elif direction_candidate[int(direction)] == Direction.DOWN:
                y += 1
                self.set_start_coordinate(y, x)
                y += 1
                self.set_start_coordinate(y, x)
                # print("DOWN")
            elif direction_candidate[int(direction)] == Direction.RIGHT:
                x += 1
                self.set_start_coordinate(y, x)
                x += 1
                self.set_start_coordinate(y, x)
                # print("RIGHT")
            elif direction_candidate[int(direction)] == Direction.UP:
                y -= 1
                self.set_start_coordinate(y, x)
                y -= 1
                self.set_start_coordinate(y, x)
                # print("UP")
        start_coordinate = self.get_start_coordinate()
        if (start_coordinate != None):
            self.dig_ground(start_coordinate['y'], start_coordinate['x'])

    def set_start_coordinate(self, y, x):
        
        if self.field[y][x] == self.WALL:
            self.field[y][x] = self.GROUND
        
        if (y % 2 == 1 and x % 2 == 1):
            self.start_cells.append({'y':y, 'x':x})
            # print(self.start_cells)
        

    def get_start_coordinate(self):
        if len(self.start_cells) == 0: return None
        index = np.random.randint(0, len(self.start_cells))
        return self.start_cells.pop(index)

    def create_view_field(self):
        global canvas, item
        self.root = tk.Tk()
        self.root.title("Field")
        sdf = self.field_to_Image()
        sdf = sdf.resize((self.field_width * 5,self.field_height * 5), Image.BOX)
        self.img = ImageTk.PhotoImage(image=sdf)
        canvas = tk.Canvas(self.root,width=self.field_width * 5 + 5,height=self.field_height * 5 + 5 + 30)
        canvas.pack()
        item = canvas.create_image(5,5 + 30, anchor="nw", image=self.img)
        self.create_button()
    
    def delete_view_field(self):
        self.root.destroy()

    def update_view(self):
        self.__init__()
        sdf = self.field_to_Image()
        sdf = sdf.resize((self.field_width * 5,self.field_height * 5), Image.BOX)
        sdf = ImageTk.PhotoImage(image=sdf)
        canvas.itemconfig(item,image=sdf)
        # canvas = tk.Canvas(self.root,width=self.field_width * 5 + 5,height=self.field_height * 5 + 5 + 30)
        # canvas.configure(Image=sdf)
        canvas.pack()
        canvas.create_image(5,5 + 30, anchor="nw", image=sdf)
        self.root.mainloop()


    def field_to_Image(self):
        rgb = np.zeros((self.field_height, self.field_width, 3))
        rgb += ((self.field.reshape([self.field_height * self.field_width, 1]) == self.GROUND) * np.array([255,255,255])).reshape((self.field_height,self.field_width, 3))
        rgb += ((self.field.reshape([self.field_height * self.field_width, 1]) == self.WALL) * np.array([0,0,0])).reshape((self.field_height,self.field_width, 3))
        rgb += ((self.field.reshape([self.field_height * self.field_width, 1]) == self.STATIC_WALL) * np.array([64,64,255])).reshape((self.field_height,self.field_width, 3))
        rgb += ((self.field.reshape([self.field_height * self.field_width, 1]) == self.START) * np.array([0,255,0])).reshape((self.field_height,self.field_width, 3))
        rgb += ((self.field.reshape([self.field_height * self.field_width, 1]) == self.GOAL) * np.array([255,0,0])).reshape((self.field_height,self.field_width, 3))

        image = Image.fromarray(rgb.astype(np.uint8))
        return image

    def get_wall(self):
        print('hogehoge')

    def create_button(self):
        btn = tk.Button(self.root, text='ボタン', background='blue', command=self.update_view)
        btn2 = tk.Button(self.root, text='閉じる', bg='yellow', command=self.delete_view_field)
        btn.place(x=5, y=5)
        btn2.place(x=100, y=5)

if __name__ == '__main__':
    sys.setrecursionlimit(20000)
    # resource.setrlimit(10 ** 10)
    asd = Field()
    asd.create_maze()
    asd.create_view_field()
    asd.root.mainloop()
    # input()
    # asd.delete_view_field()