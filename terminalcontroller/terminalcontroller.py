import sys, re

# modified from http://code.activestate.com/recipes/475116/

TERM_ESCAPE = False

class TerminalController:
    """
    A class that can be used to portably generate formatted output to
    a terminal.

    `TerminalController` defines a set of instance variables whose
    values are initialized to the control sequence necessary to
    perform a given action.  These can be simply included in normal
    output to the terminal:

        >>> term = TerminalController()
        >>> print 'This is '+term.GREEN+'green'+term.NORMAL

    Alternatively, the `render()` method can used, which replaces
    '${action}' with the string required to perform 'action':

        >>> term = TerminalController()
        >>> print term.render('This is ${GREEN}green${NORMAL}')

    If the terminal doesn't support a given action, then the value of
    the corresponding instance variable will be set to ''.  As a
    result, the above code will still work on terminals that do not
    support color, except that their output will not be colored.
    Also, this means that you can test whether the terminal supports a
    given action by simply testing the truth value of the
    corresponding instance variable:

        >>> term = TerminalController()
        >>> if term.CLEAR_SCREEN:
        ...     print 'This terminal supports clearning the screen.'

    Finally, if the width and height of the terminal are known, then
    they will be stored in the `COLS` and `LINES` attributes.
    """
    # Cursor movement:
    BOL = ''             #: Move the cursor to the beginning of the line
    UP = ''              #: Move the cursor up one line
    DOWN = ''            #: Move the cursor down one line
    LEFT = ''            #: Move the cursor left one char
    RIGHT = ''           #: Move the cursor right one char

    # Deletion:
    CLEAR_SCREEN = ''    #: Clear the screen and move to home position
    CLEAR_EOL = ''       #: Clear to the end of the line.
    CLEAR_BOL = ''       #: Clear to the beginning of the line.
    CLEAR_EOS = ''       #: Clear to the end of the screen

    # Output modes:
    BOLD = ''            #: Turn on bold mode
    BLINK = ''           #: Turn on blink mode
    DIM = ''             #: Turn on half-bright mode
    REVERSE = ''         #: Turn on reverse-video mode
    NORMAL = ''          #: Turn off all modes

    # Cursor display:
    HIDE_CURSOR = ''     #: Make the cursor invisible
    SHOW_CURSOR = ''     #: Make the cursor visible

    # Terminal size:
    COLS = None          #: Width of the terminal (None for unknown)
    LINES = None         #: Height of the terminal (None for unknown)

    # Foreground colors:
    BLACK = BLUE = GREEN = CYAN = RED = MAGENTA = YELLOW = WHITE = ''

    # Background colors:
    BG_BLACK = BG_BLUE = BG_GREEN = BG_CYAN = ''
    BG_RED = BG_MAGENTA = BG_YELLOW = BG_WHITE = ''

    _STRING_CAPABILITIES = """
    BOL=cr UP=cuu1 DOWN=cud1 LEFT=cub1 RIGHT=cuf1
    CLEAR_SCREEN=clear CLEAR_EOL=el CLEAR_BOL=el1 CLEAR_EOS=ed BOLD=bold
    BLINK=blink DIM=dim REVERSE=rev UNDERLINE=smul NORMAL=sgr0
    HIDE_CURSOR=cinvis SHOW_CURSOR=cnorm""".split()
    _COLORS = """BLACK BLUE GREEN CYAN RED MAGENTA YELLOW WHITE""".split()
    _ANSICOLORS = "BLACK RED GREEN YELLOW BLUE MAGENTA CYAN WHITE".split()

    def __init__(self, term_stream=sys.stdout, escape=False):
        """
        Create a `TerminalController` and initialize its attributes
        with appropriate values for the current terminal.
        `term_stream` is the stream that will be used for terminal
        output; if this stream is not a tty, then the terminal is
        assumed to be a dumb terminal (i.e., have no capabilities).
        """

        # when printing things out on lines accepting user input control
        # characters must be wrapped in special characters for correct
        # word wrapping, always wrap when escape == True
        self.escape = escape

        # Curses isn't available on all platforms
        try: import curses
        except: return

        # If the stream isn't a tty, then assume it has no capabilities.
        if not term_stream.isatty(): return

        # Check the terminal type.  If we fail, then assume that the
        # terminal has no capabilities.
        try: curses.setupterm()
        except: return

        # Look up numeric capabilities.
        self.COLS = curses.tigetnum('cols')
        self.LINES = curses.tigetnum('lines')

        # Look up string capabilities.
        for capability in self._STRING_CAPABILITIES:
            (attrib, cap_name) = capability.split('=')
            setattr(self, attrib, self._tigetstr(cap_name) or '')

        # Colors
        set_fg = self._tigetstr('setf')
        if set_fg:
            for i,color in zip(range(len(self._COLORS)), self._COLORS):
                setattr(self, color, curses.tparm(set_fg, i) or '')
        set_fg_ansi = self._tigetstr('setaf')
        if set_fg_ansi:
            for i,color in zip(range(len(self._ANSICOLORS)), self._ANSICOLORS):
                setattr(self, color, curses.tparm(set_fg_ansi, i) or '')
        set_bg = self._tigetstr('setb')
        if set_bg:
            for i,color in zip(range(len(self._COLORS)), self._COLORS):
                setattr(self, 'BG_'+color, curses.tparm(set_bg, i) or '')
        set_bg_ansi = self._tigetstr('setab')
        if set_bg_ansi:
            for i,color in zip(range(len(self._ANSICOLORS)), self._ANSICOLORS):
                setattr(self, 'BG_'+color, curses.tparm(set_bg_ansi, i) or '')


    def _tigetstr(self, cap_name):
        # String capabilities can include "delays" of the form "$<2>".
        # For any modern terminal, we should be able to just ignore
        # these, so strip them out.
        import curses
        cap = curses.tigetstr(cap_name) or ''
        return re.sub(r'\$<\d+>[/*]?', '', cap)

    def render(self, template):
        """
        Replace each $-substitutions in the given template string with
        the corresponding terminal control string (if it's defined) or
        '' (if it's not).
        """
        return re.sub(r'\$\$|\${\w+}', self._render_sub, template)

    def _render_sub(self, match):
        s = match.group()
        if s == '$$':
            return s
        else:
            rendered = getattr(self, s[2:-1])
            if self.escape :
                rendered = '\001'+rendered+'\002'
            return rendered


# convenience methods
def colorize(str,codes='normal') :
    term = TerminalController(escape=TERM_ESCAPE)
    outstr = ''.join(['${%s}'%l.upper() for l in codes.split(' ')])
    return term.render(outstr+str+'${NORMAL}')
def normal(st) :
    return colorize(st)

# fg colors
def black(st) :
    return colorize(st,'black')
def blue(st) :
    return colorize(st,'blue')
def green(st) :
    return colorize(st,'green')
def cyan(st) :
    return colorize(st,'cyan')
def red(st) :
    return colorize(st,'red')
def magenta(st) :
    return colorize(st,'magenta')
def yellow(st) :
    return colorize(st,'yellow')
def white(st) :
    return colorize(st,'white')

# bg colors
def bg_black(st) :
    return colorize(st,'bg_black')
def bg_blue(st) :
    return colorize(st,'bg_blue')
def bg_green(st) :
    return colorize(st,'bg_green')
def bg_cyan(st) :
    return colorize(st,'bg_cyan')
def bg_red(st) :
    return colorize(st,'bg_red')
def bg_magenta(st) :
    return colorize(st,'bg_magenta')
def bg_yellow(st) :
    return colorize(st,'bg_yellow')
def bg_white(st) :
    return colorize(st,'bg_white')

# styles
def bold(st) :
    return colorize(st,'bold')
def blink(st) :
    return colorize(st,'blink')
def reverse(st) :
    return colorize(st,'reverse')

# convenience logging functions
def info(st,fd=sys.stderr) :
    out_st = 'INFO: %s\n'%st
    if fd :
        fd.flush()
        fd.write(colorize(out_st,'bold white'))
    return out_st
def warn(st,fd=sys.stderr) :
    out_st = 'WARN: %s\n'%st
    if fd :
        fd.flush()
        fd.write(colorize('WARN: ','bold magenta')+colorize(st+'\n','bold yellow'))
    return out_st
def error(st,fd=sys.stderr) :
    out_st = 'ERROR: %s\n'%st
    if fd :
        fd.flush()
        fd.write(colorize('ERROR: ','bold red')+colorize(st+'\n','bold red'))
    return out_st
def announce(st,fd=sys.stderr) :
    out_st = '\n'+(' '+st+' ').center(max(80,80-len(st)),'=')+'\n'
    if fd :
        fd.flush()
        fd.write(colorize(out_st,'bold yellow'))
    return out_st

def test() :
    sys.stdout.write(normal('Normal colors:\n'))
    sys.stdout.write('This is %s text.\n'%bg_white(black('black')))
    sys.stdout.write('This is %s text.\n'%blue('blue'))
    sys.stdout.write('This is %s text.\n'%green('green'))
    sys.stdout.write('This is %s text.\n'%cyan('cyan'))
    sys.stdout.write('This is %s text.\n'%red('red'))
    sys.stdout.write('This is %s text.\n'%magenta('magenta'))
    sys.stdout.write('This is %s text.\n'%yellow('yellow'))
    sys.stdout.write('This is %s text.\n'%white('white'))

    sys.stdout.write(bold('Bold colors:\n'))
    sys.stdout.write('This is bold %s text.\n'%bold(bg_white(black('black'))))
    sys.stdout.write('This is bold %s text.\n'%bold(blue('blue')))
    sys.stdout.write('This is bold %s text.\n'%bold(green('green')))
    sys.stdout.write('This is bold %s text.\n'%bold(cyan('cyan')))
    sys.stdout.write('This is bold %s text.\n'%bold(red('red')))
    sys.stdout.write('This is bold %s text.\n'%bold(magenta('magenta')))
    sys.stdout.write('This is bold %s text.\n'%bold(yellow('yellow')))
    sys.stdout.write('This is bold %s text.\n'%bold(white('white')))

    sys.stdout.write(blink('Blinking text\n'))
    sys.stdout.write(colorize('Dimmed text\n','dim'))
    sys.stdout.write(reverse('Reverse text\n'))

    TERM_ESCAPE = True
    announce('This is announce')
    info('This is info')
    warn('This is warn')
    error('This is error')

if __name__ == '__main__' :
    test()
