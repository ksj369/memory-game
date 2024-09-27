# Memory game: a grid of hidden tiles is displayed. 
# When the player clicks on a tile this tile will flip and shows an image which
# will be compared with the next tile clicked by the player. 
# If the image is not same then the tile flip back to a hidden state
# else the image remains visible with it's pair
# the score is the amount of time the player takes to discover all the images
 

import pygame,random




# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game 
        self.surface = surface
        self.bg_color = pygame.Color('black')
        
        self.close_clicked = False
        self.continue_game = True

        # === initiallize game specific objects
        self.image_list=[]
        self.board_size=4
        self.board=[]
        self.hidden_tile_image=""  
        self.selected_images=[]
        self.score=0
        
        # create list of images and board
        self.create_image_list()    
        self.create_board()
        
        
    def create_image_list(self):
        # create the list of images that will be used in the game
        # -self is the Game in which the images will be used
        
        for index in range(self.board_size*2+1):
            self.image_list.append(pygame.image.load("image"+str(index)+".bmp"))
        
        # initiallize the hidden tile image    
        self.hidden_tile_image=self.image_list.pop(0)
        
        # create pair images and shuffle the list
        self.image_list+=self.image_list
        random.shuffle(self.image_list)
            
            
    def create_board(self):
        # create a uniform board according to the board size
        # -self is the Game that contains the board
        width=(self.surface.get_width()//(self.board_size+1))
        height=(self.surface.get_height()//self.board_size)
        for row_index in range(0,self.board_size): 
            row=[]
            for column_index in range(0,self.board_size):
                x=(column_index*width)
                y=(row_index*height)
                # create a Tile object for each tile
                tile=Tile(x,y,width,height,self.surface,self.hidden_tile_image,self.image_list.pop())
                row.append(tile)
            self.board.append(row)

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()            
            if self.continue_game:
                self.update()
                self.decide_continue()

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type==pygame.MOUSEBUTTONUP and self.continue_game:
                self.handle_mouse_up(event.pos)
                
    def handle_mouse_up(self,location):
        # Handle MOUSEBUTTONUP events
        # self is the Game whose event will be handled
        # location is the position where the mouse is clicked
        for row in self.board:
            for tile in row:
                if tile.select(location): # location: type tuple
                    self.selected_images.append(tile)

    
    def draw_score(self):
        # draw the score on the screen
        # - self is the Game
        
        fg_color=pygame.Color("white")
        font=pygame.font.SysFont("",80)
        score_image=font.render(str(self.score),True,fg_color)
        x=self.surface.get_width()-score_image.get_width()
        y=0
        location=(x,y)
        self.surface.blit(score_image,location)
        
        
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color) # clear the display surface first
        # draw board
        for row in self.board:
            for tile in row:
                tile.draw() # tile is an object of type Tile
        self.draw_score()
        pygame.display.update() # make the updated surface appear on the display

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        
        if len(self.selected_images)==2: # self.selected_images is a list containing Tile objects
            self.selected_images[0].compare_image(self.selected_images[1])
            # clear list for next pair selection
            self.selected_images=[]
        self.score=pygame.time.get_ticks()//1000
      
    
    def decide_continue(self):
        # Check and determine if the game should continue
        # - self is the Game to check
        self.continue_game=False
        for row in self.board:
            for tile in row:
                #check if a tile is still undiscovered
                if not tile.discovered:
                    self.continue_game=True


class Tile:
    # an object in this class represents a Tile
    
    def __init__(self,x,y,width,height,surface,hidden_image,reveal_image):
        # initiallize a Tile
        # -self is the tile to initiallize
        # -x is the x-coordinate of the tile
        # -y is the y-coordinate of the tile
        # -width is the width of the tile
        # -height is the height of the tile
        # -surface is the window's pygame.Surface object
        # -hidden_image:the image to be used when the tile is in hidden state
        # -reveal_image: the image to be used when the tile is not in hidden state
        
        self.rect=pygame.Rect(x,y,width,height)
        self.surface=surface
        self.hide_image=hidden_image
        self.reveal_image=reveal_image
        self.hidden=True
        self.discovered=False
        
    def draw(self):
        # draw the tile on the surface
        # -self is the Tile
        
        color=pygame.Color("black")
        # check hidden state then draw appropriate image
        if  self.hidden:
            self.draw_content(self.hide_image)
        else:
            self.draw_content(self.reveal_image) 
        # draw rectangle with border on top of image
        pygame.draw.rect(self.surface,color,self.rect,3)
    
    def draw_content(self,content):
        # draw the content of a Tile
        # -self is the Tile
        
        # center the content in the tile and draw on surface
        d_x=(self.rect.width- content.get_width())//2  
        d_y=(self.rect.height- content.get_height())//2           
        x=self.rect.x+d_x
        y=self.rect.y+d_y
        location=(x,y)
        self.surface.blit(content,location)
        
    def select(self,location):
        # determine if tile can be selected: return True or False
        # -self is the Tile
        # -location is the position of the mouse click
        valid_click=False
        # check if tile is in hidden state and not already discovered
        if self.rect.collidepoint(location) and not self.discovered and self.hidden:
            self.hidden=False
            valid_click=True
        return valid_click
            
    def compare_image(self,other_tile):
        # compare the image in tile with another image in another tile
        # -self is the Tile
        # -other_tile is another Tile object
        
        # if not simillar images tiles return back to hidden state
        # else tiles turn in discovered state
        if self.reveal_image!=other_tile.reveal_image:
            pygame.time.delay(500)
            self.hidden=True
            other_tile.hidden=True
        else:
            self.discovered=True
            other_tile.discovered=True


# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Memory')   
    # get the display surface
    w_surface = pygame.display.get_surface() 
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play() 
    # quit pygame and clean up the pygame window
    pygame.quit() 


    
main()

