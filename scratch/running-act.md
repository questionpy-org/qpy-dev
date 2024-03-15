Filters out most of the useless debug noise:

```sh
$ act --quiet | grep -vE '::(debug|add-path|set-output|set-env|group|end-group)::' | grep -v '  docker '
```
