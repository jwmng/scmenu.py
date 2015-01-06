# scmenu
Simple menu for future python projects. Requires `curses`.

## Usage example:

    sampleSettings = {'keys': ('1', '2', '3', '4'), 'bullet': '>'}
    sampleOptions = [('Option 1', 5),
                    ('Option 2', 'opt2'),
                    ('Something else', 'opt3')]
    sampleBar = '1: up, 2: down, 3: select, 4: back'
    sampleMenu = Menu('Example menu', sampleOptions, sampleBar,
                    0, sampleSettings)
    print sampleMenu.show()

## Documentation
All other documentation is included in docstring

## License
BSD Style
