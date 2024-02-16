import os
import sys
import pygame
import requests


class Map(object):
    def __init__(self):
        self.a = 37.530887
        self.b = 55.703118
        self.n = 0.06
        self.type = "map"

    def ll(self):
        return str(self.a) + ',' + str(self.b)

    def update(self, event):
        if self.n < 20 and event.key == pygame.K_PAGEUP:
            self.n += 0.05
        elif self.n > 0.05 and event.key == pygame.K_PAGEDOWN:
            self.n -= 0.05
        
def mapp(x):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&spn={n},{n}&l={type}".format(ll=x.ll(), n=x.n, type=x.type)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    # Запишем полученное изображение в файл.
    map_file = 'map.png'
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file

def main():
    # Инициализируем pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    x = Map()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYUP:
            x.update(event)
        map_file = mapp(x)
        # Рисуем картинку, загружаемую из только что созданного файла.
        screen.blit(pygame.image.load(map_file), (0, 0))
        # Переключаем экран и ждем закрытия окна.
        pygame.display.flip()
    pygame.quit()
    # Удаляем за собой файл с изображением.
    os.remove(map_file)
    
if __name__ == "__main__":
    main()
