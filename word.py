import random
import pygame

size = int(input("Enter the size of array: "))
z = int(input("Enter the number of words: "))

array = [[" " for _ in range(size)] for _ in range(size)]

words_with_directions = []
print("Direction codes: 1-Horizontal, 2-Vertical, 3-Diagonal L->R, 4-Diagonal R->L")
for i in range(z):
    while True:
        word = input(f"Enter word {i+1}: ").upper()
        if word.isalpha():
            break
        else:
            print(" Please enter a word with letters only.")
    while True:
        try:
            direction = int(input(f"Enter direction for '{word}': "))
            if direction in [1, 2, 3, 4]:
                break
            else:
                print("Enter a valid direction (1-4).")
        except ValueError:
            print("Please enter a number.")
    words_with_directions.append((word, direction))

def addhorizontally(array, word):
    size = len(array)
    added = False
    while not added:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - len(word))
        if all(array[row][col + i] == " " for i in range(len(word))):
            for i in range(len(word)):
                array[row][col + i] = word[i]
            added = True

def addvertically(array, word):
    size = len(array)
    added = False
    while not added:
        row = random.randint(0, size - len(word))
        col = random.randint(0, size - 1)
        if all(array[row + i][col] == " " for i in range(len(word))):
            for i in range(len(word)):
                array[row + i][col] = word[i]
            added = True

def adddiagonallyLF(array, word):
    size = len(array)
    added = False
    while not added:
        row = random.randint(0, size - len(word))
        col = random.randint(0, size - len(word))
        if all(array[row + i][col + i] == " " for i in range(len(word))):
            for i in range(len(word)):
                array[row + i][col + i] = word[i]
            added = True

def adddiagonallyRF(array, word):
    size = len(array)
    added = False
    while not added:
        row = random.randint(0, size - len(word))
        col = random.randint(len(word) - 1, size - 1)
        if all(array[row + i][col - i] == " " for i in range(len(word))):
            for i in range(len(word)):
                array[row + i][col - i] = word[i]
            added = True

for word, direction in words_with_directions:
    if direction == 1:
        addhorizontally(array, word)
    elif direction == 2:
        addvertically(array, word)
    elif direction == 3:
        adddiagonallyLF(array, word)
    elif direction == 4:
        adddiagonallyRF(array, word)

def fill_empty_cells(array):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == " ":
                array[i][j] = random.choice(alphabet)

fill_empty_cells(array)

# ============ Pygame GUI Section ============

pygame.init()
cell_size = 40
screen_size = size * cell_size + 200
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption("Word Search Solver!")
font = pygame.font.SysFont(None, 28)
clock = pygame.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)
color_palette = [(255, 182, 193),    
    (221, 160, 221),  
    (255, 160, 122),  
    (255, 105, 180),  
    (216, 191, 216),  
    (255, 218, 185),
(238, 130, 238)]
found_by_ai = []

def dfs(array, word, direction):
    size = len(array)
    if direction == 1:
        directions = [(0,1)]
    elif direction == 2:
        directions = [(1,0)]
    elif direction == 3:
        directions = [(1,1)]
    elif direction == 4:
        directions = [(1,-1)]
    else:
        directions = []

    def is_valid(x, y, visited):
        return 0 <= x < size and 0 <= y < size and (x, y) not in visited

    def search(x, y, index, visited, path):
        if array[x][y] != word[index]:
            return False
        path.append((x, y))
        if index == len(word) - 1:
            return list(path)
        visited.add((x, y))
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y, visited):
                result = search(new_x, new_y, index + 1, visited, path)
                if result:
                    return result
        visited.remove((x, y))
        path.pop()
        return False

    for i in range(size):
        for j in range(size):
            if array[i][j] == word[0]:
                result = search(i, j, 0, set(), [])
                if result:
                    return result
    return []

def draw_grid():
    screen.fill((230, 230, 250))
    
    welcome_font = pygame.font.SysFont(None, 28)
    welcome_text = welcome_font.render("WELCOME TO OUR GAME!", True, (128,0,128) )
    screen.blit(welcome_text,(screen_size//2-welcome_text.get_width()//2,10))
    
    for i in range(size):
        for j in range(size):
            x = j * cell_size + 100
            y = i * cell_size + 50
            rect = pygame.Rect(x, y, cell_size, cell_size)
            color = white
            for idx, (_, path) in enumerate(found_by_ai):
                if (i, j) in path:
                    color = color_palette[idx % len(color_palette)]
                    break
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, black, rect, 1)
            letter = font.render(array[i][j], True, black)
            screen.blit(letter, (x + 10, y + 5))
def main():
    global found_by_ai
    for word, direction in words_with_directions:
        path = dfs(array, word, direction)
        if path:
            found_by_ai.append((word, path))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        draw_grid()
        label = font.render("AI Found Words:", True, black)
        screen.blit(label, (20, size * cell_size + 60))
        y_offset = size * cell_size + 100
        for idx, (word, _) in enumerate(found_by_ai):
            text = font.render(f"✔ {word}", True,color_palette[idx % len(color_palette)] )
            screen.blit(text, (20, y_offset + idx * 30))

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
