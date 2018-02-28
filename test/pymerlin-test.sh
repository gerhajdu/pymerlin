# !/bin/bash

echo "The output of the test should be:"
echo "35076_1 -0.394 0.035 -0.449 0.037"
echo "35076_2 -0.372 0.034 -0.425 0.036"
echo "35076_3 -0.396 0.038 -0.450 0.040"

echo "The real output is:"
pymerlin test_data
