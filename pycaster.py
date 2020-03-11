import math
from os import system
from time import sleep

import click

worldmap = """1111111111111111
1_______11_____1 
1_______11_____1
1______________1
1______________1
1_____11_______1
1_____11_______1
1______________1
1____________111
1______1111____1
1______1111____1
1______________1
1______________1
1______________1
1______________1
1111111111111111"""

wall = '1'
world_list = [list(x) for x in worldmap.split('\n')]


fPlayerX, fPlayerY = 7, 9
fPlayerA = 0.0			# Player Start Rotation
fFOV = 3.14159 / 4.0    # Field of View
fDepth = 16.0			# Maximum rendering distance
fSpeed = 5.0			# Walking Speed

nMapWidth = 16
nMapHeight = 16
nScreenWidth = 120
nScreenHeight = 40


def main():
    fPlayerX, fPlayerY = 7, 9
    fPlayerA = 0.0

    while True:
        sleep(0.2)
        system('clear')
        screen = dict()

        # для каждого "пикселя" по горизонтали
        for x in range(nScreenWidth):

            fRayAngle = (fPlayerA - fFOV/2.0) + (x / nScreenWidth) * fFOV
            fStepSize = 0.5     	 # Increment size for ray casting, decrease to increase
            fDistanceToWall = 0.0    # resolution
            bHitWall = False		 # Set when ray hits wall block

            fEyeX = math.sin(fRayAngle)  # Unit vector for ray in player space
            fEyeY = math.cos(fRayAngle)

            # Пока не достигнет стены
            while (not bHitWall and fDistanceToWall < fDepth):

                fDistanceToWall += fStepSize                        # делаем шаг до стены
                # проверочная ячейка (x)
                nTestX = int(fPlayerX + fEyeX * fDistanceToWall)
                # проверочная ячейка (y)
                nTestY = int(fPlayerY + fEyeY * fDistanceToWall)

                # если проверочная ячейка вышла за границы карты
                # возвращаем максимальную длину
                if (nTestX < 0 or nTestX >= nMapWidth or nTestY < 0 or nTestY >= nMapHeight):
                    bHitWall = True
                    fDistanceToWall = fDepth

                else:
                    # если луч уперся в стену,
                    # собираем координаты этой клетки и расстояние до неё
                    if world_list[nTestX][nTestY] == wall:
                        bHitWall = True

            nCeiling = nScreenHeight/2 - nScreenHeight / fDistanceToWall
            nFloor = nScreenHeight - nCeiling

            # vertical
            for y in range(nScreenHeight):
                if y < nCeiling:
                    pixel = '_'
                elif y > nCeiling and y < nFloor:
                    pixel = '#'
                else:
                    pixel = '_'

                screen[(x, y)] = pixel

        # draw world
        for i in range(40):
            for j in range(120):
                print(screen[(j, i)], end='')
            print()

        print(f'fPlayerX: {fPlayerX}')
        print(f'fPlayerY: {fPlayerY}')
        print(f'fPlayerA: {fPlayerA}')
        print(f'math.sin(fPlayerA): {round(math.sin(fPlayerA))}')
        print(f'math.cos(fPlayerA): {round(math.cos(fPlayerA))}')

        del(screen)

        for i in range(16):
            for j in range(16):
                if i == fPlayerX and j == fPlayerY:
                    print('X', end='')
                    continue
                print(world_list[i][j], end='')
            print()

        # click.echo('Press the key, please ', nl=False)
        c = click.getchar()
        click.echo()
        if c == 'w':
            fPlayerX += round(math.sin(fPlayerA))
            fPlayerY += round(math.cos(fPlayerA))
        elif c == 's':
            fPlayerX -= round(math.sin(fPlayerA))
            fPlayerY -= round(math.cos(fPlayerA))
        elif c == 'a':
            fPlayerA -= 45
            if fPlayerA == -360:
                fPlayerA = 0
        elif c == 'd':
            fPlayerA += 45
            if fPlayerA == 360:
                fPlayerA = 0
        else:
            click.echo('Invalid input :(')
            exit(0)


if __name__ == "__main__":
    main()
