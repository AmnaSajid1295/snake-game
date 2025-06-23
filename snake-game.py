import turtle
import time
import random
import threading

delay = 0.1
score = 0
high_score = 0
food_counter = 0
super_food_timer = None

# Set up screen
wn = turtle.Screen()
wn.title("Snake Game 🐍")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Normal food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Super food
super_food = turtle.Turtle()
super_food.speed(0)
super_food.shape("square")
super_food.color("gold")
super_food.penup()
super_food.hideturtle()

# Segments list
segments = []

# Scoreboard
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Game over display
game_over = turtle.Turtle()
game_over.speed(0)
game_over.color("red")
game_over.penup()
game_over.hideturtle()
game_over.goto(0, 0)

# Movement functions
def go_up():
    if head.direction != "down":
        head.direction = "up"
def go_down():
    if head.direction != "up":
        head.direction = "down"
def go_left():
    if head.direction != "right":
        head.direction = "left"
def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)

# Optional start with spacebar
def start_game():
    if head.direction == "stop":
        head.direction = "up"
        game_over.clear()

# Hide super food after 6 seconds
def hide_super_food():
    time.sleep(6)
    super_food.hideturtle()

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
wn.onkeypress(start_game, "space")

# Game loop
while True:
    wn.update()

    # Collision with border
    if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
        game_over.clear()
        game_over.write("FAILED", align="center", font=("Courier", 36, "bold"))
        time.sleep(1.5)
        head.goto(0, 0)
        head.direction = "stop"

        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()

        score = 0
        delay = 0.1
        food_counter = 0
        food.showturtle()
        super_food.hideturtle()
        score_display.clear()
        score_display.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

    # Normal food collision
    if head.distance(food) < 20:
        x = random.randint(-270, 270)
        y = random.randint(-270, 270)
        food.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("lightgreen")
        new_segment.penup()
        segments.append(new_segment)

        delay -= 0.001
        score += 2
        food_counter += 1

        if food_counter % 8 == 0:
            super_food.goto(random.randint(-270, 270), random.randint(-270, 270))
            super_food.showturtle()
            if super_food_timer is None or not super_food_timer.is_alive():
                super_food_timer = threading.Thread(target=hide_super_food)
                super_food_timer.start()

        if score > high_score:
            high_score = score

        score_display.clear()
        score_display.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

    # Super food collision
    if super_food.isvisible() and head.distance(super_food) < 20:
        super_food.goto(1000, 1000)
        super_food.hideturtle()
        score += 8

        if score > high_score:
            high_score = score

        score_display.clear()
        score_display.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

    # Move the segments
    for i in range(len(segments)-1, 0, -1):
        x = segments[i-1].xcor()
        y = segments[i-1].ycor()
        segments[i].goto(x, y)

    if segments:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # Collision with self
    for segment in segments:
        if segment.distance(head) < 20:
            game_over.clear()
            game_over.write("FAILED", align="center", font=("Courier", 36, "bold"))
            time.sleep(1.5)
            head.goto(0, 0)
            head.direction = "stop"

            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()

            score = 0
            delay = 0.1
            food_counter = 0
            food.showturtle()
            super_food.hideturtle()
            score_display.clear()
            score_display.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)
