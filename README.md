# codeforces-tools

## codeforces-tagstat example
* Install https://www.bazel.io (just `brew install bazel` on osx)
* bazel build //tools/tagstat:codeforces-tagstat
* python3 ./bazel-bin/tools/tagstat/codeforces-tagstat --handler elshiko
