from semantic_table import *


class Quadruple(object):
    def __init__(self, operator, operand_1, operand_2, result_id):
        self.operator = operator
        self.operand_1 = operand_1
        self.operand_2 = operand_2
        self.result_id = result_id

    def __divide_expression(expression):
        exp = []
        operand = ""
        i = 0

        while i < len(expression):
            if expression[i] in [
                "+",
                "-",
                "*",
                "/",
                "%",
                "(",
                ")",
                ">",
                "<",
                "=",
                "|",
                "&",
                "!",
            ]:
                if len(operand):
                    exp.append(operand)

                symbol = expression[i]

                if symbol in ["<", ">", "=", "!"] and expression[i + 1] == "=":
                    symbol += "="
                    i += 1

                if symbol in ["|", "&"] and expression[i + 1] == symbol:
                    symbol += symbol
                    i += 1

                exp.append(symbol)
                operand = ""

            else:
                operand += expression[i]

            i += 1

        if len(operand):
            exp.append(operand)

        return exp

    def __sub_stack_from_parentheses(stack):
        if "(" in stack:
            stack.reverse()
            index = stack.index("(")
            sub_stack = stack[:index]
            stack.reverse()

            return sub_stack

        return stack

    def __another_op_mdr_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return any(item in ["MUL", "DIV", "MOD"] for item in sub_stack_operators)

    def __another_op_as_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return any(item in ["ADD", "SUB"] for item in sub_stack_operators)

    def __another_op_as_mdr_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return any(
            item in ["MUL", "DIV", "MOD", "ADD", "SUB"] for item in sub_stack_operators
        )

    def __another_op_as_mdr_comp_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return any(
            item in ["MUL", "DIV", "MOD", "ADD", "SUB", "GT", "LT", "GTE", "LTE"]
            for item in sub_stack_operators
        )

    def __a_not_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return "NOT" in sub_stack_operators

    def __any_op_in_stack(stack_operators):
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return True if len(sub_stack_operators) else False

    def __another_comparator_or_matcher_in_stack():
        sub_stack_operators = Quadruple.__sub_stack_from_parentheses(stack_operators)
        return any(
            item in Quadruple.__comparators_and_matchers for item in sub_stack_operators
        )

    def __generate_quadruple(
        stack_values, stack_operators, result_quadruple_id, final_ops
    ):
        result_id = "T" + str(result_quadruple_id)

        q = Quadruple(
            stack_operators.pop(), stack_values[-2], stack_values[-1], result_id
        )

        del stack_values[-2:]

        final_ops.append(q)
        stack_values.append(result_id)

    def __generate_not_quadruple(
        stack_values, stack_operators, result_quadruple_id, final_ops
    ):
        result_id = "T" + str(result_quadruple_id)
        q = Quadruple(stack_operators.pop(), stack_values.pop(), None, result_id)

        final_ops.append(q)
        stack_values.append(result_id)

    # TODO: Todavía no considera tipos basados en la tabla semantica
    def arithmetic_expression(expression):
        # Examples:
        stack_values = []  # ["A", "B"]
        stack_operators = []  # ["ADD"]
        stack_types = []  # ["INT", "FLT"]

        final_ops = []
        result_quadruple_id = 1

        for symbol in Quadruple.format_expression(expression):
            s_type = symbol.type
            s_name = symbol.name

            # is it is a ! operator
            if s_type == "not":
                stack_operators.append("NOT")

            elif s_type in SemanticTable.types:
                stack_values.append(s_name)
                stack_types.append(s_type)

                if Quadruple.__a_not_in_stack(stack_operators):
                    Quadruple.__generate_not_quadruple(
                        stack_values, stack_operators, result_quadruple_id, final_ops
                    )
                    result_quadruple_id += 1

            # is an operator
            elif s_type in ["operation", "comparison", "matching"]:

                # Multiplication, Divition and Residue cases
                if s_name in ["MUL", "DIV", "MOD"]:

                    # There is another operator of multiplication, division or residue
                    if Quadruple.__another_op_mdr_in_stack(stack_operators):
                        Quadruple.__generate_quadruple(
                            stack_values,
                            stack_operators,
                            result_quadruple_id,
                            final_ops,
                        )
                        result_quadruple_id += 1

                # Addition and substraction cases
                elif s_name in ["ADD", "SUB"]:

                    # There is another operator on the stack
                    if Quadruple.__another_op_as_mdr_in_stack(stack_operators):
                        Quadruple.__generate_quadruple(
                            stack_values,
                            stack_operators,
                            result_quadruple_id,
                            final_ops,
                        )
                        result_quadruple_id += 1

                        # There is another operator of sum or addition
                        if Quadruple.__another_op_as_in_stack(stack_operators):
                            Quadruple.__generate_quadruple(
                                stack_values,
                                stack_operators,
                                result_quadruple_id,
                                final_ops,
                            )
                            result_quadruple_id += 1

                # Comparison operators case
                elif s_name in ["GT", "LT", "GTE", "LTE"]:

                    # There is another mathematical and comparison operator on the stack
                    if Quadruple.__another_op_as_mdr_comp_in_stack(stack_operators):
                        Quadruple.__generate_quadruple(
                            stack_values,
                            stack_operators,
                            result_quadruple_id,
                            final_ops,
                        )
                        result_quadruple_id += 1

                        # There is another mathematical operator in stack
                        if Quadruple.__another_op_as_mdr_in_stack(stack_operators):
                            Quadruple.__generate_quadruple(
                                stack_values,
                                stack_operators,
                                result_quadruple_id,
                                final_ops,
                            )
                            result_quadruple_id += 1

                            # There is another operator of sum or addition
                            if Quadruple.__another_op_as_in_stack(stack_operators):
                                Quadruple.__generate_quadruple(
                                    stack_values,
                                    stack_operators,
                                    result_quadruple_id,
                                    final_ops,
                                )
                                result_quadruple_id += 1

                # matching operators case
                elif s_name in ["BEQ", "BNEQ", "OR", "AND"]:

                    # There is any another operator on the stack
                    if Quadruple.__any_op_in_stack(stack_operators):
                        Quadruple.__generate_quadruple(
                            stack_values,
                            stack_operators,
                            result_quadruple_id,
                            final_ops,
                        )
                        result_quadruple_id += 1

                        # There is another mathematical and comparison operator on the stack
                        if Quadruple.__another_op_as_mdr_comp_in_stack(stack_operators):
                            Quadruple.__generate_quadruple(
                                stack_values,
                                stack_operators,
                                result_quadruple_id,
                                final_ops,
                            )
                            result_quadruple_id += 1

                            # There is another mathematical operator in stack
                            if Quadruple.__another_op_as_mdr_in_stack(stack_operators):
                                Quadruple.__generate_quadruple(
                                    stack_values,
                                    stack_operators,
                                    result_quadruple_id,
                                    final_ops,
                                )
                                result_quadruple_id += 1

                                # There is another operator of sum or addition
                                if Quadruple.__another_op_as_in_stack(stack_operators):
                                    Quadruple.__generate_quadruple(
                                        stack_values,
                                        stack_operators,
                                        result_quadruple_id,
                                        final_ops,
                                    )
                                    result_quadruple_id += 1

                stack_operators.append(s_name)

            # is a parentheses
            elif s_type == "parentheses":
                # When a ( arrives
                if s_name == "OP":
                    stack_values.append("(")
                    stack_operators.append("(")

                # When a ) arrives
                elif s_name == "CP":
                    # case when there is just one value inside parenthesis example: A + (B)
                    if len(stack_operators) == 0:
                        stack_values.pop(-2)
                        stack_operators.pop()

                    else:
                        while stack_operators[-1] != "(":
                            Quadruple.__generate_quadruple(
                                stack_values,
                                stack_operators,
                                result_quadruple_id,
                                final_ops,
                            )

                            result_quadruple_id += 1

                        stack_operators.pop()
                        stack_values.pop(-2)

            # is an unknown character
            else:
                return "error: type {} not found".format(s_type)

        while len(stack_operators):
            Quadruple.__generate_quadruple(
                stack_values, stack_operators, result_quadruple_id, final_ops
            )
            result_quadruple_id += 1

        return final_ops

    def format_quadruple(self):
        return "{} {} {} {}".format(
            self.operator, self.operand_1, self.operand_2, self.result_id
        )

    def format_expression(expression):
        response = []

        if type(expression) == str:
            expression = expression.replace(" ", "")
            expression = Quadruple.__divide_expression(expression)

        for symbol in expression:
            s_type = type(symbol)

            if s_type == Symbol:
                response.append(symbol)

            elif s_type == str:
                operators = {
                    "+": Symbol("ADD", "operation"),
                    "-": Symbol("SUB", "operation"),
                    "*": Symbol("MUL", "operation"),
                    "/": Symbol("DIV", "operation"),
                    "%": Symbol("MOD", "operation"),
                    "(": Symbol("OP", "parentheses"),
                    ")": Symbol("CP", "parentheses"),
                    "!": Symbol("NOT", "not"),
                    "<": Symbol("LT", "comparison"),
                    ">": Symbol("GT", "comparison"),
                    "<=": Symbol("LTE", "comparison"),
                    ">=": Symbol("GTE", "comparison"),
                    "==": Symbol("BEQ", "matching"),
                    "!=": Symbol("BNEQ", "matching"),
                    "||": Symbol("OR", "matching"),
                    "&&": Symbol("AND", "matching"),
                }

                response.append(operators.get(symbol, Symbol(symbol, "FLT")))

        return response
