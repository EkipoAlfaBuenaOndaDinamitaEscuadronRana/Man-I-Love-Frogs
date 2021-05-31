from router_solver import *
import compilador.objects.symbol
from compilador.objects.symbol import *


class MemorySegment(object):
    def __init__(self, name, size, initial_position):
        self.name = name
        self.size = size
        self.__memory = dict()
        self.__memory_values = dict()
        self.__symbol_directions = dict()
        self.__subsegment_size = size // 7
        self.initial_position = initial_position

        self.ints = 0
        self.flts = self.__subsegment_size
        self.strs = self.__subsegment_size * 2
        self.chars = self.__subsegment_size * 3
        self.bools = self.__subsegment_size * 4
        self.nulls = self.__subsegment_size * 5
        self.frogs = self.__subsegment_size * 6

        self.spare_memory_ints = self.__subsegment_size
        self.spare_memory_flts = self.__subsegment_size
        self.spare_memory_strs = self.__subsegment_size
        self.spare_memory_chars = self.__subsegment_size
        self.spare_memory_bools = self.__subsegment_size
        self.spare_memory_nulls = self.__subsegment_size
        self.spare_memory_frogs = self.__subsegment_size

    def __get_memory_inital_direction(self, s_type):
        type_inital_position = {
            "INT": self.ints,
            "FLT": self.flts,
            "STR": self.strs,
            "CHAR": self.chars,
            "BOOL": self.bools,
            "NULL": self.nulls,
            "FROG": self.frogs,
        }

        return type_inital_position[s_type]

    def __get_spare_memory(self, s_type):
        left_memory = {
            "INT": self.spare_memory_ints,
            "FLT": self.spare_memory_flts,
            "STR": self.spare_memory_strs,
            "CHAR": self.spare_memory_chars,
            "BOOL": self.spare_memory_bools,
            "NULL": self.spare_memory_nulls,
            "FROG": self.spare_memory_frogs,
        }

        return left_memory[s_type]

    def __get_symbol_position(self, s_type):
        return (
            self.__subsegment_size
            - self.__get_spare_memory(s_type)
            + self.__get_memory_inital_direction(s_type)
        )

    def __substract_memory(self, symbol):
        s_type = symbol.type
        s_size = symbol.memory_size()

        if s_type == "INT":
            self.spare_memory_ints -= s_size

        elif s_type == "FLT":
            self.spare_memory_flts -= s_size

        elif s_type == "STR":
            self.spare_memory_strs -= s_size

        elif s_type == "CHAR":
            self.spare_memory_chars -= s_size

        elif s_type == "BOOL":
            self.spare_memory_bools -= s_size

        elif s_type == "NULL":
            self.spare_memory_nulls -= s_size

        elif s_type == "FROG":
            self.spare_memory_frogs -= s_size

    # TODO: Does not assign arrays
    def __assign_memory(self, symbol, symbol_position):
        # Scalar
        if type(symbol) == Symbol:
            symbol.segment_direction = symbol_position
            symbol.global_direction = self.initial_position + symbol_position
            self.__memory[symbol_position] = symbol
            self.__memory_values[symbol_position] = symbol.value
            if self.name == "Constant Segment":
                symbol.value = symbol.name
                self.__memory_values[symbol_position] = symbol.name
        # Two- or three-dimensional array
        else:
            pass

    # TODO: Does not work with arrays
    def insert_symbol(self, symbol):
        s_type = symbol.type
        initial_position = self.__get_memory_inital_direction(s_type)
        symbol_position = self.__get_symbol_position(s_type)
        s_size = symbol.memory_size()

        if symbol_position + s_size - 1 < initial_position + self.__subsegment_size:
            self.__assign_memory(symbol, symbol_position)
            self.__substract_memory(symbol)

            return True

        return False

    def modify_address(self, symbol, address):
        if address not in self.__memory.keys():
            self.__assign_memory(symbol, address)

    def search_symbol(self, direction):
        direction = direction - self.initial_position
        return self.__memory.get(direction, None)

    def search_value(self, direction):
        direction = direction - self.initial_position
        return self.__memory_values.get(direction, None)

    def modify_value(self, direction, value):
        direction = direction - self.initial_position
        self.__memory_values[direction] = value

    def print_memory_segment(self):
        print("##### MEMORY ", self.name, " ##########")
        for space in self.__memory:
            self.__memory[space].print_symbol()
            print("SAVED_VALUE:", self.__memory_values[space])
            print("................")
        # print(self.__memory_values)

    def save_local_memory(self):
        local_data = {}
        for space in self.__memory:
            local_data[space] = self.__memory[space].value

        return local_data

    def erase_local_memory(self):
        for space in self.__memory:
            self.__memory[space].segment_direction = None
            self.__memory[space].global_direction = None
            self.__memory_values[space] = None

    def backtrack_memory(self, frozen_memory):
        for k, v in frozen_memory.items():
            self.__memory[k].value = v
            self.__memory[k].segment_direction = k
            self.__memory[k].global_direction = k + self.initial_position
