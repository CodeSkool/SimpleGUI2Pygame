# whack-a-dot

# Game starts with a logo "Whack-A-Dot", prompt "Click to begin".
#   After 10 seconds, display the high scores.
#   After 20 seconds return to the logo.
# User clicks. Player starts with 3 lives
# Game counts down: 3, 2, 1... GO!
# Several circles displayed
# A dot appears in one of the circles (chosen randomly)
# DO: A timer counts down from 5 seconds (in tenths of a second)
#   Either: If the player clicks on the dot, the timer stops. The remaining time (x100) is added to the score.
#   OR: If the player does not click on the dot before the timer stops, they lose one life, the game counts down from 3 again.
# LOOP until no more lives
# Display the final score, record the user's initials if they got a high score.
# Display the logo / high-score list loop

# screen_saver
    # Game starts with a logo "Whack-A-Dot", prompt "Click to begin".
    #   After 10 seconds, display the high scores.
    #   After 20 seconds return to the logo.
    # User click >>> game_start
# game_start
    # Player starts with 3 lives
    # Prompt: Click when ready
    # Game counts down: 3, 2, 1... GO!
    # >>> playing
# game_over
    # Display the final score, record the user's initials if they got a high score.
    # >>> screen_saver
# playing
    # Several circles displayed
    # A dot appears in one of the circles (chosen randomly)
    # DO: A timer counts down from 5 seconds (in tenths of a second)
    #   Either: If the player clicks on the dot, the timer stops. The remaining time (x100) is added to the score.
    #               >>> playing
    #   OR: If the player does not click on the dot before the timer stops, they lose one life, the game counts down from 3 again.
    #               >>> game_start
    # LOOP until no more lives
    # game_over