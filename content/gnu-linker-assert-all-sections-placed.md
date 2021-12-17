+++
title = "Explicitly Place All Sections When Linking With GNU LD"
description = "Use an assertion to detect sections that are not placed explicitly by a linker script"
date  = 2021-03-12
updated = 2022-01-04
taxonomies.category=["Programming"]
taxonomies.tags=["C", "Embedded"]
+++

Explicitly Place All Sections When Linking With GNU LD
======================================================

## The Problem

If you place your sections manually, you sometimes forget one and the gnu linker places it automatically.
Having data or code linked in the wrong place often works for a while or when
not doing in depth tests, but can cause your system to have very odd behavior
that is hard to pinpoint.
If you are writing a linker script, it is best to place everything explicitly and get notified about every unplaced section.

## The Solution

A way to produce such a warning, is to define a catch all section and using `ASSERT()` to test, that it is empty:

```ld, linenos, hl_lines=28
memories {...}
sections {

    .text : {
        *(.text)
    } > rom
    .data : {
        *(.data)
    } > ram

    .debug_macro   : { *(.debug_macro)   }
    .debug_line    : { *(.debug_line)    }
    .debug_str     : { *(.debug_str)     }
    .debug_frame   : { *(.debug_frame)   }
    .debug_info    : { *(.debug_info)    }
    .debug_abbrev  : { *(.debug_abbrev)  }
    .debug_aranges : { *(.debug_aranges) }
    .debug_ranges  : { *(.debug_ranges)  }
    .debug_loc     : { *(.debug_loc)     }
    .comment       : { *(.comment)       }
    .version_info  : { *(.version_info)  }

    .unplaced : {
        __unplaced_start = . ;
        *(*)
        __unplaced_end = . ;

        ASSERT(__unplaced_start == __unplaced_end, "ASSERT(.unplaced empty) failed");
        /*
        * If the assert failed, check the .unplaced section in map file and
        * manually place anything that was placed there.
        */
    }
}
```

This part of the linker script places `.data` in ram, a bunch of debug stuff at its default location and anything else will end up in `.unplaced` and trigger an error like this:

```
ld: error: ASSERT(.unplaced empty) failed
```

If you look at the map file:

```
.unplaced       memory region -> /DISCARD/
                0x00000000    0x1234
                0x00000000                __unplaced_start = .
 *(*)
 .text.hello_world
                0x00000000        0x32 ./lib/lib.a(test.o)
                0x00000034                __unplaced_end = .
                0x00000000                ASSERT ((__unplaced_start == __unplaced_end), ...)
```

This tells you, that there is a section `.text.hello_world` which the compiler created when compiling `test.o` which is part of `lib/lib.a` and you did not place it explicitly.
The reason is, that we captured `.text` but not `.text.*`. The issue was
introduced when adding `-ffunction-sections` to the compiler options in order to
reduce ROM usage (by also passing `-gc-sections` to the linker). This changes
the section where code is placed, so it ended up in the wrong place.

Depending on your compilers settings, a bunch of different debug sections will have to be added to the script.
I have not found a more compact way which still allows debugging.
Please write to me if you know the way!
