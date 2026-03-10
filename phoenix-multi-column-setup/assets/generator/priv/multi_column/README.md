This directory contains templates used by `mix multi_column.generate`.

- If you will never run `mix multi_column.generate` again, removing `priv/multi_column` and `lib/<app>/multi_column` is safe for the running site.
- If you want to keep regenerating or editing navigation from the DSL, keep them.
- If you remove `lib/<app>/multi_column`, also remove `lib/mix/tasks/multi_column.generate.ex`, otherwise the Mix task remains but is broken.

The running site does not render files from this directory directly. They are only used for future generator runs.
