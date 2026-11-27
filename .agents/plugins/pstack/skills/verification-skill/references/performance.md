# Measure a change

Write down what a user waits for. Identify a repeatable workload and a correctness check that proves each run completed the same work. Read the timing code to see where the clock starts and stops. Record the target, revisions, input size, data distribution, filters, build, concurrency and cache state that materially affect the claim.

Capture a baseline. Use a separate instrumented run to locate the cost, such as a query plan for a database bottleneck or a browser trace for a rendering delay. Exercise the same path after the change. Alternate comparable runs to reduce warmup and load bias. Record each duration, errors, and the rows, bytes or other output that confirm the workload completed. Do not turn failed, empty, or cached-away work into a speedup.

Report the sample count, median and spread for both sides with the end-to-end delta. When variation obscures the difference, call the comparison inconclusive. A quick single observation can be labeled as such. Keep the command, inputs and raw measurements available for a rerun.
