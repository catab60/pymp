from pymp import Server
import random

server = Server("0.0.0.0", 5555, 2)

screen_width = 800
screen_height = 600
ball_speed_x = 5
ball_speed_y = 5
ball_size = 10
paddle_width = 10
paddle_height = 100

ball_x = screen_width // 2
ball_y = screen_height // 2
vel_x = 0
vel_y = 0

left_score = 0
right_score = 0

while True:
    if server.data:
        players = list(server.data.items())
    else:
        players = []

    left_paddle_y = 10
    right_paddle_y = 10
    
    for player in players:
        try:
            if player[1][0]["IsFirstPlayer"]:
                left_paddle_y = player[1][0]["player_y"]
            else:
                right_paddle_y = player[1][0]["player_y"]
        except:
            pass


    if len(players) < 2:
        ball_x = screen_width // 2
        ball_y = screen_height // 2
        vel_x = 0
        vel_y = 0
    else:
        if vel_x == 0 and vel_y == 0:
            vel_x = ball_speed_x * random.choice([-1, 1])
            vel_y = ball_speed_y

        ball_x += vel_x
        ball_y += vel_y

        if ball_y <= 0 or ball_y + ball_size >= screen_height:
            vel_y = -vel_y

        if ball_x <= paddle_width and left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
            vel_x = -vel_x

        if ball_x + ball_size >= screen_width - paddle_width and right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
            vel_x = -vel_x

        if ball_x < 0:
            right_score += 1
            ball_x = screen_width // 2
            ball_y = screen_height // 2
            vel_x = 0
            vel_y = 0
        elif ball_x > screen_width:
            left_score += 1
            ball_x = screen_width // 2
            ball_y = screen_height // 2
            vel_x = 0
            vel_y = 0

    server.wait(0.01)
    server.send_to_clients([ball_x, ball_y, left_score, right_score])
