+++
title               = "Video on Measuring / Increasing Performance of Code"
description         = "Emery Berger talks about performance improvements that work / don't work."
date                = 2021-12-21
taxonomies.category = ["Programming"]
taxonomies.tags     = ["performance", "video", "recommended reading"]
+++

Video on Measuring / Increasing Performance of Code
===================================================

Emery Berger talks about performance improvements that work / don't work.

{{ youtube(id="r-TLSBdHe1A") }}

Key Points
----------

*   When optimizing your code, you can easily get random side effects which impact performance more than the changes.
*   The execution environment (command args, current directory, environment
    variables) can have significant impact on execuiton speed, so they have to
    be factored out when measuring performance.
*   Use [`stabilizer`](https://github.com/plasma-umass/stabilizer) to randomize
    the layout of a linked binary and ignore accidental sideeffects.
*   `-O3` has no statistically significant benefit over `-O2` in `clang` / LLVM.
*   Typical profilers come from the single threaded single core time, and are not well
    suited to profile async or concurrent code.
*   Use [`coz-profiler`](https://github.com/plasma-umass/coz) to find code that
    causes performance problems.
*   Users don't care about the performance they care about responsiveness. This
    may or may not be the same thing.

