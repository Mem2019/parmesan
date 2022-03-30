# Extract AFLGO Targets using ParmeSan

Firstly we need to get a `LLVMgold.so` by compiling `llvm-project` at `release/7.x` branch.

```bash
mkdir buildv7 && cd buildv7
cmake -DLLVM_BINUTILS_INCDIR=/path/to/binutils/include -DCMAKE_BUILD_TYPE=Release -DLLVM_TARGETS_TO_BUILD=host -DLLVM_ENABLE_PROJECTS="clang;compiler-rt" /path/to/llvm-project/llvm/
cmake --build . -- -j 16
```

The `LLVMgold.so` can be found at `buildv7/lib/LLVMgold.so`, and we copy it to `/path/to/parmesan/llvm/clang+llvm/lib/LLVMgold.so`. We need this to generate `.bc` file for fuzzed target.

Then we can compile the target with `clang/clang++` provided by `ParmeSan` and flags `-g -flto -fuse-ld=gold -Wl,-plugin-opt=save-temps`. We want the file `xxx.0.0.preopt.bc`.

Then get the targets as ParmeSan suggests:

```bash
cd parmesan

rm -f targets.json mapping.txt *.bc
cp /path/to/xxx.0.0.preopt.bc test.bc

USE_FAST=1 bin/angora-clang -emit-llvm -o test.fast.bc -c test.bc
USE_FAST=1 bin/angora-clang -fsanitize=address -emit-llvm -o test.fast.asan.bc -c test.bc
bin/llvm-diff-parmesan -json test.fast.bc test.fast.asan.bc 2>&1 | grep "Diff BB IDs: " > ids.txt
```

Finally, we get the targets for AFLGO:

```bash
python3 tools/llvm-diff-parmesan/id-to-name.py ids.txt mapping.txt BBtargets.asan.txt
```