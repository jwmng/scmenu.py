import curses


class Menu():

    """ Simple curses Menu class. Creates a Simple menu which can be navigated
    using w (up), s (down), q (back) and e (select). Arguments are:
        - name (str): menu name (title)
        - options: list of tuples containing the item names their command
        - barData (str): data to be put in the information barData
        - selected=0 (int): initially selected item
        - settings: dict containing custom settings.
            settings keys can be:
                'bullet': (str) bullet shown in front of each option
                'selectedBullet': (str) bullet for selected option
                'infoPos': ('top' or 'bottom') location of info bar
                'keymap': list of keys in the form [up, down, select, back]"""

    def __init__(self, name, options, barData='', selected=0, settings=False):

        # Curses settings
        self.screen = curses.initscr()
        self.screen.border(0)
        curses.curs_set(0)
        curses.start_color()
        curses.noecho()
        curses.use_default_colors()
        self.screensize = self.screen.getmaxyx()

        # Get arguments
        self.barData = barData
        self.selected = selected
        self.size = len(options)
        self.name = name[0:self.screensize[1]-20]

        # Initialise lists
        self.optionNames = []
        self.optionCmds = []
        self.optionDict = {}

        # Order options in both dict and lists
        for option in options:
            # Truncate long names
            if len(option[0]) > self.screensize[1]:
                oName = option[1][0:self.screensize[1]-20] + '...'
            else:
                oName = option[0]
            self.optionNames.append(oName)
            self.optionCmds.append(option[1])
            self.optionDict[oName] = option[1]

        #  Default settings
        self.settings = {}
        self.settings['bullet'] = ''
        self.settings['selectedBullet'] = ''
        self.settings['infoPos'] = 'top'
        self.settings['keys'] = ['w', 's', 'e', 'q']  # Up down select quit

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Copy settings from settings argument
        if settings:
            self.settings.update(settings)

    def scroll(self):
        """ Makes the menu 'scrollable' if the number of items is larger than
        the height of the screen. Shows max 5 options above the selected option.
        """
        options = self.optionNames
        maxItems = self.screensize[0] - 5
        if self.size > maxItems:  # More options than fit on screen
            firstItem = max(0, self.selected - 5)
            lastItem = min(maxItems+firstItem, self.size)
            options = self.optionNames[firstItem:lastItem]
        return options

    def cdraw(self):
        """ Draws the menu using curses. """

        shownOptions = self.scroll()

        self.screen.clear()
        self.screen.border(0)

        # Draw the title centered and at line 0 (with spaces for readability)
        title = ' ' + self.name + ' '
        self.screen.addstr(0, (self.screensize[1]-len(title))/2, title)

        x = (self.screensize[0] - len(shownOptions)) / 2  # Vertical centering
        y = (self.screensize[1] - max([len(a) for a in self.optionNames]))/2
        # Items are horizontally left-aligned with the longest item centered.

        for name in shownOptions:  # Draw each item
            if name == self.optionNames[self.selected]:  # Highlight selected
                self.screen.addstr(
                    x, y,
                    self.settings['selectedBullet'] + name,
                    curses.color_pair(1))
            else:
                self.screen.addstr(x, y, self.settings['bullet'] + name)
            x = x + 1

        # Truncate the info bar if too long
        barData = self.barData[0:self.screensize[1]]

        # Infor bar can be positioned 'top' or 'bottom'
        if self.settings['infoPos'] == 'bottom':
            barXPos = self.screensize[0]-1
        else:
            barXPos = 1

        # Center horizontally
        barYPos = (self.screensize[1]-len(self.barData))/2
        self.screen.addstr(barXPos, barYPos, barData, curses.color_pair(1))

        self.screen.refresh()

    def back(self):  # Go back one menu
        return 'back'

    def down(self):  # 1 item down
        self.selected = (self.selected + 1) % self.size
        self.cdraw()
        return self.optionNames[self.selected]

    def up(self):  # 1 item up
        self.selected = (self.selected - 1) % self.size
        self.cdraw()
        return self.optionCmds[self.selected]

    def select(self):  # Return the currently selected item
        return self.optionCmds[self.selected]

    def show(self):
        """ Show the menu until an item is selected or the back button is
        pressed. Returns the item's command or 'back', respectively."""

        self.cdraw()  # Draw the menu
        self.finished = False
        keymap = [ord(x) for x in self.settings['keys']]
        while not self.finished:  # Loop until select/back
            key = self.screen.getch()
            if key == keymap[3]:  # default q: Back button
                self.finished = True
                selectedItem = 'back'
            elif key == keymap[0]:  # default w: Up
                self.up()
            elif key == keymap[1]:  # default s: Down
                self.down()
            elif key == keymap[2]:  # default e: Select
                self.finished = True
                selectedItem = self.select()
        self.screen.clear()
        self.screen.refresh()
        return selectedItem

if __name__ == '__main__':
    sampleSettings = {'keys': ('1', '2', '3', '4'), 'bullet': '>'}
    sampleOptions = [('Option 1', 5),
                     ('Option 2', 'opt2'),
                     ('Something else', 'opt3')]
    sampleBar = '1: up, 2: down, 3: select, 4: back'
    sampleMenu = Menu('Example menu', sampleOptions, sampleBar,
                      0, sampleSettings)
    print sampleMenu.show()
