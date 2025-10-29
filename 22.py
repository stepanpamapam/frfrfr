import tkinter as tk
import math

def draw_recursive_circles(canvas, x, y, radius, depth):
    if depth == 0 or radius < 5:
        return
    
    # Рисуем текущий круг
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline="black", width=2)
    
    if depth > 1:
        # Радиус дочерних кругов (меньше родительского)
        child_radius = radius * 0.4
        
        # Расстояние от центра родителя до центров детей
        # Располагаем по бокам внутри большого круга
        distance = radius - child_radius - 5  # -5 для отступа от края
        
        # Координаты для левого и правого дочерних кругов
        left_x = x - distance
        right_x = x + distance
        
        # Рекурсивно рисуем дочерние круги
        draw_recursive_circles(canvas, left_x, y, child_radius, depth - 1)
        draw_recursive_circles(canvas, right_x, y, child_radius, depth - 1)

# Создаем окно
root = tk.Tk()
root.title("Рекурсивные круги в круге - Задание 12")
canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Запускаем отрисовку из центра
draw_recursive_circles(canvas, 400, 300, 200, 4)

root.mainloop()
