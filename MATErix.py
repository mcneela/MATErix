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

import util, cmd
import subprocess, os, sys, cProfile, pstats

valid_input = False
input_filepath = os.path.join(sys.path[0], "input.txt")
output_filepath = os.path.join(sys.path[0], "output.txt")
# Prompt the user for input.
args = cmd.read_command(sys.argv)
if args.add:
    string = "add"
elif args.multiply:
    string = "multiply"
prompt_input = input("Enter the number of matrices you wish to " + string + ''' followed by the dimensions of each matrix to be multiplied in brackets.\n
Arguments should be delineated by the - character.\n
Improperly formatted input will cause program to terminate and throw an assertion error.\n
In this case, restart the program and be sure to properly format your input.\n
An example of properly formatted input is: 2 - [3, 5] - [5, 4]\n\n''')

file_args = prompt_input.split(" - ") # Generate arguments for use by create_input_file.
input_file = util.InputFile(input_filepath, string, file_args[0], file_args[1:]) # Create an input.txt file in which user will enter matrix values.

while not valid_input:
    input_file.default_editor(input_filepath) # Opens input.txt file in system's default editor, and creates a list of dimensions of matrices.
    input("\nEdit, save, and close the text file, then press Enter to continue: \n")
    user_data = input_file.read_matrix_from_file(input_filepath)
    matrix_entries = user_data[1]
    valid_input = user_data[0]
matrix_list = input_file.matrix_list
input_file.pass_input_to_matrix(matrix_list, matrix_entries)
product_list = [matrix_list[0]]
add = []
iterative = []
strassen = []
if args.time:
    profiler = cProfile.Profile()
    for matrix_a, matrix_b in zip(product_list, matrix_list[1:]):
        if args.add:
            profiler.enable()
            add.append(profiler.runcall(matrix_a.__add__, matrix_b))
            profiler.disable()
        elif args.multiply == 'iterative':
            profiler.enable()
            iterative.append(profiler.runcall(matrix_a.__mul__, matrix_b))
            profiler.disable()
        elif args.multiply == 'strassen':
            desired_rows = matrix_a.num_rows
            desired_columns = matrix_b.num_columns
            profiler.enable()
            strassen.append(profiler.runcall(matrix_a.strassen, matrix_b).strassen_strip(desired_rows, desired_columns))
            profiler.disable()
else:
    for matrix_a, matrix_b in zip(product_list, matrix_list[1:]):
        if args.add:
            add.append(matrix_a + matrix_b)
        elif args.multiply == 'iterative':
            iterative.append(matrix_a * matrix_b)
        elif args.multiply == 'strassen':
            desired_rows = matrix_a.num_rows
            desired_columns = matrix_b.num_columns
            strassen.append(matrix_a.strassen(matrix_b).strassen_strip(desired_rows, desired_columns))

if args.time:
    profile = util.File(os.path.join(sys.path[0], "profile.txt"))
    to_write = open(os.path.join(sys.path[0], "profile.txt"), 'a')   
    pstats.Stats(profiler, stream=to_write).strip_dirs().print_stats()
    profile.default_editor(os.path.join(sys.path[0], "profile.txt"))
if args.add:
    output_file = util.OutputFile(output_filepath, len(add), add)
    output_file.default_editor(output_filepath)
elif args.multiply == 'iterative':
    output_file = util.OutputFile(output_filepath, len(iterative), iterative)
    output_file.default_editor(output_filepath)
elif args.multiply == 'strassen':
    output_file = util.OutputFile(output_filepath, len(strassen), strassen)
    output_file.default_editor(output_filepath)

