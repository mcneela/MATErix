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

from ast import literal_eval
import os, sys, re, matrix

# Generic class for validating some abstract collection of data.

class DataValidator:
    def __init__(self, *args):
        self.data = args    

# A class responsible for handling user-provided
# matrix dimensions.
        
class InputValidator(DataValidator):
    def validate(self):
        num_matrices = self.data[0]
        list_of_lists = self.data[1]
        assert num_matrices == len(list_of_lists), "Number of matrices to be multiplied must equal the number of dimension specifications given."

        # Verify that each matrix dimension
        # is given by the user as a list.

        for dim in list_of_lists:
            data = literal_eval(dim) # Allow Python to evaluate user-inputted strings as actual list objects.
            assert isinstance(data, list), "Matrix dimensions must be given in the format: [# of rows, # of columns]"
            assert len(data) == 2, "Matrices must have exactly two dimensions, namely the number of rows and the number of columns."

# A class that ensures that user-provided input to the file
# input.txt is valid.
            
class MatrixValidator(DataValidator):
    def validate_matrix_entries(self, num_matrices, dimension_list):
        value_dictionary = self.data[0]
        key_count = 1
        while key_count <= num_matrices:
            key_name = "Matrix " + str(key_count)
            for row in value_dictionary[key_name]:
                if len(row) != dimension_list[key_count - 1][1]:
                    print("You did not specify valid values for all the entries in " + key_name + ". Please re-enter these values.")
                    return False
            key_count += 1
        return True

# A class representing a conceptualization of a generic file
# as a readable object possessing some location on the user's machine
# (specified here by the variable "filepath"). This class contains
# a single associated method which allows the file to be opened
# using the machine's default editor.

class File:
    def __init__(self, filepath):
        self.filepath = filepath

    # Opens the file specified by filepath
    # using the user's system's default editor. 

    def default_editor(self, filepath):
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', filepath))
        elif os.name == 'nt':
            os.startfile(filepath)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', filepath))
    
class InputFile(File):
    def __init__(self, filepath, operation, num_matrices, *args):
        self.filepath = filepath
        self.operation = operation
        self.num_matrices = int(num_matrices) # Number of matrices to be multiplied.
        self.list_of_lists = args[0] # Extracting user input from tuple given by *args.
        self.data_tuple = self.create_input_file()
        self.dimension_list = self.data_tuple[0]
        self.matrix_list = self.data_tuple[1]
        

    # Creates the file input.txt in the script directory
    # and draws the matrix template which the
    # user will edit to the file. Returns list of matrix
    # dimensions for later use in program.
    
    def create_input_file(self):
        data_list = [] # List that will contain lists of the parsed user-input.
        i = 0

        # Confirm that user input is valid.
        
        check_input = InputValidator(self.num_matrices, self.list_of_lists)
        check_input.validate()
        
        # Convert user input into usable lists.
        

        # Break user input stream into a list of characters.
        raw_data = []
        parse_input = self.list_of_lists
        while i < len(self.list_of_lists):
           raw_data = (re.findall(r'-?[0-9]+', parse_input[i]))
           raw_data = [int(c) for c in raw_data]
           for number in raw_data:
               assert number > 0, "Matrix dimensions must be positive integers."
           data_list.append(raw_data)
           i += 1

        
            # A list of all the lists containing the matrix dimensions.

        # Verify that each pair of matrices is of proper dimensions to allow for multiplication.
        if self.operation == "multiply":
            for dim1, dim2 in zip(data_list, data_list[1:]):
                assert dim1[1] == dim2[0], "The width of matrix A must equal the width of matrix B for the multiplication to be valid"
        elif self.operation == "add":
            for dim1, dim2 in zip(data_list, data_list[1:]):
                assert dim1[0] == dim2[0] and dim1[1] == dim2[1], "Matrix A and Matrix B must be of the same dimensions to be added."
                

        input_file = open(self.filepath, "w+") # Create/open a file in which the user will input matrix values.
        user_matrices = [matrix.Matrix(dimension) for dimension in data_list]
        input_file.write("Replace the underscores with the entries for each matrix you wish to multiply.\n\n")
        for a_matrix, i in zip(user_matrices, range(1, self.num_matrices + 1)): a_matrix.draw_blank_matrix(i, input_file) # Write the matrices to input_file
        input_file.close() # Close the file.
        return (data_list, user_matrices)

    # To be called after user has edited input.txt.
    # Reads matrices row-by-row and returns a dictionary
    # of matrices and lists containing their rows.

    def read_matrix_from_file(self, filepath):
        all_matrices = {}     # Dictionary holding the values of matrices as strings.
        parsed_matrices = {}  # Dictionary holding the values of matrices as floats.
        matrix_count = 0      # Count of matrix currently being read to dictionary.
        matrix_values = []    # List holding the string matrix values.
        with open(filepath, "r") as file_to_read:
            for line in file_to_read:
                if line[0] == "M":
                    all_matrices["Matrix " + str(matrix_count)] = matrix_values 
                    matrix_values = []
                    matrix_count += 1
                if line[0] == "|":
                    matrix_values.append(line)
            all_matrices["Matrix " + str(matrix_count)] = matrix_values
        for key in all_matrices:
            parsed_matrices[key] = []
            j = 0
            while j < len(all_matrices[key]):
                parsed_matrices[key].append(re.findall(r'[-+]?[0-9]*\.?[0-9]+', all_matrices[key][j]))
                j += 1
        check_input = MatrixValidator(parsed_matrices)
        proper_termination = check_input.validate_matrix_entries(self.num_matrices, self.dimension_list)
        return (proper_termination, parsed_matrices)

    def pass_input_to_matrix(self, list_of_matrices, matrix_dictionary):
        for matrix, i in zip(list_of_matrices, range(1, self.num_matrices + 1)):
            matrix.set_entries(matrix_dictionary["Matrix " + str(i)])

# Subclass of the "File" class that is responsible for
# creating and writing to a file, output.txt, with the
# results of the operations applied to the user-provided
# matrices.

class OutputFile(File):
    def __init__(self, filepath, num_matrices, *args):
        self.filepath = filepath
        self.num_matrices = num_matrices
        self.matrix_list = args[0]
        self.create_output_file()
        
    def create_output_file(self):
        output_file = open(self.filepath, "w+")
        for current_matrix in self.matrix_list:
            current_matrix.draw_matrix_output(output_file)
        output_file.close()

        


