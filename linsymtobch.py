#!/usr/bin/env python3

# # https://github.com/therealdreg/bochs_linux_kernel_debugging
# -
# MIT LICENSE Copyright <2020>
# David Reguera Garcia aka Dreg
# Dreg@fr33project.org - http://www.fr33project.org/ - https://github.com/therealdreg
# twitter: @therealdreg
# -
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# -
# WARNING!! bullshit code

import sys

print(''''

https://github.com/therealdreg/bochs_linux_kernel_debugging
-
MIT LICENSE Copyright <2020>
David Reguera Garcia aka Dreg - Dreg@fr33project.org
http://www.fr33project.org/ - https://github.com/therealdreg

usage: python linsymbtobch.py symbol_file.txt output_bochs_syms.txt [letter 1] [letter 2] [letter 3] .... [--verbose] 

where letters can be empty for all symbols or a combination:

If lowercase, the symbol is local; if uppercase, the symbol is global (external).
------------------------------------
"A" The symbol's value is absolute, and will not be changed by further linking.

"B" "b" The symbol is in the uninitialized data section (known as BSS ).

"C" The symbol is common. Common symbols are uninitialized data. When linking, multiple common symbols may appear with the same name. If the symbol is defined anywhere, the common symbols are treated as undefined references.

"D" "d" The symbol is in the initialized data section.

"G" "g" The symbol is in an initialized data section for small objects. Some object file formats permit more efficient access to small data objects, such as a global int variable as opposed to a large global array.

"i" For PE format files this indicates that the symbol is in a section specific to the implementation of DLLs. For ELF format files this indicates that the symbol is an indirect function. This is a GNU extension to the standard set of ELF symbol types. It indicates a symbol which if referenced by a relocation does not evaluate to its address, but instead must be invoked at runtime. The runtime execution will then return the value to be used in the relocation.

"N" The symbol is a debugging symbol.

"p" The symbols is in a stack unwind section.

"R" "r" The symbol is in a read only data section.

"S" "s" The symbol is in an uninitialized data section for small objects.

"T" "t" The symbol is in the text (code) section.

"U" The symbol is undefined.

"u" The symbol is a unique global symbol. This is a GNU extension to the standard set of ELF symbol bindings. For such a symbol the dynamic linker will make sure that in the entire process there is just one symbol with this name and type in use.

"V" "v" The symbol is a weak object. When a weak defined symbol is linked with a normal defined symbol, the normal defined symbol is used with no error. When a weak undefined symbol is linked and the symbol is not defined, the value of the weak symbol becomes zero with no error. On some systems, uppercase indicates that a default value has been specified.

"W" "w" The symbol is a weak symbol that has not been specifically tagged as a weak object symbol. When a weak defined symbol is linked with a normal defined symbol, the normal defined symbol is used with no error. When a weak undefined symbol is linked and the symbol is not defined, the value of the symbol is determined in a system-specific manner without error. On some systems, uppercase indicates that a default value has been specified.

"-" The symbol is a stabs symbol in an a.out object file. In this case, the next values printed are the stabs other field, the stabs desc field, and the stab type. Stabs symbols are used to hold debugging information.

"?" The symbol type is unknown, or object file format specific.
------------------------------------

Example of use:

python linsymbtobch.py symbol_file.txt output_bochs_syms.txt A a b C --verbose

'''
)

if len(sys.argv) > 2:
    flt = None
    verbose = False
    flt = None
    if len(sys.argv) > 3:
        if "--verbose" in " ".join(sys.argv[3::]).lower():
            print("verbose")
            verbose = True
            sys.argv[3::] = [x for x in sys.argv[3::] if not "--verbose" in x.lower()]
            print(sys.argv, "\n")
        if len(sys.argv[3::]):
            flt = sys.argv[3::]
    else:
        print("writting all symbols")

    with open(sys.argv[2], 'w+') as outf:
        with open(sys.argv[1], 'r', errors='ignore') as inf:
            symbols_written = 0
            letters_written = set()
            letters_found = set()
            for line in inf.readlines():
                line = " ".join(line.split())
                addr, ltr, *name = line.split()
                if not addr.lower().startswith("0x"):
                    addr = "0x" + addr
                name = ltr + "_" + " ".join(name)
                name = name.replace(" ", "_")
                letters_found.add(ltr)
                if flt is None or ltr in flt:
                    letters_written.add(ltr)
                    line_w = addr + " " + name
                    outf.write(line_w + "\n")
                    if verbose:
                        print(line_w)
                    symbols_written += 1

            if len(letters_written) == 0:
                letters_written = "<nothing>"
            else:
                letters_written = " ".join(sorted(letters_written))

            if len(letters_found) == 0:
                letters_found = "<nothing>"
            else:
                letters_found = " ".join(sorted(letters_found))

            print("\ndone!\n")
            print(F"        total symbols written: {symbols_written}")
            print(F"        total letters written: {letters_written}")
            print(F"          total letters found: {letters_found}")