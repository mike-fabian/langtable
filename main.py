#!/usr/bin/python
# vim:fileencoding=utf-8:sw=4:et

# Copyright (c) 2013 Mike FABIAN <mfabian@redhat.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import lang_table
from lang_table import list_locales
from lang_table import list_keyboards

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='lang-table')
    parser.add_argument('-T', '--territoriesfilename',
                        nargs='?',
                        type=str,
                        default='./territories.xml',
                        help='territories file, default is ./territories.xml')
    parser.add_argument('-K', '--keyboardsfilename',
                        nargs='?',
                        type=str,
                        default='./keyboards.xml',
                        help='keyboards file, default is ./keyboards.xml')
    parser.add_argument('-L', '--languagesfilename',
                        nargs='?',
                        type=str,
                        default='./languages.xml',
                        help='languages file, default is ./languages.xml')
    parser.add_argument('-l', '--logfilename',
                        nargs='?',
                        type=str,
                        default='./lang_table.log',
                        help='log file, default is ./lang_table.log')
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='print debugging output')
    return parser.parse_args()

def main():
    args = parse_args()

    lang_table.init(debug = True,
                    logfilename = args.logfilename,
                    territoriesfilename = args.territoriesfilename,
                    languagesfilename = args.languagesfilename,
                    keyboardsfilename = args.keyboardsfilename)

if __name__ == '__main__':
    main()
