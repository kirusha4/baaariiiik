from pygame import *

'''Необходимые классы'''

#класс-родитель для спрайтов 
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed, wight, height): # добавить еще два параметра при создании и задавать размер прямоугольгника для картинки самим
        #подключаем конструктор суперкласса
        super().__init__()

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (wight, height)) # вместе 55,55 - параметры
        #у каждого спрайта есть своя скорость - количество пикселей, на которое он перемещается при движении
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        #каждый спрайт должен иметь координаты своего rect - x(по горизонтали) и y(по вертикали)
        self.rect.x = player_x
        self.rect.y = player_y

        #функция отображения спрайта на экране в конкретных координатах
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
#функции, позволяющие спрайтам-игрокам перемещаться с помощью кнопок
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

#Игровая сцена:
back = (200, 255, 255) # цвет фона (background)
#ширина окна
win_width = 600
#высота окна
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)

#флаги отвечающие за состояние игры
game = True
finish = False
clock = time.Clock()
FPS = 60

#создания мяча и ракетки    
racket1 = Player('racket.png', 30, 200, 4, 50, 150) # при созданни спрайта добавляется еще два параметра
racket2 = Player('racket.png', 520, 200, 4, 50, 150)
ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)

font.init()
font = font.Font(None, 35)
lose1 = font.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font.render('PLAYER 2 LOSE!', True, (180, 0, 0))

speed_x = 3
speed_y = 3

#игровой цикл
while game:
#кнопка выхода из игры
    for e in event.get():
        if e.type == QUIT:
            game = False

#вводим все функции и условия движения спрайтов в цикл
    if finish != True:
        window.fill(back)
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        #последствия столкновений спрайтов мяча и ракеток
        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
        #перемена направления движения мяча
            speed_x *= -1
            speed_y *= 1

        # если мяч достигает границ экрана меняем направление его движения
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1

        # если мяч улетел дальше ракетки, выводим условие проигрыша для первого игрока
        if ball.rect.x < 0:
            finish = True
            window.blit(lose1, (200, 200))
            game_over = True

        # если мяч улетел дальше ракетки, выводим условие проигрыша для второго игрока
        if ball.rect.x > win_width:
            finish = True
            window.blit(lose2, (200, 200))
            game_over = True
        #функции отображения спрайтов
        racket1.reset()
        racket2.reset()
        ball.reset()

#обновление экрана
    display.update()
    clock.tick(FPS)