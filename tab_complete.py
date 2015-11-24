import os
import readline
import shlex


def prep_readline( completer ):
    readline.set_completer_delims( '\n\t;' )
    readline.parse_and_bind( 'tab: complete' )
    readline.set_completer( completer )

def _list_dir( directory ):
    files = []
    for filename in os.listdir( directory ):
        path = os.path.join( directory, filename )
        if os.path.isdir( path ):
            files.append( '{}{}'.format( path, os.sep ) )
        files.append( filename )
    return files

def norm_join_path(dirname, filename ):
    path = os.path.join( dirname, filename )
    return os.path.normpath( path )


def expand_path( path ):
    for function in ( os.path.expandvars, os.path.expanduser, os.path.normpath ):
        path = function( path )
    return path


def _complete_path( path ):
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


def _complete_hello( args ):
    if not args or not [ x for x in args if x ]:
        return './'
    else:
        path = args[0]
    return _complete_path( path )


if __name__ == '__main__':
    comp = Completer( {'hello': _complete_hello } )
    prep_readline( comp.complete )
    input( 'hello tabcomplete>>> ' )
