import time

# Initial coordinates
ball_diameter = 2

# Get TKinter ready to go
from Tkinter import *
window = Tk()
canvas = Canvas(window, width=500, height=500, bg='white')
canvas.pack()

# For each timestep
for t in range(1, 500):

    # Create an circle which is in an (invisible) box whose top left corner is at (x[t], y[t])
    canvas.create_rectangle(t, t, t, t, fill="blue", tag='cell')
    canvas.update()

    # Pause for 0.05 seconds, then delete the image
    time.sleep(0.05)
    canvas.delete('cell')

# I don't know what this does but the script won't run without it.
# window.mainloop()
