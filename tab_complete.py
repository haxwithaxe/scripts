import os
import readline
import shlex
<<<<<<< 55a23e4d0277ec2f24ad8098cdefb347290511fb
=======
import sys


def stderr(*strings):
    print(*strings, file=sys.stdout)
>>>>>>> added xrandr_setup.sh and tab_complete.py


def prep_readline( completer ):
    readline.set_completer_delims( '\n\t;' )
    readline.parse_and_bind( 'tab: complete' )
<<<<<<< 55a23e4d0277ec2f24ad8098cdefb347290511fb
    readline.set_completer( completer )
=======
    readline.set_completer( completer.complete )
    readline.set_completion_display_matches_hook(completer.display_matches)

>>>>>>> added xrandr_setup.sh and tab_complete.py

def _list_dir( directory ):
    files = []
    for filename in os.listdir( directory ):
        path = os.path.join( directory, filename )
        if os.path.isdir( path ):
            files.append( '{}{}'.format( path, os.sep ) )
        files.append( filename )
    return files

<<<<<<< 55a23e4d0277ec2f24ad8098cdefb347290511fb
=======

>>>>>>> added xrandr_setup.sh and tab_complete.py
def norm_join_path(dirname, filename ):
    path = os.path.join( dirname, filename )
    return os.path.normpath( path )


def expand_path( path ):
    for function in ( os.path.expandvars, os.path.expanduser, os.path.normpath ):
        path = function( path )
    return path


<<<<<<< 55a23e4d0277ec2f24ad8098cdefb347290511fb
def _complete_path( path ):
=======
def _complete_path( path, state = None ):
>>>>>>> added xrandr_setup.sh and tab_complete.py
    if not path:
        return _list_dir('.')
    path = expand_path( path )
    dirname, path_fragment = os.path.split( path )
    dirname = dirname or '.'
    guesses = [ norm_join_path( dirname, guess ) for guess in _list_dir( dirname ) if guess.startswith( path_fragment ) ]
    if os.path.isdir( path ):
        os.path.split()
        return [ norm_join_path( path, guess ) for guess in _list_dir( path ) ]
    if not guesses or len( guesses ) == 1:
        return path + os.sep
    return guesses


class Completer:

<<<<<<< 55a23e4d0277ec2f24ad8098cdefb347290511fb
    def __init__( self, commands ):
        self.commands = commands
        self._state = self._text = self._line = None

    def complete( self, text, state ):
        if not text or [ x for x in self._commands.keys() if x.startswith( text ) ]:
            return [ x for x in self.commands.keys() ][state]
        return self._complete_command( text, state )
        

    def _complete_command( self, text, state ):
        args = shlex.split( text )
        if len(args) > 1: 
            command = args.pop()
        else:
            command = text
        if command.strip() in self.commands:
            return self.commands[command.strip()]( args )
        guesses = [ guess + ' ' for guess in self.commands if guess.startswith( command ) ]
        guesses.append( )
        return guesses

=======
    def __init__( self, commands, subcompleters = None ):
        self.commands = commands
        self.subcompleters = subcompleters
        self._state = self._text = self._line = None

    def complete(self, text, state):
        return self._get_guesses(text, state)[state]

    def _get_guesses( self, text, state ):
        args = shlex.split( text )
        if text:
            args = shlex.split( text )
            if args:
                if self._is_command( args[0] ):
                    stderr('command')
                    return self._complete_command( args, state )
                else:
                    stderr('fallback')
                    self._fallback(args, state)
        cmds = [ x for x in self.commands.keys() ]
        stderr(cmds)
        return cmds
        
    def _is_command(self, first_string):
        return [ x for x in self.commands.keys() if x.startswith( first_string ) or x == first_string ]

    def _complete_command( self, args, state ):
        command = args.pop().strip()
        if command.strip() in self.commands:
            return self.commands[command.strip()]( args )
        guesses = [ guess + ' ' for guess in self.commands if guess.startswith( command ) ]
        return guesses

    def _fallback(self, args, state):
        for completer in self.subcompleters:
            yield completer(args, state)

    def display_matches(self, substitution, matches, longest_match_length):
        line_buffer = readline.get_line_buffer()
        columns = os.environ.get('COLUMNS', 80)

        print()

        guess_template = '{:<' + str(int(max(map(len, matches)) * 1.2)) + '}'

        guesses = ''
        for match in matches:
            match = guess_template.format(match[len(substitution):])
            if len(guesses + match) > columns:
                print(guesses)
                guesses = ''
            guesses += match

        if guesses:
            print(guesses)

        print('> ', line_buffer, end='', flush=True)

>>>>>>> added xrandr_setup.sh and tab_complete.py

def _complete_hello( args ):
    if not args or not [ x for x in args if x ]:
        return './'
    else:
        path = args[0]
    return _complete_path( path )


if __name__ == '__main__':
<<<<<<< 55a23e4d0277ec2f24ad8098cdefb347290511fb
    comp = Completer( {'hello': _complete_hello } )
    prep_readline( comp.complete )
=======
    comp = Completer( {'hello': _complete_hello }, (_complete_path,) )
    prep_readline( comp )
>>>>>>> added xrandr_setup.sh and tab_complete.py
    input( 'hello tabcomplete>>> ' )
