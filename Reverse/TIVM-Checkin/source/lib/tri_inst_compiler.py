

TI_ARGTYPE_INSTANT = 0x1
TI_ARGTYPE_OFFSET = 0x2
TI_ARGTYPE_LABEL = 0x4

# 基础指令
TI_INST_SUB_OO = 0x1
TI_INST_JMP_I = 0x2
TI_INST_PUT_O = 0x3
TI_INST_GET_O = 0x4
TI_INST_RAW_I = 0x5
TI_INST_SUBJLE_OOI = 0x6

# 复合指令
TI_INST_SUB_OI = 0x11
TI_INST_PUT_I = 0x12
TI_INST_CHKJEQ_OOI = 0x13
TI_INST_CHKJNE_OOI = 0x14
TI_INST_SUBJG_OOI = 0x15
TI_INST_SUBJLE_OII = 0x16
TI_INST_CHKJEQ_OII = 0x17
TI_INST_CHKJG_OOI = 0x18
TI_INST_CHKJG_OII = 0x19
TI_INST_MOV_OO = 0x1a   # [a0] <- [a1]
TI_INST_MOV_OI = 0x1b   # [a0] <- a1
TI_INST_LOD_OO = 0x1c   # [a0] <- [[a1]]
TI_INST_LOD_OOI = 0x1d  # [a0] <- [[a1] + a2]
TI_INST_SAV_OO = 0x1e   # [[a0]] <- [a1]
TI_INST_SAV_OOI = 0x1f  # [[a0] + a2] <- [a1]
TI_INST_SUBJGE_OOI = 0x20   # sub [a0], [a1]; jmp #a2 if [a0] >= 0  # 可能不需要
TI_INST_SUBJGE_OII = 0x21   # sub [a0], #a1 ; jmp #a2 if [a0] >= 0  # 可能不需要
TI_INST_CHKJGE_OOI = 0x22   # jmp #a2 if [a0] >= [a1]
TI_INST_CHKJGE_OII = 0x23   # jmp #a2 if [a0] >= #a1
TI_INST_CHKJLE_OOI = 0x24   # jmp #a2 if [a0] <= [a1]
TI_INST_CHKJLE_OII = 0x25   # jmp #a2 if [a0] <= #a1
TI_INST_CHKJNE_OII = 0x26
# max at 0x21

# makeing

class InstNotDefinedError(BaseException) : ...

class TriInstCompiler:
    def __init__(self) -> None:
        self.inst_type2length = {   # not used
            TI_INST_SUB_OO : 3,
            TI_INST_JMP_I : 3,
            TI_INST_PUT_O : 3,
            TI_INST_GET_O : 3,
            TI_INST_RAW_I : 1,
            TI_INST_SUBJLE_OOI : 3,
        }
        self.label2addr = {}
        self.simple_insts = set([TI_INST_SUB_OO, TI_INST_JMP_I, TI_INST_PUT_O, TI_INST_GET_O, TI_INST_RAW_I, TI_INST_SUBJLE_OOI])
    '''
    def _ti_compile_parse_get_value(self, arg : str, addr : int) -> int:
        if arg.startswith('#'):
            # if arg[1] == '-' or arg[1] == '~':
            if arg[1] == '-':
                return 0x100000000 - int(arg[2:], base=16)
            else:
                return int(arg[1:], base=16)
        elif arg.startswith('$'):
            return addr + int(arg[1:], base=16)
        elif arg.startswith('%'):
            return arg[1:]

        raise ValueError('bad arg: %s' % arg)
    '''

    def _ti_compile_parse_arg_get_value(self, arg_info : list, arg : str, addr : int):
        if arg.startswith('#'):
            if arg[1] == '-':
                arg_info[1] = 0x100000000 - int(arg[2:], base=16)
            else:
                arg_info[1] = int(arg[1:], base=16)
        elif arg.startswith('$'):
            arg_info[1] = addr + int(arg[1:], base=16)
        elif arg.startswith('%'):
            arg_info[0] |= TI_ARGTYPE_LABEL
            arg_info[1] = arg[1:]

            r = None
            t = arg.rfind('-')
            if t != -1:
                r = arg[t:]
                arg_info[1] = arg[1:t]
            t = arg.rfind('+')
            if t != -1:
                r = arg[t:]
                arg_info[1] = arg[1:t]
            if r != None:
                arg_info[2] = int(r, base=16)
        else:
            raise ValueError('bad arg: %s' % arg)

    def _log_debug(self, info : str):
        print('[tic debug] %s' % info)

    '''
    # returns [arg_type, value, offset]
    def _ti_compile_parse_arg_32(self, arg : str, addr : int) -> list[int]:
        result = [-1, -1, 0] # type, value, offset
        if arg.startswith('#'):
            result[0] = TI_ARGTYPE_INSTANT
            # if arg[1] == '-' or arg[1] == '~': # 取反
            if arg[1] == '-': # 取反
                t = 0x100000000 - int(arg[2:], base=16)
            else:
                t = int(arg[1:], base=16)
            result[1] = t
        elif arg.startswith('$'):
            result[0] = TI_ARGTYPE_INSTANT
            t = addr + int(arg[1:], base=16)
            result[1] = t
        elif arg.startswith('%'):
            result[0] = TI_ARGTYPE_LABEL | TI_ARGTYPE_INSTANT
            result[1] = arg[1:]
        elif arg.startswith('['):
            result[0] = TI_ARGTYPE_OFFSET
            t = arg[1:arg.rfind(']')]
            # if t.startswith('%'):
            #     result[0] |= TI_ARGTYPE_LABEL
            # t = self._ti_compile_parse_get_value(t, addr)
            # result[1] = t
            self._ti_compile_parse_arg_get_value(result, t, addr)
        return tuple(result)
    '''
    # returns [arg_type, value, offset]
    def _ti_compile_parse_arg_32(self, arg : str, addr : int) -> list[int]:
        result = [-1, -1, 0] # type, value, offset

        if arg.startswith('['):
            result[0] = TI_ARGTYPE_OFFSET
            t = arg[1:arg.rfind(']')]
            self._ti_compile_parse_arg_get_value(result, t, addr)
        else:
            result[0] = TI_ARGTYPE_INSTANT
            self._ti_compile_parse_arg_get_value(result, arg, addr)

        if result[0] & TI_ARGTYPE_LABEL:
            return tuple(result)
        else:
            return tuple(result[:2])

    def _ti_compile_get_inst_type(self, inst : str, parsed_args : list) -> int:
        inst_type = -1
        if   inst == 'sub':
            if   parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_OFFSET:
                inst_type = TI_INST_SUB_OO
            elif parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_SUB_OI
        elif inst == 'jmp':
            if   parsed_args[0][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_JMP_I
        elif inst == 'put':
            if   parsed_args[0][0] & TI_ARGTYPE_OFFSET:
                inst_type = TI_INST_PUT_O
            elif parsed_args[0][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_PUT_I
        elif inst == 'get':
            if   parsed_args[0][0] & TI_ARGTYPE_OFFSET:
                inst_type = TI_INST_GET_O
        elif inst == 'raw':
            if   parsed_args[0][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_RAW_I
        elif inst == 'sub-jle':
            if   parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_OFFSET and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_SUBJLE_OOI
            elif parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_INSTANT and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_SUBJLE_OII
        elif inst == 'sub-jg':
            if   parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_OFFSET and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_SUBJG_OOI
        elif inst == 'sub-jge':
            if   parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_OFFSET and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_SUBJGE_OOI
            elif parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_INSTANT and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_SUBJGE_OII
        elif inst == 'chk-jeq':
            if   parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_OFFSET and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_CHKJEQ_OOI
            elif parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_INSTANT and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_CHKJEQ_OII
        elif inst == 'chk-jne':
            if   parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_OFFSET and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_CHKJNE_OOI
            elif parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_INSTANT and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_CHKJNE_OII
        elif inst == 'chk-jg':
            if   parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_OFFSET and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_CHKJG_OOI
            elif parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_INSTANT and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_CHKJG_OII
        elif inst == 'chk-jle':
            if   parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_OFFSET and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_CHKJLE_OOI
            elif parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_INSTANT and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_CHKJLE_OII
        elif inst == 'chk-jge':
            if   parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_OFFSET and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_CHKJGE_OOI
            elif parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_INSTANT and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_CHKJGE_OII
        elif inst == 'mov':
            if   parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_OFFSET:
                inst_type = TI_INST_MOV_OO
            elif parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_MOV_OI
        elif inst == 'lod':
            if   len(parsed_args) == 2 and parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_OFFSET:
                inst_type = TI_INST_LOD_OO
            elif parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_OFFSET and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_LOD_OOI
        elif inst == 'sav':
            if   len(parsed_args) == 2 and parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_OFFSET:
                inst_type = TI_INST_SAV_OO
            elif parsed_args[0][0] & TI_ARGTYPE_OFFSET and parsed_args[1][0] & TI_ARGTYPE_OFFSET and parsed_args[2][0] & TI_ARGTYPE_INSTANT:
                inst_type = TI_INST_SAV_OOI
        else:
            raise InstNotDefinedError('inst "%s" is not defined' % inst)

        if inst_type == -1:
            raise InstNotDefinedError('invalid args for inst "%s": %s' % (inst, str(parsed_args)))

        return inst_type

    def _ti_compile_inst_32(self, inst_type : int, parsed_args : list, addr : int) -> list[int]:
        # 处理label
        # for _arg in parsed_args:
        #     if _arg[0] & TI_ARGTYPE_LABEL:
        #         _arg[1] = self._get_label(_arg[1])
        #         _arg[0] &= ~TI_ARGTYPE_LABEL
        for i in range(len(parsed_args)):
            _arg = parsed_args[i]
            if _arg[0] & TI_ARGTYPE_LABEL:
                parsed_args[i] = (_arg[0] & ~TI_ARGTYPE_LABEL, self._get_label(_arg[1]) + _arg[2])

        # 基础指令
        if   inst_type == TI_INST_SUB_OO:
            return [parsed_args[1][1], parsed_args[0][1], addr + 3]
        elif inst_type == TI_INST_JMP_I:
            return [0, 0, parsed_args[0][1]]
        elif inst_type == TI_INST_PUT_O:
            return [parsed_args[0][1], 0xffffffff, addr + 3]
        elif inst_type == TI_INST_GET_O:
            return [0xffffffff, parsed_args[0][1], addr + 3]
        elif inst_type == TI_INST_RAW_I:
            return [parsed_args[0][1]]
        elif inst_type == TI_INST_SUBJLE_OOI:
            return [parsed_args[1][1], parsed_args[0][1], parsed_args[2][1]]
        else:
            raise InstNotDefinedError('not implement: %s' % str(inst_type))

    def _is_simple_inst(self, inst : int) -> bool:
        return inst in self.simple_insts

    def _ti_compile_expand_complex_inst(self, inst_and_args, addr : int) -> list:
        inst_type, args = inst_and_args
        if   inst_type == TI_INST_SUB_OI:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 4)]),
                (TI_INST_RAW_I, [args[1]]),
                (TI_INST_SUB_OO, [args[0], (TI_ARGTYPE_OFFSET, addr + 3)]),
            ]
        elif inst_type == TI_INST_PUT_I:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 4)]),
                (TI_INST_RAW_I, [args[0]]),
                (TI_INST_PUT_O, [(TI_ARGTYPE_OFFSET, addr + 3)]),
            ]
        elif inst_type == TI_INST_CHKJEQ_OOI:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr+5)]),
                (TI_INST_RAW_I, [(TI_ARGTYPE_INSTANT, 0)]),
                (TI_INST_RAW_I, [(TI_ARGTYPE_INSTANT, 0)]),
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 3)]),
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), args[0]]),
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 4), (TI_ARGTYPE_OFFSET, addr + 4)]),
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 4), args[1]]),
                (TI_INST_SUBJLE_OOI, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 4), (TI_ARGTYPE_INSTANT, addr + 23)]),#17
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 29)]),
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 4), (TI_ARGTYPE_OFFSET, addr + 4)]),#23
                (TI_INST_SUBJLE_OOI, [(TI_ARGTYPE_OFFSET, addr + 4), (TI_ARGTYPE_OFFSET, addr + 3), args[2]]),#26
            ]
        elif inst_type == TI_INST_CHKJNE_OOI:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr+5)]),
                (TI_INST_RAW_I, [(TI_ARGTYPE_INSTANT, 0)]),
                (TI_INST_RAW_I, [(TI_ARGTYPE_INSTANT, 0)]),
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 3)]),
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), args[0]]),
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 4), (TI_ARGTYPE_OFFSET, addr + 4)]),
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 4), args[1]]),
                (TI_INST_SUBJLE_OOI, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 4), (TI_ARGTYPE_INSTANT, addr + 23)]),#17
                (TI_INST_JMP_I, [args[2]]),
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 4), (TI_ARGTYPE_OFFSET, addr + 4)]),#23
                (TI_INST_SUBJLE_OOI, [(TI_ARGTYPE_OFFSET, addr + 4), (TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_INSTANT, addr + 32)]),#26
                (TI_INST_JMP_I, [args[2]]),#29
            ]
        elif inst_type == TI_INST_CHKJNE_OII:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 4)]),
                (TI_INST_RAW_I, [args[1]]),
                (TI_INST_CHKJNE_OOI, [args[0], (TI_ARGTYPE_OFFSET, addr + 3), args[2]]),
            ]
        elif inst_type == TI_INST_SUBJG_OOI:
            return [
                (TI_INST_SUBJLE_OOI, [args[0], args[1], (TI_ARGTYPE_INSTANT, addr + 6)]),
                (TI_INST_JMP_I, [args[2]]),
            ]
        elif inst_type == TI_INST_SUBJLE_OII:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 4)]),
                (TI_INST_RAW_I, [args[1]]),#3
                (TI_INST_SUBJLE_OOI, [args[0], (TI_ARGTYPE_OFFSET, addr + 3), args[2]]),
            ]
        elif inst_type == TI_INST_CHKJEQ_OII:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 4)]),
                (TI_INST_RAW_I, [args[1]]),#3
                (TI_INST_CHKJEQ_OOI, [args[0], (TI_ARGTYPE_OFFSET, addr + 3), args[2]]),
            ]
        elif inst_type == TI_INST_CHKJG_OOI:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 4)]),
                (TI_INST_RAW_I, [(TI_ARGTYPE_INSTANT, 0)]),
                (TI_INST_MOV_OO, [(TI_ARGTYPE_OFFSET, addr + 3), args[0]]),
                (TI_INST_SUBJG_OOI, [(TI_ARGTYPE_OFFSET, addr + 3), args[1], args[2]]),
            ]
        elif inst_type == TI_INST_CHKJG_OII:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 4)]),
                (TI_INST_RAW_I, [args[1]]),
                (TI_INST_CHKJG_OOI, [args[0], (TI_ARGTYPE_OFFSET, addr + 3), args[2]]),
            ]
        elif inst_type == TI_INST_MOV_OO:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 4)]),
                (TI_INST_RAW_I, [(TI_ARGTYPE_INSTANT, 0)]),
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 3)]),
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), args[1]]),
                (TI_INST_SUB_OO, [args[0], args[0]]),
                (TI_INST_SUB_OO, [args[0], (TI_ARGTYPE_OFFSET, addr + 3)]),
            ]
        elif inst_type == TI_INST_MOV_OI:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 4)]),
                (TI_INST_RAW_I, [args[1]]),
                (TI_INST_MOV_OO, [args[0], (TI_ARGTYPE_OFFSET, addr + 3)]),
            ]
        elif inst_type == TI_INST_LOD_OO:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 4)]),#0
                (TI_INST_RAW_I, [(TI_ARGTYPE_INSTANT, 0)]),#3
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 3)]),#4
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), args[1]]),#7
                (TI_INST_SUB_OO, [args[0], args[0]]),#10
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 22), (TI_ARGTYPE_OFFSET, addr + 22)]),#13
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 22), (TI_ARGTYPE_OFFSET, addr + 3)]),#16
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 3)]),#19
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), args[0]]),#22, dynamic
                (TI_INST_SUB_OO, [args[0], (TI_ARGTYPE_OFFSET, addr + 3)]),
            ]
        elif inst_type == TI_INST_LOD_OOI:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 5)]),#0
                (TI_INST_RAW_I, [(TI_ARGTYPE_INSTANT, 0)]),#3
                (TI_INST_RAW_I, [args[2]]),#4
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 3)]),#5
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 4)]),#8
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), args[1]]),#11
                (TI_INST_SUB_OO, [args[0], args[0]]),#14
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 26), (TI_ARGTYPE_OFFSET, addr + 26)]),#17
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 26), (TI_ARGTYPE_OFFSET, addr + 3)]),#20
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 3)]),#23
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), args[0]]),#26, dynamic
                (TI_INST_SUB_OO, [args[0], (TI_ARGTYPE_OFFSET, addr + 3)]),
            ]
        elif inst_type == TI_INST_SAV_OO:   # 真的需要这么长吗
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 4)]),#0
                (TI_INST_RAW_I, [(TI_ARGTYPE_INSTANT, 0)]),#3
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 3)]),#4
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), args[0]]),#7

                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 34), (TI_ARGTYPE_OFFSET, addr + 34)]),#10
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 34), (TI_ARGTYPE_OFFSET, addr + 3)]),#13
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 35), (TI_ARGTYPE_OFFSET, addr + 35)]),#16
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 35), (TI_ARGTYPE_OFFSET, addr + 3)]),#19
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 38), (TI_ARGTYPE_OFFSET, addr + 38)]),#22
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 38), (TI_ARGTYPE_OFFSET, addr + 3)]),#25

                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 3)]),#28
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), args[1]]),#31
                (TI_INST_SUB_OO, [args[0], args[0]]),#34, dynamic [[a0]] <- 0
                (TI_INST_SUB_OO, [args[0], (TI_ARGTYPE_OFFSET, addr + 3)]),#37, dynamic [[a0]] <- [a1]
            ]
        elif inst_type == TI_INST_SAV_OOI:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 5)]),#0
                (TI_INST_RAW_I, [(TI_ARGTYPE_INSTANT, 0)]),#3
                (TI_INST_RAW_I, [args[2]]),#4
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 3)]),#5
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), args[0]]),#8
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 4)]),#11

                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 38), (TI_ARGTYPE_OFFSET, addr + 38)]),#14
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 38), (TI_ARGTYPE_OFFSET, addr + 3)]),#17
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 39), (TI_ARGTYPE_OFFSET, addr + 39)]),#20
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 39), (TI_ARGTYPE_OFFSET, addr + 3)]),#23
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 42), (TI_ARGTYPE_OFFSET, addr + 42)]),#26
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 42), (TI_ARGTYPE_OFFSET, addr + 3)]),#29

                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 3)]),#32
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), args[1]]),#35
                (TI_INST_SUB_OO, [args[0], args[0]]),#38, dynamic [[a0] + a2] <- 0
                (TI_INST_SUB_OO, [args[0], (TI_ARGTYPE_OFFSET, addr + 3)]),#41, dynamic [[a0] + a2] <- [a1]
            ]
        elif inst_type == TI_INST_CHKJLE_OOI:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 5)]),#0
                (TI_INST_RAW_I, [(TI_ARGTYPE_INSTANT, 0)]),#3
                (TI_INST_RAW_I, [(TI_ARGTYPE_INSTANT, 0)]),#4
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 4), (TI_ARGTYPE_OFFSET, addr + 4)]),#5
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 4), args[0]]),#8
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 3)]),#11
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 4)]),#13
                (TI_INST_SUBJLE_OOI, [(TI_ARGTYPE_OFFSET, addr + 3), args[1], args[2]]),
            ]
        elif inst_type == TI_INST_CHKJLE_OII:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 4)]),#0
                (TI_INST_RAW_I, [args[1]]),#3
                (TI_INST_CHKJLE_OOI, [args[0], (TI_ARGTYPE_OFFSET, addr + 3), args[2]]),
            ]
        elif inst_type == TI_INST_SUBJGE_OOI:
            return [
                (TI_INST_SUBJLE_OOI, [args[1], args[0], args[2]]),
            ]
        elif inst_type == TI_INST_SUBJGE_OII:
            return [
                (TI_INST_SUBJLE_OII, [args[1], args[0], args[2]]),
            ]
        elif inst_type == TI_INST_CHKJGE_OOI:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 5)]),#0
                (TI_INST_RAW_I, [(TI_ARGTYPE_INSTANT, 0)]),#3
                (TI_INST_RAW_I, [(TI_ARGTYPE_INSTANT, 0)]),#4
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 4), (TI_ARGTYPE_OFFSET, addr + 4)]),#5
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 4), args[1]]),#8
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 3)]),#11
                (TI_INST_SUB_OO, [(TI_ARGTYPE_OFFSET, addr + 3), (TI_ARGTYPE_OFFSET, addr + 4)]),#13
                (TI_INST_SUBJGE_OOI, [args[0], (TI_ARGTYPE_OFFSET, addr + 3), args[2]]),
            ]
        elif inst_type == TI_INST_CHKJGE_OII:
            return [
                (TI_INST_JMP_I, [(TI_ARGTYPE_INSTANT, addr + 4)]),#0
                (TI_INST_RAW_I, [args[1]]),#3
                (TI_INST_CHKJGE_OOI, [args[0], (TI_ARGTYPE_OFFSET, addr + 3), args[2]]),
            ]
        else:
            raise InstNotDefinedError('not implement: %s' % str(inst_type))

    def _ti_compile_expand_complex_recursive(self, inst_and_args : tuple, addr : int) -> list[tuple]:
        result = [inst_and_args]
        i = 0
        addr_offset = 0
        while i < len(result):
            inst_type, args = result[i]
            if self._is_simple_inst(inst_type):
                addr_offset += self._get_length_of_inst(inst_type)
                i += 1
                continue

            t_res = self._ti_compile_expand_complex_inst(result[i], addr + addr_offset)
            result.pop(i)
            for j in range(len(t_res)):
                result.insert(i + j, t_res[j])
        return result

    # not used
    def _evaluate_length_of_inst(self, inst_type : int) -> int:
        result = 0
        for t_type, _ in self._ti_compile_expand_complex_inst((inst_type, [(0, 0)] * 4)):
            result += self._get_length_of_inst(t_type)
        return result

    def _get_length_of_inst(self, inst_type : int) -> int:
        if not self.inst_type2length.__contains__(inst_type):
            self.inst_type2length[inst_type] = self._evaluate_length_of_inst(inst_type)

        return self.inst_type2length[inst_type]
        
    def _add_label(self, label : str, addr : int):
        if self.label2addr.__contains__(label):
            raise ValueError('duplicated label: %s' % label)
        self.label2addr[label] = addr

    def _get_label(self, label : str) -> int:
        if not self.label2addr.__contains__(label):
            raise ValueError('no label named: %s' % label)
        return self.label2addr[label]

    # 预编译，处理label以及复杂指令
    def ti_precompile(self, asm : str) -> list[tuple]:
        # result = []
        ip = 0

        parsed_asm = [] # [(inst_type, [[arg_type, value], ...]), ...]

        for line in asm.split('\n'):
            line = line.lstrip().rstrip()
            if len(line) == 0:
                continue

            if line.startswith('//'):
                continue

            if line.endswith(':'):  #label
                self._add_label(line[:-1], ip)
                continue

            pos_inst_end = line.find(' ')
            inst = line[:pos_inst_end]
            args = line[pos_inst_end+1:].split(', ') if pos_inst_end + 1 < len(line) else []

            parsed_args = [self._ti_compile_parse_arg_32(x, ip) for x in args]
            # 解析指令类型
            inst_type = self._ti_compile_get_inst_type(inst, parsed_args)

            if self._is_simple_inst(inst_type):
                t = (inst_type, parsed_args)
                parsed_asm.append(t)
                ip += self._get_length_of_inst(inst_type)
            else:
                t_res = self._ti_compile_expand_complex_recursive((inst_type, parsed_args), ip)
                parsed_asm.extend(t_res)
                ip += sum([self._get_length_of_inst(x[0]) for x in t_res])


            # res = self._ti_compile_inst_32(inst_type, parsed_args, ip)
            # result.extend(res)
            # ip += len(res)
        return parsed_asm

    def get_bytecode(self, pre_compiled : list[tuple]) -> str:
        labels = []
        for key in self.label2addr.keys():
            labels.append((self.label2addr[key], key))
        labels.sort()
        label_index = 0

        def process_arg(arg):
            result = '<invalid>'
            fm = '%s'
            if arg[0] & TI_ARGTYPE_OFFSET:
                fm = '[%s]'
            if arg[0] & TI_ARGTYPE_LABEL:
                if arg[2] == 0:
                    result = '%' + arg[1]
                elif arg[2] > 0:
                    result = '%%%s+%x' % (arg[1], arg[2])
                else:
                    result = '%%%s%x' % (arg[1], arg[2])
            else:
                result = '#%x' % arg[1]

            return fm % result

        result = []
        ip = 0
        for inst_type, args in pre_compiled:
            head = '0x%04x ' % ip
            while label_index < len(labels) and labels[label_index][0] <= ip:
                result.append('    ' + labels[label_index][1] + ('(0x%x):' % labels[label_index][0]))
                label_index += 1
            s = '<invalid>'
            if   inst_type == TI_INST_SUB_OO:
                s = 'sub %s, %s' % (process_arg(args[0]), process_arg(args[1]))
            elif inst_type == TI_INST_JMP_I:
                s = 'jmp %s' % process_arg(args[0])
            elif inst_type == TI_INST_PUT_O:
                s = 'put %s' % process_arg(args[0])
            elif inst_type == TI_INST_GET_O:
                s = 'get %s' % process_arg(args[0])
            elif inst_type == TI_INST_RAW_I:
                s = 'raw %s' % process_arg(args[0])
                ip -= 2
            elif inst_type == TI_INST_SUBJLE_OOI:
                s = 'sub-jle %s, %s, %s' % (process_arg(args[0]), process_arg(args[1]), process_arg(args[2]))
            ip += 3
            result.append(head + s)
        return '\n'.join(result)

    def ti_compile(self, pre_compiled : list[tuple]) -> list[int]:
        result = []
        ip = 0
        for inst_type, args in pre_compiled:
            res = self._ti_compile_inst_32(inst_type, args, ip)
            result.extend(res)
            ip += len(res)
        return result


if __name__ == '__main__':
    asm = open('dynacode.txt', 'r').read()

    tic = TriInstCompiler()
    pre_compiled = tic.ti_precompile(asm)
    print(pre_compiled)

    bytecode = tic.get_bytecode(pre_compiled)

    fp = open('helloworld.tribc', 'w')
    fp.write(bytecode)
    fp.close()

    code = tic.ti_compile(pre_compiled)

    fp = open('helloworld.tricode', 'w')
    fp.write(str(code))
    fp.close()