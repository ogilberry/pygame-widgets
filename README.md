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
