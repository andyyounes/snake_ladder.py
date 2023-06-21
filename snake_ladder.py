import tkinter as tk
import random
import time

# Define the game board and the positions of the snakes and ladders
board_size = 10
snakes = {
    14: 7,
    19: 2,
    34: 12,
    60: 40,
    69: 33,
}
ladders = {
    5: 22,
    11: 36,
    17: 72,
    20: 41,
    40: 60,
    63: 82,
    74: 88,
    80: 99
}

# Create a Tkinter window for the start page
start_window = tk.Tk()
start_window.title("Start Game")

# Create UI components for the start page
num_players_label = tk.Label(start_window, text="Number of Players:")
num_players_label.pack()
num_players_entry = tk.Entry(start_window)
num_players_entry.pack()

name_entries = []
color_entries = []

# Function to start the game
def start_game():
    num_players = int(num_players_entry.get())
    players = []

    for i in range(num_players):
        name = name_entries[i].get()
        color = color_entries[i].get()

        # Exclude players with empty names or colors
        if name and color:
            players.append({"name": name, "color": color, "position": 0})

    # Close the start window
    start_window.destroy()

    # Create a new window for the game
    game_window = tk.Tk()
    game_window.title("Snake-Ladder Game")

    # Create a canvas to draw the game board
    canvas_width = 400
    canvas_height = 400
    canvas = tk.Canvas(game_window, width=canvas_width, height=canvas_height)
    canvas.pack()

    # Draw the game board
    def draw_board():
        cell_width = canvas_width // board_size
        cell_height = canvas_height // board_size

        for i in range(board_size):
            for j in range(board_size):
                x1 = j * cell_width
                y1 = (board_size - 1 - i) * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height

                # Fill the cells with different colors
                if (i + j) % 2 == 0:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="lightgray")
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="white")

                # Draw the cell number
                cell_number = j + (i * board_size) + 1
                canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(cell_number))

    # Draw the snakes on the board
    def draw_snakes():
        for start, end in snakes.items():
            start_row = board_size - 1 - (start // board_size)
            start_col = start % board_size
            end_row = board_size - 1 - (end // board_size)
            end_col = end % board_size

            x1 = start_col * (canvas_width // board_size)
            y1 = start_row * (canvas_height // board_size)
            x2 = end_col * (canvas_width // board_size)
            y2 = end_row * (canvas_height // board_size)

            canvas.create_line(x1, y1, x2, y2, fill="red", width=3)
            canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="Snake")

    # Draw the ladders on the board
    def draw_ladders():
        for start, end in ladders.items():
            start_row = board_size - 1 - (start // board_size)
            start_col = start % board_size
            end_row = board_size - 1 - (end // board_size)
            end_col = end % board_size

            x1 = start_col * (canvas_width // board_size)
            y1 = start_row * (canvas_height // board_size)
            x2 = end_col * (canvas_width // board_size)
            y2 = end_row * (canvas_height // board_size)

            canvas.create_line(x1, y1, x2, y2, fill="blue", width=3)
            canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="Ladder")

    # Draw the players' positions on the board
    def draw_players():
        for player in players:
            position = player["position"]
            color = player["color"]
            cell_width = canvas_width // board_size
            cell_height = canvas_height // board_size

            # Calculate the row and column of the current position
            row = board_size - 1 - (position // board_size)
            col = position % board_size

            # Calculate the coordinates of the cell
            x1 = col * cell_width
            y1 = row * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height

            # Draw the player's dot on the board
            canvas.create_oval(x1 + cell_width // 4, y1 + cell_height // 4, x2 - cell_width // 4, y2 - cell_height // 4,
                               fill=color, tags="player")

    # Roll the dice and move the players
    def roll_dice():
        total_moves = 0
        estimated_time = (board_size * board_size) * num_players * 0.5  # Estimated time calculation
        print("Estimated Time: {:.2f} seconds".format(estimated_time))
        while True:
            for player in players:
                dice_value = random.randint(1, 6)
                print("{} rolled dice: {}".format(player["name"], dice_value))
                total_moves += 1

                for _ in range(dice_value):
                    player["position"] += 1

                    if player["position"] in snakes:
                        player["position"] = snakes[player["position"]]

                    if player["position"] in ladders:
                        player["position"] = ladders[player["position"]]

                    if player["position"] >= board_size * board_size:
                        player["position"] = board_size * board_size - 1

                    canvas.delete("player")
                    draw_players()
                    game_window.update()
                    game_window.after(500)

                    if player["position"] == board_size * board_size - 1:
                        print("{} won!".format(player["name"]))
                        winner_label.config(text="{} won!".format(player["name"]))
                        roll_button.config(state=tk.DISABLED)
                        break

                if player["position"] == board_size * board_size - 1:
                    break

            if player["position"] == board_size * board_size - 1:
                break

        # Calculate the actual time taken to finish the game
        end_time = time.time()
        actual_time = end_time - start_time

        # Display the actual time
        actual_time_label.config(text="Actual Time: {:.2f} seconds".format(actual_time))

    # Create UI components for the game page
    draw_board()
    draw_snakes()
    draw_ladders()
    draw_players()

    roll_button = tk.Button(game_window, text="Roll Dice", command=roll_dice)
    roll_button.pack()

    winner_label = tk.Label(game_window, text="")
    winner_label.pack()

    actual_time_label = tk.Label(game_window, text="")
    actual_time_label.pack()

    # Start the timer
    start_time = time.time()

    # Start the Tkinter event loop
    game_window.mainloop()


# Function to add player fields dynamically
def add_player():
    name_label = tk.Label(start_window, text="Player Name:")
    name_label.pack()
    name_entry = tk.Entry(start_window)
    name_entry.pack()
    name_entries.append(name_entry)

    color_label = tk.Label(start_window, text="Player Color:")
    color_label.pack()
    color_entry = tk.Entry(start_window)
    color_entry.pack()
    color_entries.append(color_entry)


# Create UI components for the start page
add_player_button = tk.Button(start_window, text="Add Player", command=add_player)
add_player_button.pack()

start_button = tk.Button(start_window, text="Start Game", command=start_game)
start_button.pack()

# Start the Tkinter event loop
start_window.mainloop()

