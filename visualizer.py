import pygame
import random
import math
from heapq import heappush, heappop
pygame.init()


class DrawInformation:
    black = 0, 0, 0
    white = 255, 255, 255
    green = 0, 255, 0
    red = 255, 0, 0
    grey = 128, 128, 128
    BACKGROUND_COLOR = white

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont("comicsans", 20)
    LARGE_FONT = pygame.font.SysFont("comicsans", 30)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1,
                                        draw_info.black)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1,
                                     draw_info.black)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width() / 2, 45))

    sorting = draw_info.FONT.render("I - Insert Sort | B - Bubble Sort | S - Selection Sort | Z - Bogo Sort", 1,
                                    draw_info.black)
    sorting2 = draw_info.FONT.render(" M - Merge Sort | Q - Quick Sort", 1, draw_info.black)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 70))
    draw_info.window.blit(sorting2, (draw_info.width / 2 - sorting.get_width() / 2, 95))
    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width-draw_info.SIDE_PAD, draw_info.height -
                      draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.green, j + 1: draw_info.red}, True)
                yield True

    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i-1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.green, i: draw_info.red}, True)
            yield True

    return lst


def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(0, len(lst) - 1):
        cur_min_idx = i
        for j in range(i +1, len(lst)):

            if ascending == True:
                if lst[j] < lst[cur_min_idx]:
                    cur_min_idx = j

            elif ascending == False:
                if lst[j] > lst[cur_min_idx]:
                    cur_min_idx = j

        lst[i], lst[cur_min_idx] = lst[cur_min_idx], lst[i]
        draw_list(draw_info, {i: draw_info.green, cur_min_idx: draw_info.red}, True)
        yield True


def merge_sort(draw_info, ascending=True):

    lst = draw_info.lst

    def merge_rec(start, end):

        if end - start > 1:

            mid = (start+end) // 2
            yield from merge_rec(start, mid)

            yield from merge_rec(mid, end)
            
            left_lst = lst[start: mid]
            right_lst = lst[mid: end]

            i = 0
            j = 0
            k = start

            while i < len(left_lst) and j < len(right_lst):

                if (left_lst[i] < right_lst[j] and ascending == True) or (left_lst[i] > right_lst[j] and not ascending):

                    lst[k] = left_lst[i]
                    i += 1
                    draw_list(draw_info, {i: draw_info.green, k: draw_info.red}, True)

                else:
                    lst[k] = right_lst[j]
                    j += 1
                k += 1
                draw_list(draw_info, {i: draw_info.green, j: draw_info.red}, True)

            while i < len(left_lst):
                lst[k] = left_lst[i]
                i += 1
                k += 1
                draw_list(draw_info, {i: draw_info.green, k: draw_info.red}, True)

            while j < len(right_lst):
                lst[k] = right_lst[j]
                j += 1
                k += 1
                draw_list(draw_info, {j: draw_info.green, k: draw_info.red}, True)

            yield True
    yield from merge_rec(0, len(lst))


def bogo_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def is_sorted(lst):
        n = len(lst)

        for i in range(0, n-1):
            if ascending == True and lst[i] > lst[i + 1] or lst[i] < lst[i + 1] and not ascending:

                return False

        return True

    while is_sorted(lst) == False:

        def shuffle(lst):
            n = len(lst)

            for i in range(0, n):
                j = random.randint(0, n - 1)
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {j: draw_info.green, i: draw_info.red}, True)
        shuffle(lst)
    yield True


def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def partition(lst, low, high):
        i = (low - 1)

        pivot = lst[high]

        for j in range(low, high):

            if (lst[j] <= pivot and ascending == True) or (lst[j] >= pivot and ascending == False):

                i = i + 1
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {j: draw_info.green, i: draw_info.red}, True)

        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        draw_list(draw_info, {high: draw_info.green, i: draw_info.red}, True)

        return i + 1

    def quick_sort_rec(lst, low, high):
        if len(lst) == 1:
            return lst
        if low < high:

            pi = partition(lst, low, high)

            yield from quick_sort_rec(lst, low, pi-1)

            yield from quick_sort_rec(lst, pi+1, high)

    yield from quick_sort_rec(lst, 0, len(lst)-1)


def heap_sort(draw_info):
    h = []
    lst = draw_info.lst
    for i in range(1, len(lst)):
        heappush(h, i)
    lst.clear()
    for j in range(len(h)):
        lst.append(heappop(h))

    return lst


def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 50

    lst = generate_starting_list(n, min_val, max_val)

    draw_info = DrawInformation(800, 600, lst)

    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(30)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insert Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algo_name = "Merge sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection sort"
            elif event.key == pygame.K_z and not sorting:
                sorting_algorithm = bogo_sort
                sorting_algo_name = "Bogo Sort"
    pygame.quit()


if __name__ == "__main__":
    main()
