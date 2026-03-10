This directory contains the local implementation behind `mix multi_column.generate`.

- If you will never run `mix multi_column.generate` again, removing `lib/<app>/multi_column` and `priv/multi_column` is safe for the running site.
- If you want to keep regenerating or editing navigation from the DSL, keep them.
- If you remove `lib/<app>/multi_column`, also remove `lib/mix/tasks/multi_column.generate.ex`, otherwise the Mix task remains but is broken.

The generated site itself lives in the regular app files under `lib/<app>_web/...`, not in this directory.
