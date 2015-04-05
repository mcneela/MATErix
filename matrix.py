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

import cProfile

def profile_func(func):
    def wrapper(*args, **kwargs):
        fpath = func.__name__ + '.txt'
        profile = cProfile.Profile()
        profile.enable()
        ret = profile.runcall(func, *args, **kwargs)
        profile.disable()
        profile.print_stats()
        return ret
    return wrapper


class Matrix:
    def __init__(self, dimension_list):
        self.dimension_list = dimension_list    # The list holding the dimensions of the matrix, e.g. [3, 4].
        self.num_rows = dimension_list[0]       # The number of rows in the matrix.
        self.num_columns = dimension_list[1]    # The number of columns in the matrix.
        self.entries = [[None for i in range(0, self.num_columns)] for j in range(0, self.num_rows)] # The matrix's entries held in a two-dimensional list.

    #Returns True if the matrix is a square matrix and False otherwise.

    def is_square(self):
        if self.num_rows == self.num_columns:
            return True
        return False

    # The string representation for the matrix object.

    def __str__(self):
        longest_number = 0
        has_negative = False
        for row in self.entries:
            for value in row:
                if len(str(value)) > len(str(longest_number)):
                    longest_number = value
                if value < 0:
                    has_negative = True
        if has_negative:
            front_padding = " "
        back_padding = len(str(longest_number))
        row_strings = [["|"] for i in range(self.num_rows)]
        for row, string_row in zip(self.entries, row_strings):
            for value in row[:-1]:
                if value < 0:
                    space_string = ""
                    i = 0
                    while i < back_padding - len(str(value)):
                        space_string += " "
                        i += 1
                    string_row[0] += (str(value) + space_string + " ")
                else:
                    space_string = ""
                    i = 0
                    while i < back_padding - len(str(value)) - 1:
                        space_string += " "
                        i += 1
                    if has_negative:
                        string_row[0] += front_padding + str(value) + space_string + " "
                    else:
                        string_row[0] += (str(value) + space_string + " ")
            string_row[0] += (str(row[-1]) + space_string + "|")
        string_representation = ""
        for row in row_strings:
            string_representation += row[0] + "\n"
        return string_representation
            

    # Method to be called when two matrix objects are compared using the '==' operator.
    
    def __eq__(self, other):
        if self.dimension_list == other.dimension_list:
            for i in range(self.num_rows):
                for j in range(self.num_columns):
                    if self.entries[i][j] != other.entries[i][j]:
                        return False
            return True
        return False
        
    # Method to be called when adding matrix objects using the '+' operator.

    def __add__(self, other):
        # sum_entries holds the entries with which the matrix self + other will be initialized.
        sum_entries = [[0 for j in range(self.num_columns)] for i in range(self.num_rows)]
        if self.dimension_list != other.dimension_list:
            raise MatrixAddError("The matrices to be added must be of the same dimensions.")
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                sum_entries[row][column] = self.entries[row][column] + other.entries[row][column]
        sum_matrix = Matrix([self.num_rows, self.num_columns])
        sum_matrix.set_entries(sum_entries)
        return sum_matrix

    # Method to be called when subtracting matrix other from self using the '-' operator.

    def __sub__(self, other):
        sub_entries = [[0 for j in range(self.num_columns)] for i in range(self.num_rows)]
        if self.dimension_list != other.dimension_list:
            raise MatrixAddError("The matrices to be subtracted must be of the same dimensions.")
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                sub_entries[row][column] = self.entries[row][column] - other.entries[row][column]
        sub_matrix = Matrix([self.num_rows, self.num_columns])
        sub_matrix.set_entries(sub_entries)
        return sub_matrix

    # Default method to be called when multiplying two matrices using '*' operator.
    # Uses a basic, iterative algorithm to compute the product.

    def __mul__(self, other):
        product_entries = [[0 for j in range(0, other.num_columns)] for i in range(0, self.num_rows)]
        for i in range(self.num_rows):
            for j in range(other.num_columns):
                for k in range(self.num_columns):
                    product_entries[i][j] += self.entries[i][k]*other.entries[k][j]
        product_matrix = Matrix([self.num_rows, other.num_columns])
        product_matrix.set_entries(product_entries)
        return product_matrix

    def strassen(self, matrix_b):
        desired_product_dims = [self.num_rows, matrix_b.num_columns]
        product_entries = [[0 for j in range(0, matrix_b.num_columns)] for i in range(0, self.num_rows)]
        if (self.is_square() and matrix_b.is_square()) and (self.num_rows % 2 == 0):
            if self.num_rows == 2:
                return self * matrix_b
    
            submatrix_dimension = self.num_rows//2
            dimension_list = [submatrix_dimension, submatrix_dimension]
            A_11, A_12, A_21, A_22 = Matrix(dimension_list), Matrix(dimension_list), Matrix(dimension_list), Matrix(dimension_list)
            B_11, B_12, B_21, B_22 = Matrix(dimension_list), Matrix(dimension_list), Matrix(dimension_list), Matrix(dimension_list)
            submatrixA_list = [A_11, A_12, A_21, A_22]
            submatrixB_list = [B_11, B_12, B_21, B_22]
            range_double_list = [[range(0, submatrix_dimension), range(submatrix_dimension, 2*submatrix_dimension)] for i in range(0, 2)]
            submatrix_count = 0
            submatrixA_entries = [[0], [0], [0], [0]]
            submatrixB_entries = [[0], [0], [0], [0]]
            while submatrix_count < 4:
                i = 0
                while i < 2:
                    j = 0
                    while j < 2:
                        submatrixA_entries[submatrix_count] = [[self.entries[n][m] for m in range_double_list[i][j]] for n in range_double_list[j][i]]
                        submatrixB_entries[submatrix_count] = [[matrix_b.entries[n][m] for m in range_double_list[i][j]] for n in range_double_list[j][i]]
                        submatrixA_list[submatrix_count].set_entries(submatrixA_entries[submatrix_count])
                        submatrixB_list[submatrix_count].set_entries(submatrixB_entries[submatrix_count])
                        submatrix_count += 1
                        j += 1
                    i += 1
        
            P_1 = (A_11.strassen_strip(submatrix_dimension, submatrix_dimension) + A_22.strassen_strip(submatrix_dimension, submatrix_dimension)).strassen((B_11 + B_22))
            P_2 = (A_21 + A_22).strassen(B_11)
            P_3 = A_11.strassen((B_12 - B_22))
            P_4 = A_22.strassen((B_21 - B_11))
            P_5 = (A_11 + A_12).strassen(B_22)
            P_6 = (A_21 - A_11).strassen((B_11 + B_12))
            P_7 = (A_12 - A_22).strassen((B_21 + B_22))

            C_11 = P_1 + P_4 - P_5 + P_7
            C_12 = P_3 + P_5
            C_21 = P_2 + P_4
            C_22 = P_1 + P_3 - P_2 + P_6
            c_list = [C_11, C_21, C_12, C_22]
            
            final_product_entries = [0, 0, 0, 0]
            final_product = Matrix([self.num_rows, matrix_b.num_columns])
            
            submatrix_count = 0
            while submatrix_count < 4:
                final_product_entries[submatrix_count] = [[c_list[submatrix_count].entries[n][m] for m in range(0, 2)] for n in range(0, 2)]
                submatrix_count += 1
            entry_list = []
            
            for half_row1, half_row2 in zip(final_product_entries, final_product_entries[submatrix_dimension:]):
                for entry1, entry2 in zip(half_row1, half_row2):
                    entry_list.append(entry1 + entry2)
            final_product.set_entries(entry_list)

            if final_product.num_rows != desired_product_dims[0]:
                while final_product.num_rows > desired_product_dims[0]:
                    final_product.remove_row()
            if final_product.num_columns != desired_product_dims[1]:
                while final_product.num_columns != desired_product_dims[1]:
                    final_product.remove_column()
            return final_product

        elif (self.is_square() and matrix_b.is_square()) and self.num_columns%2 != 0:
            self.add_column()
            self.add_row()
            matrix_b.add_column()
            matrix_b.add_row()
            return self.strassen(matrix_b)
        
        else:
            if not (self.is_square() and matrix_b.is_square()):
                if matrix_b.is_square():
                    dim_dif = abs(self.num_rows - self.num_columns)
                    if max(self.num_rows, self.num_columns) == self.num_columns:
                        i = 0
                        while i < dim_dif:
                            self.add_row()
                            i += 1
                    else:
                        i = 0
                        while i < dim_dif:
                            self.add_column()
                            i += 1
                    return self.strassen(matrix_b)
                
                elif self.is_square():
                    dim_dif = abs(matrix_b.num_rows - matrix_b.num_columns)
                    if max(matrix_b.num_rows, matrix_b.num_columns) == matrix_b.num_columns:
                        i = 0
                        while i < dim_dif:
                            matrix_b.add_row()
                            i += 1
                    else:
                        i = 0
                        while i < dim_dif:
                            matrix_b.add_column()
                            i += 1
                    return self.strassen(matrix_b)
                                 
                else:
                    dim_dif = abs(self.num_rows - self.num_columns)
                    if max(self.num_rows, self.num_columns) == self.num_columns:
                        i = 0
                        while i < dim_dif:
                            self.add_row()
                            i += 1
                    elif max(self.num_rows, self.num_columns) == self.num_rows:
                        i = 0
                        while i < dim_dif:
                            self.add_column()
                            i += 1
                            
                    dim_dif = abs(matrix_b.num_rows - matrix_b.num_columns)
                    if max(matrix_b.num_rows, matrix_b.num_columns) == matrix_b.num_columns:
                        i = 0
                        while i < dim_dif:
                            matrix_b.add_row()
                            i += 1
                            
                    elif max(matrix_b.num_rows, matrix_b.num_columns) == matrix_b.num_rows:
                        i = 0
                        while i < dim_dif:
                            matrix_b.add_column()
                            i += 1
                    return self.strassen(matrix_b)
        
    # Returns a list of strings, where each string
    # is a line to be written to the input file.

    def format_matrix_text(self):
        i, j = 0, 0 # Count variables for loops involving num_rows and num_columns respectively.
        matrix_text = [] # List that holds each line of ascii text representation of the matrix.
        row_string = "|_" 
        while j < self.num_columns - 2: # Generates placeholders, denoted by _ , which user will then replace with matrix entries.
            row_string +=  " _"
            j += 1
        row_string += " _|\n"
        while i < self.num_rows:
            matrix_text.append(row_string)
            i += 1
        return matrix_text # Returns list of text to be written to file.

    # Takes as an argument a list of lists of row values.
    # Sets the entries of the matrix accordingly.

    def set_entries(self, list_of_rows):
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                current_row = list_of_rows[i]
                self.entries[i][j] = float(current_row[j])

    # Adds a row of 0s to the matrix.
    
    def add_row(self):
        self.entries.append([0 for j in range(self.num_columns)])
        self.num_rows += 1

    # Adds a column of 0s to the matrix
    
    def add_column(self):
        for i in range(self.num_rows):
            self.entries[i].append(0)
        self.num_columns += 1

    # Removes the last row from the matrix.

    def remove_row(self):
        self.entries.pop()
        self.num_rows -= 1

    # Removes the last column from the matrix.

    def remove_column(self):
        for i in range(self.num_rows):
            self.entries[i].pop()
        self.num_columns -= 1

    def strassen_strip(self, desired_rows, desired_columns):
        if self.num_rows > desired_rows:
            while self.num_rows > desired_rows:
                self.remove_row()
        if self.num_columns > desired_columns:
            while self.num_columns > desired_columns:
                self.remove_column()
        return self

    # Writes text representations of num_matrices number of matrices with
    # dimensions given in dimension_list to the file file_to_write.
        
    def draw_blank_matrix(self, matrix_number, file_to_write):
        file_to_write.write("Matrix " + str(matrix_number) + ":\n\n") # Text that identifies which matrix the drawn diagram represents.
        matrix_text = self.format_matrix_text() # Get the text to be written to file
        for line in matrix_text:                # Write the aforementioned text to file_to_write.
            file_to_write.write(line)
        file_to_write.write("\n")

    def draw_matrix_output(self, file_to_write):
        file_to_write.write(str(self))
        

    

