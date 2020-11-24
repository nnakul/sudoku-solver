

import pygame
import tkinter
from time import sleep
from random import randint
from tkinter import messagebox
from timeit import default_timer as timer


pygame.init()
CELL_WIDTH = 51
SCREEN_WIDTH = CELL_WIDTH * 9
SUBCELL_WIDTH = int (CELL_WIDTH / 3)

root = pygame.display.set_mode((SCREEN_WIDTH+2, SCREEN_WIDTH+2))
pygame.display.set_caption('SUDOKU')


print('\n\nCLICK space TO ACTIVATE PENCIL MODE')
print('CLICK s TO SUBMIT YOUR BOARD AND SHOW THE RESULT')
print('CLICK enter TO VIEW THE SOLVED BOARD')


COLORS   =  {
                'white' : (255, 255, 255) ,
                'black' : (0, 0, 0) ,
                'pink' : (255, 20, 147) ,
                'darkGrey' : (47, 79, 79) ,
                'blue' : (0, 0, 128) ,
                'grey' : (119, 136, 153) ,
                'green' : (0, 255, 0) ,
                'red' : (255, 0, 0) ,
                'cream' : (255, 248, 220)
            }


root.fill(COLORS['white'])
pygame.display.update()



class Game :
    
    pencilOn = False
    solving = False
    winStatus = None
    completed = False
    
    n = None
    available_boards = (
                            [
                                [2, 7, n, 5, n, 6, 1, n, 8] ,
                                [n, n, n, 2, 9, n, n, n, n] ,
                                [n, 4, n, n, n, n, n, n, n] ,
                                [7, n, 8, 1, n, n, 4, 6, n] ,
                                [4, 1, n, n, n, n, n, n, 2] ,
                                [5, n, n, n, n, n, n, n, n] ,
                                [n, n, 5, n, 8, 4, n, n, 9] ,
                                [n, n, n, n, n, n, n, n, 3] ,
                                [3, n, 4, 9, 7, 1, n, 2, 6]
                            ] , # medium - level
                            
                            [
                                [1, 5, n, n, n, 2, n, 3, 8] ,
                                [9, 6, 7, 5, 3, n, n, n, n] ,
                                [n, n, 2, 7, 1, 4, n, 9, 6] ,
                                [7, 9, 6, 3, 4, n, 8, n, 2] ,
                                [2, 4, 3, n, 7, 5, 9, 6, 1] ,
                                [n, n, n, n, n, 9, 3, n, n] ,
                                [n, 3, 9, 1, 2, 6, 4, 7, n] ,
                                [6, 7, n, n, 5, n, 2, 8, n] ,
                                [4, 2, n, 9, 8, n, 6, n, n]
                            ] , # easy - level
                            
                            [
                                [3, 9, 5, 4, 8, n, n, n, n] ,
                                [n, n, n, n, 9, n, n, n, 5] ,
                                [8, n, 2, n, n, 7, n, n, 1] ,
                                [5, 2, 9, n, n, n, n, n, n] ,
                                [n, n, n, n, n, n, n, n, 4] ,
                                [4, n, n, 9, n, n, 2, 5, n] ,
                                [n, 4, n, 6, n, n, 1, n, n] ,
                                [6, 1, n, 8, 7, n, n, n, n] ,
                                [9, n, n, n, 4, 3, n, 6, n]
                            ] , # medium - level
                            
                            [
                                [n, 3, 8, n, 5, n, n, n, n] ,
                                [6, n, 2, n, n, 4, 1, 8, n] ,
                                [n, n, n, n, n, n, n, n, n] ,
                                [n, 8, 6, n, n, 1, 9, 3, n] ,
                                [n, 4, n, n, n, n, n, 6, n] ,
                                [n, 9, 3, 2, n, n, 4, 5, n] ,
                                [n, n, n, n, n, n, n, n, n] ,
                                [n, 1, 4, 6, n, n, 5, n, 3] ,
                                [n, n, n, n, 3, n, 6, 4, n]
                            ] , # hard - level
                            
                            [
                                [1, n, n, 9, n, 3, n, n, n] ,
                                [n, n, n, n, n, n, n, n, n] ,
                                [3, 8, n, n, 1, n, 5, n, n] ,
                                [n, n, n, 5, n, n, n, 4, 3] ,
                                [n, 9, 8, n, 6, n, n, n, n] ,
                                [n, n, 4, n, n, n, n, n, 7] ,
                                [n, n, n, n, n, n, n, n, n] ,
                                [n, 5, n, 6, n, 8, n, n, n] ,
                                [4, n, n, n, 3, 2, n, 1, n]
                            ] , # expert - level
                            
                            [
                                [n, n, 5, 1, n, 6, n, n, 4] ,
                                [3, n, n, n, 7, n, n, 2, n] ,
                                [n, n, n, 4, 8, n, n, n, n] ,
                                [9, 8, n, 3, 2, n, n, n, n] ,
                                [n, n, n, n, n, n, n, n, 1] ,
                                [5, 7, n, n, 4, n, n, n, n] ,
                                [n, n, n, n, n, n, n, n, n] ,
                                [n, n, 7, n, n, n, 2, 5, n] ,
                                [n, n, n, 2, n, n, n, 9, n]
                            ] , # expert - level
                            
                            [
                                [n, 8, n, 5, 6, 4, n, n, n] ,
                                [n, n, 9, n, n, n, n, n, 6] ,
                                [n, 5, 4, n, n, 9, n, 2, n] ,
                                [n, n, n, n, 5, 8, n, n, 3] ,
                                [n, n, n, 4, n, 2, n, n, n] ,
                                [4, n, n, 7, 9, n, n, n, n] ,
                                [n, 3, n, 9, n, n, 8, 7, n] ,
                                [9, n, n, n, n, n, 2, n, n] ,
                                [n, n, n, 2, 8, 6, n, 9, n]
                            ] , # hard - level
                            
                            [
                                [n, n, n, n, 1, 4, 6, 9, n] ,
                                [n, n, 2, n, n, n, n, n, n] ,
                                [n, n, 7, n, n, 2, n, n, n] ,
                                [n, 6, n, n, 8, n, n, 2, 3] ,
                                [n, 1, n, n, 5, n, n, n, n] ,
                                [n, n, 3, n, 6, n, n, n, 8] ,
                                [n, n, n, 5, n, n, 9, n, n] ,
                                [n, 2, n, n, n, n, n, 3, n] ,
                                [4, n, 5, n, n, n, n, n, n]
                            ] , # expert - level
                            
                            [
                                [n, n, n, n, 8, 7, 3, n, 9] ,
                                [n, n, n, 9, n, 6, n, n, n] ,
                                [n, 4, 5, n, n, n, n, n, n] ,
                                [n, n, 4, 8, n, n, 6, n, 5] ,
                                [2, 8, n, n, n, n, n, 9, 1] ,
                                [5, n, 6, n, n, 1, 7, n, n] ,
                                [n, n, n, n, n, n, 5, 6, n] ,
                                [n, n, n, 3, n, 8, n, n, n] ,
                                [4, n, 8, 5, 6, n, n, n, n]
                            ] , # hard - level
                            
                            [
                                [n, n, n, n, n, n, 7, n, n] ,
                                [n, n, 9, n, 1, n, n, 4, n] ,
                                [n, 2, 4, 7, 8, 9, n, 3, n] ,
                                [8, n, n, n, n, 6, n, n, n] ,
                                [3, 7, 2, 4, n, n, 8, n, n] ,
                                [n, 5, n, 1, 2, 8, n, n, n] ,
                                [n, 8, n, n, 4, n, n, n, 5] ,
                                [n, n, n, n, n, 7, 9, 2, n] ,
                                [2, 4, 7, n, n, n, n, n, n]
                            ] , # medium - level
                            
                            [
                                [n, n, 7, n, 2, 3, n, 5, n] ,
                                [n, 6, 4, 1, n, 7, n, n, n] ,
                                [n, n, n, n, n, n, n, n, 3] ,
                                [8, 2, n, n, 3, n, n, n, n] ,
                                [n, n, n, n, n, 6, n, n, n] ,
                                [n, n, n, n, n, 8, 4, n, n] ,
                                [n, n, n, n, n, n, n, n, 6] ,
                                [5, n, n, n, n, n, n, 3, n] ,
                                [n, n, n, 9, 1, n, 5, n, 2]
                            ] , # expert - level
                            
                            [
                                [n, n, n, n, 8, 1, 2, 4, 9] ,
                                [5, n, n, n, n, n, n, n, n] ,
                                [n, n, 4, n, n, n, n, n, n] ,
                                [4, n, n, n, n, 9, n, n, 2] ,
                                [3, n, 9, 8, 5, n, 1, n, 4] ,
                                [n, n, 8, n, 7, 6, 5, n, n] ,
                                [n, 1, n, 6, n, n, 4, 2, 7] ,
                                [n, n, n, 1, n, n, n, n, n] ,
                                [n, 3, 6, n, n, n, n, 8, 1]
                            ] , # medium - level
                            
                            [
                                [n, 9, 6, n, n, 8, 1, 2, 3] ,
                                [3, 5, n, 4, n, n, n, n, 8] ,
                                [n, n, 8, n, n, n, n, 9, 4] ,
                                [n, 7, n, n, n, n, n, 8, n] ,
                                [n, n, n, n, 8, 2, 6, n, n] ,
                                [2, n, n, n, n, 3, 4, n, 5] ,
                                [n, n, 2, 3, 4, n, n, 5, n] ,
                                [n, n, n, n, n, n, 8, n, n] ,
                                [n, 4, 7, n, n, n, n, 1, n]
                            ]   # medium - level
                            
                        )
    
    available_boards_count = 13
    unused_boards = [ x for x in range(0, available_boards_count) ]
    default_board = available_boards[ unused_boards.pop( randint(0, len(unused_boards)-1) ) ]
    
    
    @classmethod                
    def change_pencil_mode(cls) :
        if cls.pencilOn :
            cls.pencilOn = False
            pygame.display.set_caption('SUDOKU')
        elif not cls.pencilOn :
            cls.pencilOn = True
            pygame.display.set_caption('SUDOKU      ( pencil - mode )')
    
    
    @classmethod                
    def change_default_board(cls) :
        if not len(cls.unused_boards) :
            cls.unused_boards = [ x for x in range(0, cls.available_boards_count) ]
        cls.default_board = cls.available_boards[ cls.unused_boards.pop( randint(0, len(cls.unused_boards)-1) ) ]

    

class Cell :
    
    def __init__ (self, position, value) :
        self.pos = position
        self.val = value
        self.subVal = set()
        self.isEmpty = False if value else True
        self.byDefault = True if value else False # if the number was on the default board
        
    def update_value(self, new_val) :
        self.val = new_val
        self.isEmpty = False if new_val else True
        


def make_board() :
    grid = list()
    
    for i in range(0,9) :
        grid.append(list())
        for j in range(0,9) :
            grid[i].append( Cell((i,j), Game.default_board[i][j]) )
            
    return grid
 


for_sub_cells = [   (0,0), (SUBCELL_WIDTH,0), (2*SUBCELL_WIDTH,0),
                    (0,SUBCELL_WIDTH), (SUBCELL_WIDTH,SUBCELL_WIDTH), (2*SUBCELL_WIDTH,SUBCELL_WIDTH),
                    (0,2*SUBCELL_WIDTH), (SUBCELL_WIDTH,2*SUBCELL_WIDTH), (2*SUBCELL_WIDTH,2*SUBCELL_WIDTH)   
                ]

 
    
def draw_board(grid) :
    
    
    if Game.completed :
        root.fill(COLORS['white'])
        
        if Game.winStatus == 'win' : color = COLORS['green']
        if Game.winStatus == 'lose' : color = COLORS['red']
        
        for x in range(0,10) :
            if x in (0,3,6,9) :
                pygame.draw.line(root, color, (x*CELL_WIDTH, 0), (x*CELL_WIDTH, SCREEN_WIDTH), 4)
                pygame.draw.line(root, color, (0, x*CELL_WIDTH), (SCREEN_WIDTH, x*CELL_WIDTH), 4)
            else :
                pygame.draw.line(root, color, (x*CELL_WIDTH, 0), (x*CELL_WIDTH, SCREEN_WIDTH))
                pygame.draw.line(root, color, (0, x*CELL_WIDTH), (SCREEN_WIDTH, x*CELL_WIDTH))
        
        for i in range(0,9) :
            for j in range(0,9) :
                coords = ( grid[i][j].pos[1]*CELL_WIDTH, grid[i][j].pos[0]*CELL_WIDTH )
                text = str( grid[i][j].val )
                custom_font = pygame.font.Font('freesansbold.ttf', 36)
                if grid[i][j].byDefault : text_surface = custom_font.render(text, True, COLORS['black'])
                else :  text_surface = custom_font.render(text, True, COLORS['blue'])
                text_rect = text_surface.get_rect()
                text_rect.center = ( coords[0] + CELL_WIDTH/2, coords[1] + CELL_WIDTH/2 )
                root.blit(text_surface, text_rect)
        
        pygame.display.update()
        return
    
    
    if Game.solving :
        root.fill(COLORS['white'])
        
        for x in range(0,10) :
            if x in (0,3,6,9) :
                pygame.draw.line(root, COLORS['darkGrey'], (x*CELL_WIDTH, 0), (x*CELL_WIDTH, SCREEN_WIDTH), 4)
                pygame.draw.line(root, COLORS['darkGrey'], (0, x*CELL_WIDTH), (SCREEN_WIDTH, x*CELL_WIDTH), 4)
            else :
                pygame.draw.line(root, COLORS['black'], (x*CELL_WIDTH, 0), (x*CELL_WIDTH, SCREEN_WIDTH))
                pygame.draw.line(root, COLORS['black'], (0, x*CELL_WIDTH), (SCREEN_WIDTH, x*CELL_WIDTH))
        
        for i in range(0,9) :
            for j in range(0,9) :
                coords = ( grid[i][j].pos[1]*CELL_WIDTH, grid[i][j].pos[0]*CELL_WIDTH )
                
                if grid[i][j].isEmpty : 
                    if grid[i][j].val == 0 :    
                        pygame.draw.rect(root, COLORS['red'], coords+(CELL_WIDTH, CELL_WIDTH), 4)
                    continue
                
                text = str( grid[i][j].val )
                custom_font = pygame.font.Font('freesansbold.ttf', 36)
                
                if grid[i][j].byDefault : text_surface = custom_font.render(text, True, COLORS['black'])
                else :
                    pygame.draw.rect(root, COLORS['green'], coords+(CELL_WIDTH, CELL_WIDTH), 4)
                    text_surface = custom_font.render(text, True, COLORS['blue'])
                    
                text_rect = text_surface.get_rect()
                text_rect.center = ( coords[0] + CELL_WIDTH/2, coords[1] + CELL_WIDTH/2 )
                root.blit(text_surface, text_rect)
        
        pygame.display.update()
        return

    
    root.fill(COLORS['white'])
    
    mouse_pos = pygame.mouse.get_pos()
    top_left = int(mouse_pos[0]/CELL_WIDTH)*CELL_WIDTH, int(mouse_pos[1]/CELL_WIDTH)*CELL_WIDTH
    pygame.draw.rect(root, COLORS['cream'], top_left + (CELL_WIDTH,)*2)
    
    for i in range(0,9) :
        for j in range(0,9) :
            
            if grid[i][j].isEmpty :
                if len(grid[i][j].subVal) :
                   for x in grid[i][j].subVal :
                        coords = ( grid[i][j].pos[1]*CELL_WIDTH, grid[i][j].pos[0]*CELL_WIDTH )
                        coords = ( coords[0] + for_sub_cells[x-1][0], coords[1] + for_sub_cells[x-1][1] )
                        text = str( x )
                        custom_font = pygame.font.SysFont('arialblack', 12)
                        text_surface = custom_font.render(text, True, COLORS['grey'])
                        text_rect = text_surface.get_rect()
                        text_rect.center = ( coords[0] + SUBCELL_WIDTH/2, coords[1] + SUBCELL_WIDTH/2 )
                        root.blit(text_surface, text_rect)
                continue
           
            text = str( grid[i][j].val )
            custom_font = pygame.font.Font('freesansbold.ttf', 36)
            if grid[i][j].byDefault : text_surface = custom_font.render(text, True, COLORS['black'])
            else : text_surface = custom_font.render(text, True, COLORS['blue'])
            text_rect = text_surface.get_rect()
            
            coords = ( grid[i][j].pos[1]*CELL_WIDTH, grid[i][j].pos[0]*CELL_WIDTH )
            
            text_rect.center = ( coords[0] + CELL_WIDTH/2, coords[1] + CELL_WIDTH/2 )
            root.blit(text_surface, text_rect)
            
    for x in range(0,10) :
        if x in (0,3,6,9) :
            pygame.draw.line(root, COLORS['darkGrey'], (x*CELL_WIDTH, 0), (x*CELL_WIDTH, SCREEN_WIDTH), 4)
            pygame.draw.line(root, COLORS['darkGrey'], (0, x*CELL_WIDTH), (SCREEN_WIDTH, x*CELL_WIDTH), 4)
        else :
            pygame.draw.line(root, COLORS['black'], (x*CELL_WIDTH, 0), (x*CELL_WIDTH, SCREEN_WIDTH))
            pygame.draw.line(root, COLORS['black'], (0, x*CELL_WIDTH), (SCREEN_WIDTH, x*CELL_WIDTH))

    pygame.display.update()
    
 

def update_cell(board, value, position) :
    pos = ( int(position[1]/CELL_WIDTH), int(position[0]/CELL_WIDTH) )
    if board[pos[0]][pos[1]].byDefault : return
    
    if not Game.pencilOn :
        if board[pos[0]][pos[1]].val == value : 
            board[pos[0]][pos[1]].update_value(None)
            board[pos[0]][pos[1]].subVal.clear()
        else :  board[pos[0]][pos[1]].update_value(value)
        
    elif Game.pencilOn :
        board[pos[0]][pos[1]].update_value(None)
        if value in board[pos[0]][pos[1]].subVal :  board[pos[0]][pos[1]].subVal.remove(value)
        else :  board[pos[0]][pos[1]].subVal.add(value)



def solve_board( board, counter, showVis ) :
    empty_cell_pos = find_empty_cell(make_board(), counter)
    
    if not empty_cell_pos : 
        draw_board(board)
        return True
    
    empty_cell = board[empty_cell_pos[0]][empty_cell_pos[1]]
    
    for i in range(1,10) :
        if check_exit() : return 'quit'
        
        if check_fit(board, empty_cell, i) :
            if check_exit() : return 'quit'
            empty_cell.update_value(i)
            if showVis : draw_board(board)
            result = solve_board(board, counter+1, showVis)
            if result : 
                if result == 'quit' : return 'quit'
                return True
            else :  continue
    
    empty_cell.update_value(0)
    return False
    


def check_exit() :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            return True
    return False
    
    
    
def find_empty_cell(board, counter) :
    count = 0
    
    for row in range(0,9) :
        for col in range(0,9) :
            
            if board[row][col].isEmpty :
                count += 1
                
            if count == counter :
                return (row, col)

    return None
    
    
def check_fit(board, cell, val) :
    
    row = cell.pos[0]
    col = cell.pos[1]
    
    for x in range(0,9) :
        if board[row][x].val == val : return False
        if board[x][col].val == val : return False
    
    super_cell = ( int(row/3)*3, int(col/3)*3 )
    
    cells = [
                (super_cell[0], super_cell[1]) ,
                (super_cell[0] + 1, super_cell[1]) ,
                (super_cell[0] + 2, super_cell[1]) ,
                
                (super_cell[0], super_cell[1] + 1) ,
                (super_cell[0] + 1, super_cell[1] + 1) ,
                (super_cell[0] + 2, super_cell[1] + 1) ,
                
                (super_cell[0], super_cell[1] + 2) ,
                (super_cell[0] + 1, super_cell[1] + 2) ,
                (super_cell[0] + 2, super_cell[1] + 2)
            ]
    
    for each in cells :
        if board[each[0]][each[1]].val == val : return False
    
    return True
    


def show_visual() :
    popup = tkinter.Tk()
    popup.withdraw()
    
    answer = messagebox.askyesno('', 'Do you wish to see the visualisation and not simply display the solved board ?')
    
    popup.destroy()
    popup.mainloop()
    return bool(answer)
    
    
    
def ask_confirmation() :
    popup = tkinter.Tk()
    popup.withdraw()
    
    answer = messagebox.askyesno('', 'Are you sure about submitting your board ?')
    
    popup.destroy()
    popup.mainloop()
    return bool(answer)
    


def is_board_full (board) :
    for row in range(0,9) :
        for col in range(0,9) :
            if board[row][col].isEmpty : return False
    return True
    
    
    
def show_result (board) :
    board_values = list()
    
    for row in range(0,9) :
        board_values.append(list())
        for col in range(0,9) :
            board_values[row].append(board[row][col].val)
    
    for row in board_values :
        for i in range(1,10) :
            if not i in row : return False

    for col in range(0,9) :
        values = [ row[col] for row in board_values ]
        for i in range(1,10) :
            if not i in values : return False
   
    super_cells = [
                    [ row[0:3] for row in board_values[0:3] ] ,
                    [ row[3:6] for row in board_values[0:3] ] ,
                    [ row[6:9] for row in board_values[0:3] ] ,
                    [ row[0:3] for row in board_values[3:6] ] ,
                    [ row[3:6] for row in board_values[3:6] ] ,
                    [ row[6:9] for row in board_values[3:6] ] ,
                    [ row[0:3] for row in board_values[6:9] ] ,
                    [ row[3:6] for row in board_values[6:9] ] ,
                    [ row[6:9] for row in board_values[6:9] ]
    
                  ]
 
    for square in super_cells :
        for i in range(1,10) :
            if not ( (i in square[0]) or (i in square[1]) or (i in square[2]) ) :
                return False
    
    return True



board = make_board()
run = True
result_of_algo = None

input_keys = [  pygame.K_1, pygame.K_2, pygame.K_3,
                pygame.K_4, pygame.K_5, pygame.K_6,
                pygame.K_7, pygame.K_8, pygame.K_9  ]



while run :
    
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False
            
        if event.type == pygame.KEYUP :
            if event.key in input_keys :
                update_cell(board, input_keys.index(event.key)+1, pygame.mouse.get_pos())
                
            if event.key == pygame.K_SPACE :
                Game.change_pencil_mode()
                
            if event.key == pygame.K_BACKSPACE and ( Game.solving or Game.completed ) :
                Game.solving = False
                Game.completed = False
                result_of_algo = None
                Game.change_default_board()
                board = make_board()
                
            if event.key == pygame.K_s and not Game.solving and not Game.completed :
                if is_board_full(board) :
                    submit = ask_confirmation()
                    if submit :
                        print('\nBOARD SUBMITTED !')
                        Game.completed = True
                        Game.winStatus = 'win' if show_result(board) else 'lose'
                        
                        if Game.winStatus == 'win' :
                            print('CONGRATULATIONS! YOU WON .')
                        elif Game.winStatus == 'lose' :
                            print('SORRY! YOU LOST .')
                            
                        print('CLICK backspace TO START A NEW GAME')
                        draw_board(board)
                        
                else :  print('\nFILL ALL THE CELLS BEFORE SUBMITTING THE BOARD .')
                
            if event.key == pygame.K_RETURN and not Game.solving and not Game.completed :
                Game.solving = True
                new_board = make_board()
                draw_board(new_board)
                
                show_vis = show_visual()
                print('\nALGORITHM RUNNING ... PLEASE WAIT ...')
                startTime = timer()
                result_of_algo = solve_board( new_board, 1, show_vis )
                endTime = timer()
                if result_of_algo == 'quit' :
                    print('\nALGORITHM ABRUPTLY STOPPED AFTER {:.6f} SECONDS .'.format(endTime-startTime))
                    run = False
                    pygame.quit()
                else :
                    print('\nALGORITHM COMPLETED IN {:.6f} SECONDS .'.format(endTime-startTime))
                    print('CLICK backspace TO START A NEW GAME')
    
    
    if not result_of_algo and not Game.completed : draw_board(board)



print('\n\nGOODBYE ...')
pygame.quit()
sleep(1)
