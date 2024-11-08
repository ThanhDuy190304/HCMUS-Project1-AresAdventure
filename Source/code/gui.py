import tkinter as tk
from tkinter import font, messagebox
from .bfs import *
from .dfs import *
from .astar import *
from .ucs import *
from .support import *
import os
from PIL import Image, ImageTk

current_level = 1
algorithms = ["Breadth-First Search", "Depth-First Search", "Uniform Cost Search", "A* Search with heuristic"]
current_algorithm_index = 0
is_algorithm_running = False

def save_result_to_file(output_file, result, algorithm_name):
    algorithm_short_name = {
        "Breadth-First Search": "BFS",
        "Depth-First Search": "DFS",
        "Uniform Cost Search": "UCS",
        "A* Search with heuristic": "A*"
    }
    short_name = algorithm_short_name.get(algorithm_name, algorithm_name)
    num_checked_states, final_node, total_time, memory_usage = result
    # Convert actions to a concatenated string
    actions_str = ''.join(final_node.actions)
    with open(output_file, "a") as f:
        f.write(f"{short_name}\n")
        f.write(f"Steps: {len(final_node.actions)}, Weight: {final_node.total_weight}, Node: {num_checked_states}, Time (ms): {total_time * 1000:.2f}, Memory (MB): {memory_usage / (1024 ** 2):.4f}\n")
        f.write(f"{actions_str}\n")  # Newline after each algorithm output


    
# Run the selected algorithm    
def run_algorithm(game, result_path, algorithm_name,result_window):

    global is_algorithm_running
    is_algorithm_running = True
    run_button.config(state=tk.DISABLED)

     # Check if result window is open or create a new one
    if result_window is None or not result_window.winfo_exists():
        result_window = tk.Toplevel(root)
        result_window.title("RESULT")
        result_window.geometry("400x200+820+300")
        result_window.configure(bg="black")
    # Select the algorithm to run based on user choice
    if algorithm_name == "Breadth-First Search":
        result = BFS(game)
    elif algorithm_name == "Depth-First Search":
        result = DFS(game)
    elif algorithm_name == "Uniform Cost Search":
        result = UCS(game)
    elif algorithm_name == "A* Search with heuristic":
        result = AStar(game)
    else:
        messagebox.showerror("Lỗi", f"Thuật toán '{algorithm_name}' không được hỗ trợ.")
        return
    # Display the result if it exists
    if result:
        num_checked_states, final_node, total_time, memory_usage = result
        result_text = (
            f"Algorithm: {algorithm_name}\n"
            f"Shorted path: {''.join(final_node.actions)}\n"
            f"Total weight: {final_node.total_weight}\n"
            f"Steps: {len(final_node.actions)}\n"
            f"Time: {total_time*1000:.2f} ms\n"
            f"Memory: {memory_usage / (1024 ** 2):.4f} MB\n"
            f"Node generated: {num_checked_states}"
        )

        # Clear previous result display
        for widget in result_window.winfo_children():
            widget.destroy()

        result_label = tk.Label(result_window, text=result_text, font=("Helvetica", 12), fg="white", bg="black", justify="left", wraplength=350)
        result_label.pack(pady=10, padx=20)
        save_result_to_file(result_path, result, algorithm_name)
        animate_movement_with_push(game, final_node.actions)
        root.after(int(total_time * 1000) + 1000, lambda: run_button.config(state=tk.NORMAL))
    else:
        is_algorithm_running = False
        run_button.config(state=tk.NORMAL)
        status_label.config(text="Process has no result",font="bold", fg="purple")
        return
    is_algorithm_running = False
    status_label.config(text="Process completed", font="bold", fg="green")
    
# Animate the movements of the solution
def animate_movement_with_push(game: Sokoban, path):
    grid, player_pos, stones_map, shortest_path = game.board, game.playerPos, game.stone_map, path
    player_x, player_y = player_pos
    step_index = 0
    grid_size = 40

    canvas.update()
    max_row_length = max(len(row) for row in grid) 
    map_width = max_row_length * grid_size
    map_height = len(grid) * grid_size
    start_x = (canvas.winfo_width() - map_width) // 2
    start_y = (canvas.winfo_height() - map_height) // 2

    goal_positions = set((x, y) for x, y in [(i, j) for i, row in enumerate(grid) for j, val in enumerate(row) if val == '.'or val =='*' or val=='+'])
    # Function to determine the next position based on the direction
    def get_next_position(x, y, direction):
        if direction in ('u', 'U'):
            return x - 1, y
        elif direction in ('d', 'D'):
            return x + 1, y
        elif direction in ('l', 'L'):
            return x, y - 1
        elif direction in ('r', 'R'):
            return x, y + 1
        return x, y
    # Perform each step of the movement animation
    def perform_step():
        global is_algorithm_running
        nonlocal player_x, player_y, step_index, stones_map
        if step_index >= len(shortest_path):
            # If all steps are completed, stop the animation and enable the run button
            is_algorithm_running = False
            run_button.config(state=tk.NORMAL)
            status_label.config(text="Process completed",font="bold", fg="green")
            return

        # Get the next move in the path
        move = shortest_path[step_index]
        x0, y0 = start_x + player_y * grid_size, start_y + player_x * grid_size
        x1, y1 = x0 + grid_size, y0 + grid_size

        # Check if the player is on a goal position and display the appropriate image
        if (player_x, player_y) in goal_positions:
            canvas.create_image(x0 + grid_size // 2, y0 + grid_size // 2, image=goal_img)
        else:
            canvas.create_image(x0 + grid_size // 2, y0 + grid_size // 2, image=ground_img)

        next_player_x, next_player_y = get_next_position(player_x, player_y, move)

        # If the move is uppercase, it means pushing a box
        if move.isupper():
            next_box_x, next_box_y = get_next_position(next_player_x, next_player_y, move)
            current_box_pos = (next_player_x, next_player_y)

            # Check if there is a stone at the current box position
            if current_box_pos in stones_map:
                stone_weight = stones_map[current_box_pos]
                del stones_map[current_box_pos]
                stones_map[(next_box_x, next_box_y)] = stone_weight
                # Display the appropriate image for the current and next box positions
                if current_box_pos in goal_positions:
                    canvas.create_image((current_box_pos[1] * grid_size) + start_x + grid_size // 2,
                                        (current_box_pos[0] * grid_size) + start_y + grid_size // 2, image=goal_img)
                else:
                    canvas.create_image((current_box_pos[1] * grid_size) + start_x + grid_size // 2,
                                        (current_box_pos[0] * grid_size) + start_y + grid_size // 2, image=ground_img)

                if (next_box_x, next_box_y) in goal_positions:
                    canvas.create_image((next_box_y * grid_size) + start_x + grid_size // 2,
                                        (next_box_x * grid_size) + start_y + grid_size // 2, image=stone_on_goal_img)
                else:
                    canvas.create_image((next_box_y * grid_size) + start_x + grid_size // 2,
                                        (next_box_x * grid_size) + start_y + grid_size // 2, image=box_img, tags="stone")
                # Display the weight of the stone
                canvas.create_text(
                    (next_box_y * grid_size) + start_x + grid_size // 2,
                    (next_box_x * grid_size) + start_y + grid_size // 2,
                    text=str(stone_weight),
                    font=("Arial", 14, "bold"),
                    fill="brown"
                )
        # Update the player position
        player_x, player_y = next_player_x, next_player_y
        canvas.create_image((player_y * grid_size) + start_x + grid_size // 2,
                            (player_x * grid_size) + start_y + grid_size // 2, image=player_img, tags="player")
        # Move to the next step in the path
        step_index += 1
        root.after(100, perform_step)

    perform_step()


def start_algorithm():
    global is_algorithm_running
    is_algorithm_running = True
    run_button.config(state=tk.DISABLED)
    if is_algorithm_running:
        status_label.config(text="Process is running",font="bold", fg="red")
        
    load_level(current_level) # Load the current level
    root.after(1000, load_and_run_algorithm) # Delay and start the algorithm


def load_and_run_algorithm():
    global current_level
    input_path = f"./input/input-{str(current_level).zfill(2)}.txt"
    output_path = f"./output/output-{str(current_level).zfill(2)}.txt"
    if not os.path.isfile(input_path):
        messagebox.showerror("Lỗi", f"Tệp đầu vào {input_path} không tồn tại.")
        return
    # Read game configuration from input file
    grid, stones, stone_weights, switches, player_position = read_maze_file(input_path)
    check_points = find_list_check_point(grid)
    boxes_data = find_boxes_position(grid, stone_weights)
    game = Sokoban(grid, check_points, boxes_data)

    selected_algorithm = algorithms[current_algorithm_index]
    run_algorithm(game, output_path, selected_algorithm,result_window)

def load_level(level):
    global current_level, current_grid, current_stones_map,background_img_id
    current_level = level
    input_path = f"./input/input-{str(level).zfill(2)}.txt"

    if not os.path.isfile(input_path):
        messagebox.showerror("Lỗi", f"Tệp đầu vào {input_path} không tồn tại.")
        return
    
    # Initialize the grid and stones map
    grid = []
    stones_map = {}

    with open(input_path, "r", encoding="utf-8") as fi:
        weights_line = fi.readline().strip()
        stone_weights = list(map(int, weights_line.split()))

        stone_index = 0
        for i, line in enumerate(fi):
            row = list(line.rstrip('\n'))
            for j, char in enumerate(row):
                if char == '$' or char =='*':
                    stones_map[(i, j)] = stone_weights[stone_index]
                    stone_index += 1
            grid.append(row)

    current_grid = grid
    current_stones_map = stones_map
    level_label.config(text=f"Lv.{level}")
    display_map(current_grid, current_stones_map)

def display_map(grid, stones_map):
    
    grid_size = 40
    
    max_row_length = max(len(row) for row in grid) 
    map_width = max_row_length * grid_size
    map_height = len(grid) * grid_size
    canvas.config(width=max(600, map_width), height=max(500, map_height), bg="white")
    canvas.update()

    start_x = (canvas.winfo_width() - map_width) // 2
    start_y = (canvas.winfo_height() - map_height) // 2

    for i, row in enumerate(grid):
        first_wall_index = next((j for j, char in enumerate(row) if char == '#'), None)
        if first_wall_index is None:
            continue
        for j, char in enumerate(row[first_wall_index:], start=first_wall_index):
            x_center = start_x + (j) * grid_size + grid_size // 2
            y_center = start_y + i * grid_size + grid_size // 2

            if char == '#':
                canvas.create_image(x_center, y_center, image=wall_img)
            elif char == '@':
                canvas.create_image(x_center, y_center, image=player_img, tags="player")
            elif char == '.':
                canvas.create_image(x_center, y_center, image=goal_img)
            elif char == '+':
                canvas.create_image(x_center, y_center, image=player_on_goal_img)
            elif char == '*':
                canvas.create_image(x_center, y_center, image=stone_on_goal_img)
            else:
                canvas.create_image(x_center, y_center, image=ground_img)

    goal_positions = set((i, j) for i, row in enumerate(grid) for j, val in enumerate(row) if val in ['.', '*', '+'])
    for (stone_x, stone_y), weight in stones_map.items():
        row = grid[stone_x]
        first_wall_index = next((j for j, char in enumerate(row) if char == '#'), 0)
        x_center = start_x + first_wall_index * grid_size + (stone_y - first_wall_index) * grid_size + grid_size // 2
        y_center = start_y + stone_x * grid_size + grid_size // 2

        if (stone_x, stone_y) in goal_positions:
            canvas.create_image(x_center, y_center, image=stone_on_goal_img)
        else:
            canvas.create_image(x_center, y_center, image=box_img, tags="stone")

        canvas.create_text(
            x_center,
            y_center,
            text=str(weight),
            font=("Arial", 14, "bold"),
            fill="brown"
        )

def change_level(direction):
    global current_level
    if direction == "Right":
        current_level = current_level + 1 if current_level < 10 else 1
    elif direction == "Left":
        current_level = current_level - 1 if current_level > 1 else 10
    canvas.delete("all")
    background_img_id = canvas.create_image(0, 0, image=bg_image, anchor='nw')
    load_level(current_level)
    status_label.config(text="")

# Switch algorithms when the spacebar is pressed
def switch_algorithm(event):
    global current_algorithm_index
    current_algorithm_index = (current_algorithm_index + 1) % len(algorithms)
    algorithm_label.config(text=algorithms[current_algorithm_index])

# Initialize the main map and UI components
def map_init():
    global root, current_level, algorithms, current_algorithm_index, canvas, result_window
    current_level = 1
    algorithms = ["Breadth-First Search", "Depth-First Search", "Uniform Cost Search", "A* Search with heuristic"]
    current_algorithm_index = 0

    root = tk.Tk()
    root.title("ARES'S ADVENTURE")
    root.geometry("800x720+0+0")
    root.configure(bg="black")

    global result_window
    result_window = None

    # Create a separate window for results
    result_window = tk.Toplevel(root)
    result_window.title("RESULT")
    result_window.geometry("400x200+820+300")
    result_window.configure(bg="black")
    result_window.lift()
    result_window.attributes("-topmost", True)

    # Load images
    global player_img, box_img, goal_img, wall_img, original_img, run_img, player_on_goal_img, stone_on_goal_img, ground_img, bg_image
    background_img = Image.open("./img/anh6.webp")
    background_img = background_img.resize((800, 720), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(background_img)

    player_img = tk.PhotoImage(file="./img/anh1.png")
    box_img = tk.PhotoImage(file="./img/anh2.png")
    goal_img = tk.PhotoImage(file="./img/anh3.png")
    wall_img = tk.PhotoImage(file="./img/anh4.png")
    original_img = Image.open("./img/anh5.png")
    run_img = ImageTk.PhotoImage(original_img)
    player_on_goal_img = tk.PhotoImage(file="./img/anh7.png")
    stone_on_goal_img = ImageTk.PhotoImage(file="./img/anh8.png")
    ground_img = tk.PhotoImage(file="./img/anh9.png")

    # Configure widgets
    background_label = tk.Label(root, image=bg_image)
    background_label.place(relwidth=1, relheight=1)

    title_font = font.Font(family="Helvetica", size=20, weight="bold")
    subtitle_font = font.Font(family="Helvetica", size=10)

    title_label = tk.Label(root, text="ARES'S ADVENTURE", font=title_font, fg="white", bg="black")
    title_label.pack(pady=5)

    subtitle_label = tk.Label(root, text="Now, select your map!!!", font=subtitle_font, fg="white", bg="black")
    subtitle_label.pack(pady=5)

    # Navigation for levels
    level_frame = tk.Frame(root, bg="black")
    level_frame.pack(pady=10)
    prev_button = tk.Button(level_frame, text="<", font=subtitle_font, command=lambda: change_level("Left"))
    prev_button.grid(row=0, column=0)
    global level_label
    level_label = tk.Label(level_frame, text=f"Lv.{current_level}", font=title_font, fg="white", bg="black")
    level_label.grid(row=0, column=1, padx=5)
    next_button = tk.Button(level_frame, text=">", font=subtitle_font, command=lambda: change_level("Right"))
    next_button.grid(row=0, column=2)

    # Frame for algorithm selection
    algorithm_frame = tk.LabelFrame(root, text="Press Space to Select Algorithm", font=("Helvetica", 14, "bold"), fg="white", bg="black", bd=4, labelanchor="n")
    algorithm_frame.pack(pady=10)

    global algorithm_label
    algorithm_label = tk.Label(algorithm_frame, text=algorithms[current_algorithm_index], font=("Helvetica", 16, "bold"), fg="white", bg="black")
    algorithm_label.pack(padx=5, pady=5)

    global status_label
    status_label = tk.Label(root, text="", font=("Helvetica", 12), fg="white", bg="black", justify="left")
    status_label.pack(pady=10)

    global run_button
    run_button = tk.Button(root, image=run_img, command=start_algorithm)
    run_button.pack(pady=10)

    canvas = tk.Canvas(root, width=400, height=350, bg="grey")
    canvas.pack(pady=10)
    canvas.create_image(0, 0, image=bg_image, anchor='nw')

    result_label = tk.Label(root, text="", font=("Helvetica", 12), fg="white", bg="black", justify="left")
    result_label.pack(pady=10)

    root.bind("<Right>", lambda event: change_level("Right"))
    root.bind("<Left>", lambda event: change_level("Left"))
    root.bind("<space>", switch_algorithm)

    load_level(current_level)

    root.mainloop()