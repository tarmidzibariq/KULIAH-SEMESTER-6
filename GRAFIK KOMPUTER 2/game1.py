import pygame
from pygame.locals import *
from random import randint

class CEvent:
    def __init__(self):
        pass

    def on_input_focus(self):
        pass

    def on_input_blur(self):
        pass

    def on_key_down(self, event):
        keys=pygame.key.get_pressed()
        if keys[K_LEFT]:
            return 'keKiri'
        elif keys[K_RIGHT]:
            return 'keKanan'
        elif keys[K_UP]:
            return 'keAtas'
        elif keys[K_DOWN]:
            return 'keBawah'
        elif keys[K_q]:
            return 'keluar'
    
    def on_key_up(self, event):
        pass
    def on_mouse_focus(self):
        pass
    def on_mouse_blur(self):
        pass
    def on_mouse_move(self, event):
        pass
    def on_mouse_wheel(self, event):
        pass
    def on_lbutton_up(self, event):
        pass
    def on_lbutton_down(self, event):
        pass
    def on_rbutton_up(self, event):
        pass
    def on_rbutton_down(self, event):
        pass
    def on_mbutton_up(self, event):
        pass
    def on_mbutton_down(self, event):
        pass
    def on_minimize(self):
        pass
    def on_restore(self):
        pass
    def on_resize(self,event):
        pass
    def on_expose(self):
        pass
    def on_exit(self):
        pass
    def on_user(self,event):
        pass
    def on_joy_axis(self,event):
        pass
    def on_joybutton_up(self,event):
        pass
    def on_joybutton_down(self,event):
        pass
    def on_joy_hat(self,event):
        pass
    def on_joy_ball(self,event):
        pass

class App: #aplikasi Game

    def __init__(self):
        self.event = CEvent()
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1024, 768
        self.speed = [5, 5]
        self.black = 0,0,0  
        self.clock = pygame.time.Clock()
        
        #Baca gambar
        self.pacmanR = pygame.image.load("pacman.png")
        self.pacmanL = pygame.image.load("pacmanL.png")
        self.pacmanUp = pygame.image.load("pacmanUp.png")
        self.pacmanDw = pygame.image.load("pacmanDw.png")
        self.apple = pygame.image.load("apple.png")

        #Kotak untuk gambar Pacman
        self.pm_back_rect = pygame.Rect(512,350,50,50) #ukuran 50x50 pixel
        self.pm_back_surf = pygame.Surface((self.pm_back_rect.h, self.pm_back_rect.w))
        self.pm_back_surf.fill(color=(0,0,0))
        self.pm_back_rect_posx = 512
        self.pm_back_rect_posy = 350
        self.pm_back_rect.x = self.pm_back_rect_posx
        self.pm_back_rect.y = self.pm_back_rect_posy

        #Kotak untuk gambar apel
        self.ap_back_rect = pygame.Rect(0,0,50,50) #ukuran 50x50 pixel
        self.ap_back_surf = pygame.Surface((self.pm_back_rect.h, self.pm_back_rect.w))
        self.ap_back_surf.fill(color=(0,0,0))
        self.ap_back_rect_posx = randint(100,950)
        self.ap_back_rect_posy = randint(200,600)
        self.ap_back_rect.x = self.ap_back_rect_posx
        self.ap_back_rect.y = self.ap_back_rect_posy

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.score = 0

        #state gambar yang akan ditampilkan
        self.apple_enable = True
        self.pacmanR_enable = True
        self.pacmanL_enable = False
        self.pacmanUp_enable = False
        self.pacmanDw_enable = False
        self.keyheld_down = False

        #state key yang aktif
        self.key_left = False
        self.key_right = False
        self.key_up = False
        self.key_down = False

    def on_init(self):
        pygame.init()
        self.apple_enable = True
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._apple_surf = self.apple.convert()
        self._pacmanR_surf = self.pacmanR.convert()
        self._pacmanL_surf = self.pacmanL.convert()
        self._pacmanDw_surf = self.pacmanDw.convert()
        self._pacmanUp_surf = self.pacmanUp.convert()
        self._running = True

    def on_event(self, event):
        if event.type == QUIT:
            self.on_exit()
        elif event.type >= USEREVENT:
            self.on_user(event)
 
        elif event.type == VIDEOEXPOSE:
            self.on_expose()
 
        elif event.type == VIDEORESIZE:
            self.on_resize(event)
 
        elif event.type == KEYUP:
            self.event.on_key_up(event)
            self.key_left = False
            self.key_right = False
            self.key_up = False
            self.key_down = False

        elif event.type == KEYDOWN:
            self.keyheld_down = True
            state = self.event.on_key_down(event)
            if (state == 'keKiri'): 
                self.key_left = True
            elif (state == 'keKanan'):
                self.key_right = True
            elif (state == 'keAtas'):
                self.key_up = True
            elif (state == 'keBawah'): 
                self.key_down = True
            elif (state == 'keluar'):
                self.on_exit()
        
        elif event.type == MOUSEMOTION:
            self.event.on_mouse_move(event)
 
        elif event.type == MOUSEBUTTONUP:
            if event.button == 0:
                self.event.on_lbutton_up(event)
            elif event.button == 1:
                self.event.on_mbutton_up(event)
            elif event.button == 2:
                self.event.on_rbutton_up(event)
 
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 0:
                self.event.on_lbutton_down(event)
            elif event.button == 1:
                self.event.on_mbutton_down(event)
            elif event.button == 2:
                self.event.on_rbutton_down(event)
 
        elif event.type == ACTIVEEVENT:
            if event.state == 1:
                if event.gain:
                    self.event.on_mouse_focus()
                else:
                    self.event.on_mouse_blur()
            elif event.state == 2:
                if event.gain:
                    self.event.on_input_focus()
                else:
                    self.event.on_input_blur()
            elif event.state == 4:
                if event.gain:
                    self.on_restore()
                else:
                    self.on_minimize()

    def on_loop(self):
        if self.key_left: #panah kiri
            if (self.pm_back_rect_posx == 30) :
                self.pm_back_rect_posx = 30
                self.key_left = False
            else: self.pm_back_rect_posx -= 1
            self.pacmanR_enable = False
            self.pacmanL_enable = True
            self.pacmanDw_enable = False
            self.pacmanUp_enable = False
        
        elif self.key_right:
            if (self.pm_back_rect_posx == 990) :
                self.pm_back_rect_posx = 990
                self.key_right = False
            else: self.pm_back_rect_posx += 1
            self.pacmanR_enable = True
            self.pacmanL_enable = False
            self.pacmanDw_enable = False
            self.pacmanUp_enable = False
        
        elif self.key_up:
            if (self.pm_back_rect_posy == 60) :
                self.pm_back_rect_posy = 60
                self.key_up = False
            else: self.pm_back_rect_posy -= 1
            self.pacmanR_enable = False
            self.pacmanL_enable = False
            self.pacmanDw_enable = False
            self.pacmanUp_enable = True

        elif self.key_down:
            if (self.pm_back_rect_posy == 680) :
                self.pm_back_rect_posy = 680
                self.key_down = False
            else: self.pm_back_rect_posy += 1
            self.pacmanR_enable = False
            self.pacmanL_enable = False
            self.pacmanDw_enable = True
            self.pacmanUp_enable = False

        if self.pm_back_rect.colliderect(self.ap_back_rect) and self.apple_enable:
            self.apple_enable = False
            self.score += 10
        pass
    def on_expose(self):
        pass

    def on_render(self):
        self._display_surf.fill((0,0,0))
        if (self.apple_enable == False): #apple dimakan via collition
            self.ap_back_rect_posx = randint(100,950)
            self.ap_back_rect_posy = randint(200,600)
            self.ap_back_rect.x = self.ap_back_rect_posx
            self.ap_back_rect.y = self.ap_back_rect_posy
            self.apple_enable = True
        else:
            self.ap_back_rect.x = self.ap_back_rect_posx
            self.ap_back_rect.y = self.ap_back_rect_posy
            self._display_surf.blit(self._apple_surf,(self.ap_back_rect_posx,self.ap_back_rect_posy))
            self._display_surf.blit(self.ap_back_surf,(self.pm_back_rect_posx,self.pm_back_rect_posy))
        self.pm_back_rect.x = self.pm_back_rect_posx
        self.pm_back_rect.y = self.pm_back_rect_posy

        if (self.pacmanR_enable):
            self._display_surf.blit(self._pacmanR_surf,(self.pm_back_rect_posx,self.pm_back_rect_posy))
        elif (self.pacmanL_enable):
            self._display_surf.blit(self._pacmanL_surf,(self.pm_back_rect_posx,self.pm_back_rect_posy))
        elif (self.pacmanUp_enable):
            self._display_surf.blit(self._pacmanUp_surf,(self.pm_back_rect_posx,self.pm_back_rect_posy))
        elif (self.pacmanDw_enable):
            self._display_surf.blit(self._pacmanDw_surf,(self.pm_back_rect_posx,self.pm_back_rect_posy))
        
        self.text_score_surface = self.my_font.render('Skor Kamu = ', False, (255, 255, 255))
        self._display_surf.blit(self.text_score_surface, (600,0))
        self.numeric_score_surface = self.my_font.render(str(self.score), False, (255, 255, 255))
        self._display_surf.blit(self.numeric_score_surface, (800,0))
        self.text_score_surface = self.my_font.render('Tekan \'q\' untuk Keluar Permainan ', False, (255, 255, 255))
        self._display_surf.blit(self.text_score_surface, (550,710))
        
        pygame.display.flip()
    
    def on_cleanup(self):
        pygame.quit()
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
    
    #add on_exit(self) to CApp:
    def on_exit(self):
        self._running = False

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()