# (C) 2015, Daniel McNeela - All Rights Reserved
#
# This file is part of the MATErix software application.
# MATErix is proprietary software and may not be used,
# distributed, copied, published, or in any way altered
# without the express written permission of Daniel McNeela.
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# This file contains functions responsible for handling
# command line arguments passed to calculator.py by the
# user.

import argparse

def read_command(argv):
    usage_string = """   python calculator.py <arguments>
    
    Run MATErix at the command line by using the above syntax.
    
    A list of valid argument values can be found in the
    user_manual.txt file or by running calculator.py
    using either the -h or --help tag.
    """
    
    parser = argparse.ArgumentParser(prog='MATErix', description='Meet MATErix, your friend in the cold, calculating world of linear algebra.', usage=usage_string)
    operation_group = parser.add_mutually_exclusive_group()
    operation_group.add_argument('-a', '--add', action='store_true', dest='add', help='add an arbitrary number of matrices.')
    operation_group.add_argument('-m', '--multiply', choices=['iterative', 'strassen'], default='iterative', dest='multiply', help='multiply an arbitrary number of matrices using ALGORITHM', metavar='ALGORITHM')
    parser.add_argument('-t', '--time', action='store_true', dest='time', help='measure execution time of each implemented algorithm applied to input matrices.')
    parser.add_argument('--version', action='version', version='\n%(prog)s 1.0')
    
    args = parser.parse_args()
    if not (args.add or args.multiply):
        parser.error("You must specify an operation for MATErix to compute. For a list of valid operations, run MATErix using the -h or --help tag.")
    return args
