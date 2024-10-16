import pygame
import random
import sys
#import requests

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

# Display dimensions
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))

# Title and Clock
pygame.display.set_caption("Snake Game - Levels")
clock = pygame.time.Clock()

# Snake properties
snake_block = 10
snake_speed = 5

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)

def play_background_music():
    pygame.mixer.music.load('bg_music_1.mp3')  # Load your music file
    pygame.mixer.music.play(-1)  # Play the music indefinitely (-1 means loop)

# Score function
def score_display(score):
    value = font_style.render("Score: " + str(score), True, WHITE)
    dis.blit(value, [dis_width - 150, 10])  # Position score on the right


# Snake function
def create_snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], block, block])


# Message display function
def message(msg, color, position=None):
    mesg = font_style.render(msg, True, color)
    if position:
        dis.blit(mesg, position)
    else:
        dis.blit(mesg, [dis_width / 6, dis_height / 3])


# Generate arithmetic questions and answers
def generate_question(difficulty):
    if difficulty == 'easy':
        num1 = random.randint(1, 9)
        num2 = random.randint(1, 9)
    elif difficulty == 'medium':
        num1 = random.randint(10, 99)
        num2 = random.randint(10, 99)
    else:  # hard
        num1 = random.randint(100, 999)
        num2 = random.randint(100, 999)

    operators = ['+', '-', '*']
    operator = random.choice(operators)

    question = f"{num1} {operator} {num2}"
    correct_answer = eval(question)

    answers = [correct_answer] + [random.randint(correct_answer - 10, correct_answer + 10) for _ in range(3)]
    random.shuffle(answers)

    return question, correct_answer, answers

#To send updated score in flask
# def update_score_in_flask(username, score):
#     try:
#         response = requests.post('http://127.0.0.1:5000/update_score', json={'score': score})
#         print(response.text)
#     except requests.exceptions.RequestException as e:
#         print(f"Error sending score to Flask: {e}")

# Level 1 game loop with three sub-levels (Easy, Medium, Hard)
def game_loop_level_1():
    game_over = False
    game_close = False

    # Snake initial position and movement variables
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    snake_speed = 15

    score = 0

    sub_level = 'easy'  # Start at easy
    target_scores = {'easy': 50, 'medium': 100, 'hard': 150}

    question, correct_answer, answers = generate_question(sub_level)

    # Adjust food positions generation to ensure they are scattered within the window
    food_positions = []

    def place_food():
        nonlocal food_positions
        food_positions = []
        buffer = 50  # Ensures food is not too close to the window edges

        for _ in range(4):  # Create 4 answer positions
            food_x = random.randint(buffer, dis_width - buffer - snake_block) // 10 * 10
            food_y = random.randint(buffer, dis_height - buffer - snake_block) // 10 * 10
            food_positions.append([food_x, food_y])

    place_food()

    while not game_over:
        while game_close:
            dis.fill(BLACK)
            message("You Lost! Press Enter to Restart", RED)
            pygame.display.update()

            # Send the final score when the game ends
            # final_score = score  # Replace 'score' with the final score variable
            # update_score_in_flask(session['username'], final_score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop_level_1()  # Restart Level 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)

        # Display the question and possible answers
        message(f"Question: {question}", WHITE, [10, 10])

        # Draw food for each answer
        for i, pos in enumerate(food_positions):
            pygame.draw.rect(dis, RED, [pos[0], pos[1], snake_block, snake_block])
            answer_text = font_style.render(str(answers[i]), True, WHITE)
            dis.blit(answer_text, [pos[0], pos[1]])

        # Draw the snake
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        create_snake(snake_block, snake_list)
        score_display(score)
        pygame.display.update()

        # Check if snake eats correct or wrong food
        for i, pos in enumerate(food_positions):
            if x1 == pos[0] and y1 == pos[1]:
                if answers[i] == correct_answer:
                    length_of_snake += 1
                    score += 10
                else:
                    game_close = True

                # Generate a new question and answers
                question, correct_answer, answers = generate_question(sub_level)
                place_food()  # Reposition food after eating
                break

        # Sub-level progression logic
        if score >= target_scores['easy'] and sub_level == 'easy':
            sub_level = 'medium'
            message("Moving to Medium Level...", GREEN)
            pygame.display.update()
            pygame.time.delay(2000)
            question, correct_answer, answers = generate_question(sub_level)
            place_food()  # Generate new food
        elif score >= target_scores['medium'] and sub_level == 'medium':
            sub_level = 'hard'
            message("Moving to Hard Level...", GREEN)
            pygame.display.update()
            pygame.time.delay(2000)
            question, correct_answer, answers = generate_question(sub_level)
            place_food()  # Generate new food
        elif score >= target_scores['hard'] and sub_level == 'hard':
            message("Level 1 Complete! Moving to Level 2...", GREEN, [dis_width / 6, dis_height / 3])
            message("Instruction for Level 2: Make the snake eat numbers to sum up to 100 in 120 secs", RED,
                    [dis_width / 6, dis_height / 3 + 60])
            message("sum up to 100 in 120 secs", RED,
                    [dis_width / 6, dis_height / 3 + 90])
            pygame.display.update()
            pygame.time.delay(2000)
            game_loop_level_2()

        clock.tick(snake_speed)


# Game loop for Level 2 (already implemented)
def game_loop_level_2():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    snake_speed = 15
    total_score = 0

    start_time = pygame.time.get_ticks()

    food_positions = []

    def place_food():
        nonlocal food_positions
        food_positions = []
        for _ in range(5):
            food_num = random.randint(1, 20)
            food_positions.append([random.randrange(0, dis_width - snake_block, 10),
                                   random.randrange(0, dis_height - snake_block, 10), food_num])

    place_food()

    while not game_over:
        while game_close:
            dis.fill(BLACK)
            message("Game Over! Press Enter to Restart", RED)
            pygame.display.update()

            # Send the final score when the game ends
            # final_score = total_score  # Replace 'total_score' with the final score variable
            # update_score_in_flask(session['username'], final_score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop_level_1()  # Restart level

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        x1 += x1_change
        y1 += y1_change

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        dis.fill(BLACK)

        current_time = pygame.time.get_ticks()
        time_left = 120 - (current_time - start_time) / 1000
        if time_left <= 0:
            game_close = True

        for pos in food_positions:
            pygame.draw.rect(dis, RED, [pos[0], pos[1], snake_block, snake_block])
            answer_text = font_style.render(str(pos[2]), True, WHITE)
            dis.blit(answer_text, [pos[0], pos[1]])

        score_display(total_score)
        timer_display = font_style.render(f"Time left: {int(time_left)} sec", True, WHITE)
        dis.blit(timer_display, [dis_width - 150, 0])

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        create_snake(snake_block, snake_list)
        pygame.display.update()

        for pos in food_positions:
            if x1 == pos[0] and y1 == pos[1]:
                length_of_snake += 1
                total_score += pos[2]
                place_food()

        if total_score >= 100:
            message("Level 2 Completed! You Win!", GREEN)
            pygame.display.update()
            pygame.time.delay(2000)
            return  # End the game or proceed to next logic

        clock.tick(snake_speed)
        # You can reuse your current Level 2 logic here
    pass

def show_start_screen():
    dis.fill(BLACK)  # Clear the display
    message("Answer to the displayed questions by eating", WHITE, [dis_width / 3, dis_height / 3])  # Centered message
    message("the correct answers.", WHITE, [dis_width / 3, dis_height / 3 + 30])
    message("Two Levels 'LEVEL 1' 'LEVEL 2'", RED, [dis_width / 3, dis_height / 3 + 60])
    message("LEVEL 1 has three sub-levels", GREEN, [dis_width / 3, dis_height / 3 + 90])
    message("'EASY' 'MEDIUM' 'HARD'", WHITE, [dis_width / 3, dis_height / 3 + 120])
    message("Completing all the sub-levels you enter", WHITE, [dis_width / 3, dis_height / 3 + 150])
    message("LEVEL 2", WHITE, [dis_width / 3, dis_height / 3 + 180])
    message("Press ENTER to START the Game", GREEN, [dis_width / 3, dis_height / 3 + 240])
    message("ALL THE BEST !!!!!", RED, [dis_width / 3, dis_height / 3 + 280])
    pygame.display.update()  # Update the display

    # Wait for the Enter key to start the game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False  # Exit the loop and start the game
# def update_score_in_flask(username, score):
#     requests.post(f'http://127.0.0.1:5000/update_score', json={'username': username, 'score': score})

    # # When game ends:
    # final_score = score  # Your final score
    # update_score_in_flask(username, final_score)
    # # Main function to run the game
def main():
    while True:
        play_background_music()
        show_start_screen()
        game_loop_level_1()
main()


