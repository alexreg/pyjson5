# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse


class _Bailout(Exception):
    pass


class ArgumentParser(argparse.ArgumentParser):
    SUPPRESS = argparse.SUPPRESS

    def __init__(self, host, prog, desc, **kwargs):
        kwargs['prog'] = prog
        kwargs['description'] = desc
        kwargs['formatter_class'] = argparse.RawDescriptionHelpFormatter
        super(ArgumentParser, self).__init__(**kwargs)
        self._host = host
        self.exit_status = None
        self.add_argument('-V', '--version', action='store_true',
                          help='Print the version and exit.')

    def parse_args(self, args=None, namespace=None):
        try:
            rargs = super(ArgumentParser, self).parse_args(args=args,
                                                           namespace=namespace)
        except _Bailout:
            return None

        return rargs

    # Redefining built-in 'file' pylint: disable=W0622

    def _print_message(self, msg, file=None):
        self._host.print_(msg=msg, stream=file, end='\n')

    def print_help(self, file=None):
        self._print_message(msg=self.format_help(), file=file)

    def error(self, message, bailout=True):  # pylint: disable=W0221
        self.exit(2, '%s: error: %s\n' % (self.prog, message), bailout=bailout)

    def exit(self, status=0, message=None,  # pylint: disable=W0221
             bailout=True):
        self.exit_status = status
        if message:
            self._print_message(message, file=self._host.stderr)
        if bailout:
            raise _Bailout()
