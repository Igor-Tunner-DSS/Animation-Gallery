import re
from colors import Colors, display_colors
from os import system
from time import sleep
from threading import Thread, Event



def cut_declaration(string: str) -> list[str]:
    variable_declarations: list = re.split("'", string)
    # [n[0] = , ..., ;n[1] = , ..., ;n[2] = , ...]

    frames: list[str] = []

    for i, line in enumerate(variable_declarations):
        if i % 2 == 0:
            continue

        frames.append(line)

    return frames


def main() -> None:
    print(Colors.END)
    file_txt = open("animations.txt")
    animations: dict = eval(file_txt.read())
    system("cls")
    available_animations: tuple = tuple(animations.keys())
    for i in available_animations:
        print(f"{i:^20}")

    while True:
        chosen_animation = input(f"{Colors.END}\n\nEscolha uma animação:\n >> ")
        if chosen_animation in available_animations:
            break

        else:
            print(f"\033[93m\033[1mErro: valor inválido. Tente novamente\n\033[00m")

    system("cls")

    while True:
        available_colors = dir(Colors)
        display_colors()
        chosen_color: str = input(f"\n\nEscolha uma cor: \n >> ").upper().strip()

        if len(chosen_color.split()) > 1:
            command: list[str] = chosen_color.split()
            chosen_color: str = command[0]
            delay: float = float(command[1])
            variation: str = command[2].lower()

        if chosen_color in available_colors or chosen_color == "DEGRADE":
            break

        else:
            print(f"\033[93m\033[1mErro: valor inválido. Tente novamente\n\033[00m")

    system("cls")
    try:
        frame_rate: int = int(input("Escolha o FPS (padrão = 120):\n >> "))

    except ValueError:
        print(f"\033[93m\033[1mErro: valor inválido. Utilizando o padrão (120)\n\033[00m")
        frame_rate: int = 120
        sleep(1)


    animation = animations[chosen_animation]
    frames: list[str] = cut_declaration(animation)
    if chosen_color != "DEGRADE":
        print(getattr(Colors, chosen_color))

    else:
        run_event = Event()
        run_event.set()
        degrade_thread = Thread(target=cycle_colors, args=(run_event, delay, variation))
        degrade_thread.start()

    # frames_thread = Thread(target=cycle_frames, args=(frame_rate, frames))

    try:
        cycle_frames(frame_rate, frames)

    except KeyboardInterrupt:
        if chosen_color == "DEGRADE":
            run_event.clear()
            degrade_thread.join()

        print(Colors.END)


def cycle_frames(frame_rate: int, frames: list[str]) -> None:
    while True:
        delay: float = 1 / frame_rate
        if frame_rate >= 120:
            delay = 0

        for frame in frames:
            print(frame, '\n >> Aperte Ctrl + C para parar a animação')
            sleep(delay)
            system("cls")


def cycle_colors(run_event: Event, delay: float, variation: str) -> None:
    variations: dict = {
        "blue_shades" : (
            Colors.BLUE,
            Colors.LIGHT_BLUE,
            Colors.CYAN,
            Colors.LIGHT_CYAN
        ),
        "red_shades" : (
            Colors.RED,
            Colors.LIGHT_RED,
            Colors.LIGHT_PURPLE,
            Colors.PURPLE
        ),
        "gold_shades" : (
            Colors.LIGHT_GRAY,
            Colors.YELLOW,
            Colors.BROWN
        )
    }
    variation: tuple = variations[variation]
    current_shade_index: int = 0
    increment: int = 1

    while run_event.is_set():
        print(variation[current_shade_index])
        sleep(delay)
        current_shade_index += increment
        if current_shade_index == len(variation) - 1:
            increment = -1

        elif current_shade_index == 0:
            increment = 1


if __name__ == '__main__':
    main()
