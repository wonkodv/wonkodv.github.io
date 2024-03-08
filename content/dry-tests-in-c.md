+++
title               = "Don't Repeat Yourself While Writing Unit Tests in C"
description         = "Use macro magic to avoid having to repeat test names"
date                = 2021-05-30
updated             = 2022-01-04
taxonomies.category = ["Programming"]
taxonomies.tags     = ["c", "unit tests"]
+++

# Don't Repeat Yourself While Writing Unit Tests in C

A File containing unit tests can be as simple as this:

```c
#include <test.h>
#include <sum.h>

TEST_CASE(sum_zero_elements)
{
    uint32_t elements[1] = {1};
    s = sum(elements, 0);
    ASSERT_EQUAL(s, 0);
}
TEST_CASE(sum_one_element)
{
    uint32_t elements[1] = {1};
    s = sum(elements, 1);
    ASSERT_EQUAL(s, 1);
}
TEST_CASE(sum_null)
{
    s = sum(NULL, 1);
    ASSERT_ERROR(ARGUMENT_ERROR);
}
```

There is no reason to write any Test Suite functions or Test Runners.
The macro in cooperation with the linker can do that, with something like:

```c
#define TEST_CASE(tc)
   static void TC_##tc(TEST_RUN* run);
   __attribute__(("section=.test_cases."##tc)) static const TEST_CASE_INFO TCI_##tc = {
    .line=__LINE__,
    .file=__FILE__,
    .name=#tc,
    .function=TC_##tc,
  }
  static void TC_##tc(TEST_RUN* run)
```

This places an info struct in a dedicated section.
The linker will link all those together to produce an array of `TEST_CASE_INFO` which the test runner can simply iterate over:

```c
TEST_CASE_INFO __test_cases_start[];
TEST_CASE_INFO __test_cases_end[];

uint32_t passed, failed;
TEST_CASE_INFO tc;

for (tc=&__test_cases_start[0]; tc<&__test_cases_end[0]; tc=&tc[1]) {
    TEST_RUN run = {
       .failed=false,
       .test_case=tc,
    };
    tc.function(&run);
    if (run.failed) {
        failed += 1;
        /* info already printed by assert */
    } else {
        passed += 1;
        printf("%s:TC_%:%d:PASS\n", tc->file, tc->name, tc->line);
    }
}
printf("\nSUMMARY\n%d Tests Passed %d tests Failed\n", passed, failed);
```

The benefits of this kind of approach:

- You don't repeat yourself.
    The Name of the test case appears exactly once in your project.
    Calling the function from a test suite and the suite from a test runner is just repeating things that you should not have to.
    Every step that has to be done by hand will be forgotten sooner or later.
    Automating solves the problem.
- Lean commits because you only touch one place when adding, deleting or renaming tests.
- You can concentrate on the test, not the surrounding, allowing you to write more tests in less time.
- It is easy to disable all tests you are not currently working on by deleting them. Later, get them from your git to run all tests.
- It is easy to partition tests into chunks if you want to run tests on an embedded device with limited memory, by simply compiling a couple of files at a time.
-   `ctags` can know where `TC_sum_zero_elements()` is defined by something like:
    ```txt
    --regex-c=/^ *TEST_CASE\(([a-zA-Z0-9_]*)\)/TC_\1/f/
    ```
    This regex extracts the word inside the parenthesis, prefixes it with `TC_` and adds it as a function tag.

If you get a bad feeling whether all tests ran, you can do the following things (all of which are a good idea anyway):

-   Measure code coverage
-   Have your build tool tool count the number of `TEST_CASE` maybe also the number of `ASSERT` in your tests folder (`grep TEST_CASE -r tests/|wc -l`) 
    and verify that as many tests were executed.
    Before a Release, do the same by hand.
    This is even more important if you are not using linker magic,
    because developers will eventually forget to add their newly written tests to the test suite.
-   Extend the TEST_CASE macro to add, which requirement(s) are covered by a test case and let your requirements,
    print the requirement ids in the testlog for tests that passed and
    configure your requirement tracing tool to track requirements into the test
    log
    ```c
    TEST_CASE(sum_one_element, "UC_sum_1")
    {
        uint32_t elements[1] = {1};
        s = sum(elements, 1);
        ASSERT_EQUAL(s, 1);
    }
    ```
    ```txt
    ts_sum.c:TC_sum_one_element:42:PASS COVERS: UC_sum_1
    ```
-   Use coverage marks in your code
    ```c
    void (uint32_t *elements, count) {
        COVER(UC_sum);
        if (!elements) {
            COVER(UC_sum_nullptr);
            set_error(ARGUMENT_ERROR);
            return;
        }
        ...
    }
    ```
    and define them to print marks when executing code.
    ```c
    #define COVER(m) do{                                             \
        printf("{}:{}:{}:Covers: {}\n",                              \
        current_test_run->tc.file,                                   \
        current_test_run->tc.line,                                   \
        current_test_run->tc.name,                                   \
        #m);
    ```
    The requirements tool can now verify that the unittest hit code that
    implements a requirement by tracing into the log:
    ```
    ts_sum.c:TC_sum_null:42:Covers: UC_sum
    ts_sum.c:TC_sum_null:42:Covers: UC_sum_nullptr
    ts_sum.c:TC_sum_null:42:PASS
    ```
