# -*- coding: utf-8 -*-

# python imports
import struct

# project imports
from ..parser_core import Tokens


class HeaderGenerator:

    def __init__(self, code_editor):
        self._code_editor = code_editor


    def gen_header(self):
        self._code_editor.add_line("# -*- coding: utf-8 -*-\n")
        self._gen_imports()
        self._code_editor.add_line('\n')


    def _gen_imports(self):
        self._code_editor.add_line("# python imports")
        self._code_editor.add_line("import struct")
        self._code_editor.add_line("from enum import Enum")


###################################################################################
###################################################################################


class TypeGenerator:

    def __init__(self, code_editor):
        self._user_defined_types = {
            Tokens.Class: [],
            Tokens.Enum: {}
        }

        self._code_editor = code_editor
        self._initializer_generator = InitializerGenerator(self._user_defined_types, code_editor)
        self._serializer_generator = SerializerGenerator(self._user_defined_types, code_editor)
        self._deserializer_generator = DeserializerGenerator(self._user_defined_types, code_editor)


    def gen_type(self, type_name, properties):
        gen_func = getattr(self, '_gen_type_%s' % properties['_def'][0])
        gen_func(type_name, properties)



    def _gen_type_class(self, type_name, properties):
        code_editor = self._code_editor

        _def = properties.pop('_def')
        properties = sorted(properties.items())

        self._user_defined_types[Tokens.Class].append(type_name)
        parents = ['object'] if len(_def) == 1 else [p[0] for p in _def[1]]

        # generate definitions
        code_editor.add_line("class %s(%s):" % (type_name, ', '.join(parents)))
        code_editor.add_line()
        code_editor.increase_indentation()

        # generate constructor
        code_editor.add_line("def __init__(self, init=False):")
        code_editor.add_line("super(%s, self).__init__()" % type_name, 1)
        code_editor.add_line()
        code_editor.add_line("if init:", 1)
        code_editor.add_line("self.initialize()", 2)
        code_editor.add_line("else:", 1)
        for attr_name, tree in properties:
            attr_name = "self.%s" % attr_name
            code_editor.add_line("%s = None" % attr_name, 2)
        code_editor.add_line('\n')

        # generate initializer
        code_editor.add_line("def initialize(self):")
        code_editor.increase_indentation()

        if parents[0] != 'object':
            for parent in parents:
                code_editor.add_line("%s.initialize(self)" % parent)
            code_editor.add_line()

        for attr_name, tree in properties:
            attr_name = "self.%s" % attr_name
            self._initializer_generator.gen_initializer(attr_name, tree)

        code_editor.decrease_indentation()
        code_editor.add_line('\n')

        # generate serializer
        result_name = 's'
        code_editor.add_line("def serialize(self):")
        code_editor.increase_indentation()
        code_editor.add_line("%s = b''" % result_name)
        code_editor.add_line()

        if parents[0] != 'object':
            code_editor.add_line("# serialize parents")
            for parent in parents:
                code_editor.add_line("%s += %s.serialize(self)" % (result_name, parent))
            code_editor.add_line()

        for attr_name, tree in properties:
            attr_name = "self.%s" % attr_name
            code_editor.add_line("# serialize %s" % attr_name)
            self._serializer_generator.gen_serializer(attr_name, result_name, tree)
            code_editor.add_line()

        code_editor.add_line("return %s" % result_name)
        code_editor.decrease_indentation()
        code_editor.add_line('\n')

        # generate deserializer
        data_name = 's'
        offset_name = 'offset'
        code_editor.add_line("def deserialize(self, %s, %s=0):" % (data_name, offset_name))
        code_editor.increase_indentation()

        if parents[0] != 'object':
            code_editor.add_line("# deserialize parents")
            for parent in parents:
                code_editor.add_line("%s = %s.deserialize(self, %s, %s)" % 
                                     (offset_name, parent, data_name, offset_name))
            code_editor.add_line()

        for attr_name, tree in properties:
            attr_name = "self.%s" % attr_name
            code_editor.add_line("# deserialize %s" % attr_name)
            self._deserializer_generator.gen_deserializer(data_name, offset_name, attr_name, tree)
            code_editor.add_line()

        code_editor.add_line("return %s" % offset_name)
        code_editor.decrease_indentation()

        code_editor.decrease_indentation()


    def _gen_type_enum(self, type_name, properties):
        code_editor = self._code_editor

        _def = properties.pop('_def')
        self._user_defined_types[Tokens.Enum][type_name] = _def[1][0]
        value_type = _def[1][0][0]
        code_editor.add_line("class %s(Enum):" % type_name)

        value = 0
        for attr in _def[1][1]:
            name = attr[0]
            if len(attr) > 1:
                value = attr[1]
            code_editor.add_line("%s = %s" % (name, value), 1)
            value += 1


###################################################################################
###################################################################################


class InitializerGenerator:

    def __init__(self, user_defined_types, code_editor):
        self._simples_initial_value_table = {
            Tokens.Boolean: "bool()",
            Tokens.Char: "'\\x00'",
            Tokens.Byte: "int()",
            Tokens.UnsignedByte: "int()",
            Tokens.Short: "int()",
            Tokens.UnsignedShort: "int()",
            Tokens.Integer: "int()",
            Tokens.UnsignedInteger: "int()",
            Tokens.Long: "int()",
            Tokens.UnsignedLong: "int()",
            Tokens.Float: "float()",
            Tokens.Double: "int()",
            Tokens.String: "str()",
            Tokens.List: "list()",
            Tokens.Map: "dict()"
        }

        self._user_defined_types = user_defined_types
        self._code_editor = code_editor


    def gen_initializer(self, value_name, tree):
        initial_value = self._gen_initializer(tree)
        self._code_editor.add_line("%s = %s" % (value_name, initial_value))


    def _gen_initializer(self, tree):
        value_type = tree[0]
        initializer_func = None

        for type_token in self._user_defined_types:
            if value_type in self._user_defined_types[type_token]:
                initializer_func = getattr(self, '_gen_initializer_%s' % type_token)
                break

        if initializer_func is None:
            initializer_func = getattr(
                self,
                '_gen_initializer_%s' % value_type,
                self._gen_initializer_simples
            )

        return initializer_func(value_type, tree)



    def _gen_initializer_class(self, value_type, tree):
        return "%s()" % value_type


    def _gen_initializer_enum(self, value_type, tree):
        return "list(%s)[0]" % value_type


    def _gen_initializer_array(self, value_type, tree):
        dims = list(tree[1][0])
        dims.reverse()
        array_type = tree[1][1]

        initial_value = self._gen_initializer(array_type)
        for dim in dims:
            initial_value = "[%s for _ in range(%s)]" % (initial_value, dim)

        return initial_value


    def _gen_initializer_simples(self, value_type, tree):
        return self._simples_initial_value_table[value_type]


###################################################################################
###################################################################################


class SerializerGenerator:

    def __init__(self, user_defined_types, code_editor):
        self._simples_format_table = {
            Tokens.Boolean: '?',
            Tokens.Char: 'c',
            Tokens.Byte: 'b',
            Tokens.UnsignedByte: 'B',
            Tokens.Short: 'h',
            Tokens.UnsignedShort: 'H',
            Tokens.Integer: 'i',
            Tokens.UnsignedInteger: 'I',
            Tokens.Long: 'q',
            Tokens.UnsignedLong: 'Q',
            Tokens.Float: 'f',
            Tokens.Double: 'd'
        }

        self._user_defined_types = user_defined_types
        self._code_editor = code_editor


    def gen_serializer(self, value_name, result_name, tree):
        value_type = tree[0]
        serializer_func = None

        for type_token in self._user_defined_types:
            if value_type in self._user_defined_types[type_token]:
                serializer_func = getattr(self, '_gen_serializer_%s' % type_token)
                break

        if serializer_func is None:
            serializer_func = getattr(
                self,
                '_gen_serializer_%s' % value_type,
                self._gen_serializer_simples
            )

        serializer_func(value_name, result_name, tree)



    def _gen_serializer_class(self, value_name, result_name, tree):
        self._code_editor.add_line("%s += %s.serialize()" % (result_name, value_name))


    def _gen_serializer_enum(self, value_name, result_name, tree):
        self._gen_serializer_simples(
            "%s.value" % value_name,
            result_name,
            self._user_defined_types[Tokens.Enum][tree[0]]
        )


    def _gen_serializer_list(self, value_name, result_name, tree):
        code_editor = self._code_editor

        # gen size
        self._gen_size(value_name, result_name, tree)

        # gen items
        item = code_editor.new_tempvar()
        code_editor.add_line("for %s in %s:" % (item, value_name))
        code_editor.increase_indentation()
        self.gen_serializer(item, result_name, tree[1])
        code_editor.decrease_indentation()


    def _gen_serializer_map(self, value_name, result_name, tree):
        code_editor = self._code_editor

        # gen size
        self._gen_size(value_name, result_name, tree)

        # gen items
        key = code_editor.new_tempvar()
        code_editor.add_line("for %s in %s:" % (key, value_name))
        code_editor.increase_indentation()
        self.gen_serializer(key, result_name, tree[1][0])
        self.gen_serializer("%s[%s]" % (value_name, key), result_name, tree[1][1])
        code_editor.decrease_indentation()


    def _gen_serializer_array(self, value_name, result_name, tree):
        code_editor = self._code_editor

        dims = tree[1][0]
        array_type = tree[1][1]

        indexes = []
        for i in range(len(dims)):
            index = code_editor.new_tempvar()
            indexes.append(index)
            code_editor.add_line("for %s in range(%s):" % (index, dims[i]), i)

        code_editor.increase_indentation(len(dims))
        value_name += "[%s]" % ']['.join(indexes)
        self.gen_serializer(value_name, result_name, array_type)
        code_editor.decrease_indentation(len(dims))


    def _gen_serializer_string(self, value_name, result_name, tree):
        # gen size
        self._gen_size(value_name, result_name, tree)

        # gen string
        self._code_editor.add_line("%s += %s.encode('ascii')" % (result_name, value_name))


    def _gen_serializer_char(self, value_name, result_name, tree):
        value_name = "%s.encode('ascii')" % value_name
        self._gen_serializer_simples(value_name, result_name, tree)


    def _gen_serializer_simples(self, value_name, result_name, tree):
        fmt = self._simples_format_table[tree[0]]
        self._code_editor.add_line("%s += struct.pack('%s', %s)" % (result_name, fmt, value_name))


    def _gen_size(self, value_name, result_name, tree):
        code_editor = self._code_editor

        size = code_editor.new_tempvar()
        code_editor.add_line("%s = b''" % size)
        self._gen_serializer_simples("len(%s)" % value_name, size, (Tokens.UnsignedInteger, ))
        code_editor.add_line("while len(%s) and %s[-1] == b'\\x00'[0]:" % (size, size))
        code_editor.add_line("%s = %s[:-1]" % (size, size), 1)

        self._gen_serializer_simples("len(%s)" % size, result_name, (Tokens.UnsignedByte, ))
        code_editor.add_line("%s += %s" % (result_name, size))
        code_editor.add_line()


###################################################################################
###################################################################################


class DeserializerGenerator:

    def __init__(self, user_defined_types, code_editor):
        self._simples_format_table = {
            Tokens.Boolean: '?',
            Tokens.Char: 'c',
            Tokens.Byte: 'b',
            Tokens.UnsignedByte: 'B',
            Tokens.Short: 'h',
            Tokens.UnsignedShort: 'H',
            Tokens.Integer: 'i',
            Tokens.UnsignedInteger: 'I',
            Tokens.Long: 'q',
            Tokens.UnsignedLong: 'Q',
            Tokens.Float: 'f',
            Tokens.Double: 'd'
        }

        self._simples_fmtsize_table = {
            key: struct.calcsize(val) for key, val in self._simples_format_table.items()
        }

        self._user_defined_types = user_defined_types
        self._code_editor = code_editor



    def _get_data(self, data_name, offset_name, length):
        return "%s[%s:%s + %s]" % (data_name, offset_name, offset_name, length)

    def _increase_offset(self, offset_name, n):
        self._code_editor.add_line("%s += %s" % (offset_name, n))



    def gen_deserializer(self, data_name, offset_name, value_name, tree):
        value_type = tree[0]
        deserializer_func = None

        for type_token in self._user_defined_types:
            if value_type in self._user_defined_types[type_token]:
                deserializer_func = getattr(self, '_gen_deserializer_%s' % type_token)
                break

        if deserializer_func is None:
            deserializer_func = getattr(
                self,
                '_gen_deserializer_%s' % value_type,
                self._gen_deserializer_simples
            )

        deserializer_func(data_name, offset_name, value_name, tree)



    def _gen_deserializer_class(self, data_name, offset_name, value_name, tree):
        code_editor = self._code_editor

        code_editor.add_line("if %s is None:" % value_name)
        code_editor.add_line("%s = %s()" % (value_name, tree[0]), 1)
        code_editor.add_line("%s = %s.deserialize(%s, %s)" % 
                             (offset_name, value_name, data_name, offset_name))


    def _gen_deserializer_enum(self, data_name, offset_name, value_name, tree):
        code_editor = self._code_editor

        enum_type = tree[0]
        val = code_editor.new_tempvar()
        self._gen_deserializer_simples(
            data_name,
            offset_name,
            val,
            self._user_defined_types[Tokens.Enum][tree[0]]
        )
        code_editor.add_line("%s = %s(%s)" % (value_name, enum_type, val))


    def _gen_deserializer_list(self, data_name, offset_name, value_name, tree):
        code_editor = self._code_editor

        # gen size
        size = self._gen_size(data_name, offset_name, value_name, tree)

        # gen items
        code_editor.add_line("%s = []" % value_name)
        i = code_editor.new_tempvar()
        code_editor.add_line("for %s in range(%s):" % (i, size))
        item = code_editor.new_tempvar()
        code_editor.increase_indentation()
        self.gen_deserializer(data_name, offset_name, item, tree[1])
        code_editor.add_line("%s.append(%s)" % (value_name, item))
        code_editor.decrease_indentation()


    def _gen_deserializer_map(self, data_name, offset_name, value_name, tree):
        code_editor = self._code_editor

        # gen size
        size = self._gen_size(data_name, offset_name, value_name, tree)

        # gen items
        code_editor.add_line("%s = {}" % value_name)
        i = code_editor.new_tempvar()
        code_editor.add_line("for %s in range(%s):" % (i, size))
        key = code_editor.new_tempvar()
        val = code_editor.new_tempvar()
        code_editor.increase_indentation()
        self.gen_deserializer(data_name, offset_name, key, tree[1][0])
        self.gen_deserializer(data_name, offset_name, val, tree[1][1])
        code_editor.add_line("%s[%s] = %s" % (value_name, key, val))
        code_editor.decrease_indentation()


    def _gen_deserializer_array(self, data_name, offset_name, value_name, tree):
        code_editor = self._code_editor

        dims = tree[1][0]
        array_type = tree[1][1]

        indexes = []
        for i in range(len(dims)):
            index = code_editor.new_tempvar()
            indexes.append(index)
            code_editor.add_line("for %s in range(%s):" % (index, dims[i]), i)

        code_editor.increase_indentation(len(dims))
        value_name += "[%s]" % ']['.join(indexes)
        self.gen_deserializer(data_name, offset_name, value_name, array_type)
        code_editor.decrease_indentation(len(dims))


    def _gen_deserializer_string(self, data_name, offset_name, value_name, tree):
        # gen size
        size = self._gen_size(data_name, offset_name, value_name, tree)

        # gen string
        self._code_editor.add_line("%s = %s.decode('utf-8')" % 
                                   (value_name, self._get_data(data_name, offset_name, size)))
        self._increase_offset(offset_name, size)


    def _gen_deserializer_char(self, data_name, offset_name, value_name, tree):
        self._gen_deserializer_simples(data_name, offset_name, value_name, tree)
        self._code_editor.add_line("%s = %s.decode('utf-8')" % (value_name, value_name))


    def _gen_deserializer_simples(self, data_name, offset_name, value_name, tree):
        fmt = self._simples_format_table[tree[0]]
        size = self._simples_fmtsize_table[tree[0]]
        data = data_name if offset_name is None else self._get_data(data_name, offset_name, size)
        self._code_editor.add_line("%s = struct.unpack('%s', %s)[0]" % 
                                   (value_name, fmt, data))
        if offset_name is not None:
            self._increase_offset(offset_name, size)


    def _gen_size(self, data_name, offset_name, value_name, tree):
        code_editor = self._code_editor

        size_len = code_editor.new_tempvar()
        self._gen_deserializer_simples(data_name, offset_name, size_len, (Tokens.UnsignedByte, ))
        size_bytes = code_editor.new_tempvar()
        code_editor.add_line("%s = %s" % (size_bytes, self._get_data(data_name, offset_name, size_len)))
        self._increase_offset(offset_name, size_len)
        code_editor.add_line("%s += b'\\x00' * (%s - %s)" % 
                             (size_bytes, self._simples_fmtsize_table[Tokens.UnsignedInteger], size_len))
        size = code_editor.new_tempvar()
        self._gen_deserializer_simples(size_bytes, None, size, (Tokens.UnsignedInteger, ))
        code_editor.add_line()

        return size