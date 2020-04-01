#!/usr/bin/env bash
contract_name="$1"
./vendor/SmartPyBasic/SmartPy.sh test "src/contracts/${contract_name}.py" "src/contracts/compiled/${contract_name}"
echo "========="
cat "src/contracts/compiled/${contract_name}/test.output"
