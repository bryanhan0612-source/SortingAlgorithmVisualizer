import pygame
import random

pygame.init()

class DrawInformation:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [(128, 128, 128), (160, 160, 160), (192, 192, 192)]

    FONT = pygame.font.SysFont("calibri", 20)
    LARGEFONT = pygame.font.SysFont("calibri", 30)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)
        self.block_width = (self.width - self.SIDE_PAD) // len(lst)
        self.block_height = (self.height - self.TOP_PAD) // (self.max_val - self.min_val or 1)
        self.start_x = self.SIDE_PAD // 2


def generate_list(n, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(n)]


def draw(draw_info, algo_name, ascending, speed):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    title = draw_info.LARGEFONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", True, draw_info.BLACK)

    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))
    controls = draw_info.FONT.render(f"R - Reset | SPACE - Start | A - Ascending | D - Descending | Speed ({speed}ms)", True, draw_info.BLACK)

    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))
    sorting_text = draw_info.FONT.render("B - Bubble Sort | I - Insertion Sort | S - Selection Sort", True, draw_info.BLACK)

    draw_info.window.blit(sorting_text, (draw_info.width / 2 - sorting_text.get_width() / 2, 75))
    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(draw_info.lst):
        x = draw_info.start_x + i * draw_info.block_width
        height = (val - draw_info.min_val) * draw_info.block_height
        y = draw_info.height - height
        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, height))

    if clear_bg:
        pygame.display.update()


def bubble_sort(draw_info, ascending=True, speed=30):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            if (lst[j] > lst[j + 1] and ascending) or (lst[j] < lst[j + 1] and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                pygame.time.delay(speed)
                yield True


def insertion_sort(draw_info, ascending=True, speed=30):
    lst = draw_info.lst
    
    for i in range(1, len(lst)):
        current = lst[i]
        j = i - 1
        while j >= 0 and ((lst[j] > current and ascending) or (lst[j] < current and not ascending)):
            lst[j + 1] = lst[j]
            j -= 1
            lst[j + 1] = current
            draw_list(draw_info, {j + 1: draw_info.GREEN, i: draw_info.RED}, True)
            pygame.time.delay(speed)
            yield True


def selection_sort(draw_info, ascending=True, speed=30):
    lst = draw_info.lst
    
    for i in range(len(lst)):
        min_idx = i
        for j in range(i + 1, len(lst)):
            if (lst[j] < lst[min_idx] and ascending) or (lst[j] > lst[min_idx] and not ascending):
                min_idx = j
            draw_list(draw_info, {i: draw_info.GREEN, min_idx: draw_info.RED}, True)
            pygame.time.delay(speed)
            yield True
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, min_idx: draw_info.RED}, True)
        pygame.time.delay(speed)
        yield True


def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    speed = 30

    lst = generate_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60)
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending, speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending, speed)

            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"

            elif event.key == pygame.K_UP:
                speed = max(1, speed - 5)
            elif event.key == pygame.K_DOWN:
                speed += 5

    pygame.quit()


if __name__ == "__main__":
    main()
