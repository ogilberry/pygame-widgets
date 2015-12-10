# pygame-widgets
A collection of widgets for use in pygame, by Jordan Ogilvy

They are designed to be easy to use, and only require two lines of code in your pygame project.
first create the widget, with something like:

mywidget = WidgetType(game_window, position, some_attribute,...)

Then, in the event loop of your game, get all the events from pygame (events = pygame.event.get()), then
call update(events) on the widget, like so:

events = pygame.event.get()
for event in events:
  if event.type == pygame.SOME_EVENT:
    do something
    
mywidget.update(events)

ENTRY WIDGET
initialising is straightforward:
my_entry = Entry(display, position)
-display is any surface or pygame window,
-position is an (x,y) co-ordinate tuple representing the pixel location of the top left corner of the entry box.
Additional attributes with defaults:
width=100, font="Helvetica", fontsize=12, default_text = "Hello World!", fontcolor = (0,0,0), background = (255,255,255),
border = (0,0,0), activeborder = (0,100,255), borderwidth = 1, frames_per_blink = 15)

BUTTON WIDGET
initialising:
my_button = Button(display, position, normal, depressed, hover, message, action)
-display and position are the same as for the Entry widget.
-normal, depressed, and hover, are all strings representing the name of image files, e.g. "my_button.png".
-Each picture represents the button in each of its three different states as they are named.
-message is a string, and is the text to be shown on the button.
-action is a function, NOT a call to a function, and is the function that will be called when the button is clicked on.
Additional attributes with defaults:
-fontcolor = (0,0,0)
-font = "Helvetica"

