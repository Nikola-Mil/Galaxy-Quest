import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("Galaxy Quest\Menu-System-PyGame-main/assets/wp7872665.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Galaxy Quest\Menu-System-PyGame-main/assets/font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        
        SCREEN.blit(BG,(0,0))

        OPTIONS_TEXT = get_font(45).render("Choose Difficulty", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        EASY_BUTTON = Button(image=None, pos=(320, 250), 
                            text_input="Easy", font=get_font(50), base_color="White", hovering_color="#d7fcd4")
        NORMAL_BUTTON = Button(image=None, pos=(640, 250), 
                            text_input="Normal", font=get_font(50), base_color="White", hovering_color="#d7fcd4")
        HARD_BUTTON = Button(image=None, pos=(960, 250), 
                            text_input="Hard", font=get_font(50), base_color="White", hovering_color="#d7fcd4")


        OPTIONS_BACK = Button(image=None, pos=(640, 400), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="#d7fcd4")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        EASY_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        NORMAL_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        HARD_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        EASY_BUTTON.update(SCREEN)
        NORMAL_BUTTON.update(SCREEN)
        HARD_BUTTON.update(SCREEN)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    # Set the difficulty level to easy
                    print("Easy difficulty selected")
                if NORMAL_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    # Set the difficulty level to normal
                    print("Normal difficulty selected")
                if HARD_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    # Set the difficulty level to hard
                    print("Hard difficulty selected")
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(90).render("Galaxy Quest", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Galaxy Quest\Menu-System-PyGame-main/assets/Novi_play_backround.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="White", hovering_color="#d7fcd4")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Galaxy Quest\Menu-System-PyGame-main/assets/Button_Difficulty_Backround.png"), pos=(640, 400), 
                            text_input="DIFFICULTY", font=get_font(75), base_color="White", hovering_color="#d7fcd4")
        QUIT_BUTTON = Button(image=pygame.image.load("Galaxy Quest\Menu-System-PyGame-main/assets/Novi_quit_backround.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="White", hovering_color="#d7fcd4")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()