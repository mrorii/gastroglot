#!/usr/bin/env bash

set -e
set -o pipefail

if [[ $# != 3 && $# != 4 ]]; then
  echo >&2 "Usage: $0 en.json ja.json output_dir [seed]"
  echo >&2 "       The `seed` is used for shuffling the files"
  exit 1
fi

en_json=$1
ja_json=$2
output_dir=$3

if [ $# == 4 ]; then
  seed=$4
else
  seed=1
fi

train_percentage=0.8
dev_percentage=0.1
test_percentage=0.1

en_shuffled=$output_dir/en.$RANDOM$RANDOM$RANDOM
ja_shuffled=$output_dir/ja.$RANDOM$RANDOM$RANDOM

cat $en_json | perl -MList::Util=shuffle -e "srand $seed; print shuffle(<STDIN>);" > $en_shuffled
cat $ja_json | perl -MList::Util=shuffle -e "srand $seed; print shuffle(<STDIN>);" > $ja_shuffled

total_length=`wc -l $en_json | sed 's/^ *//g' | cut -f1 -d' '`
train_length=`echo "($total_length * $train_percentage) / 1" | bc`
dev_length=`echo "($total_length * $dev_percentage) / 1" | bc`
test_length=`echo "(($total_length - $train_length) - $dev_length)" | bc`

echo "train: $train_length"
echo "dev: $dev_length"
echo "test: $test_length"

split_data() {
  data=$1
  train_file=$2
  dev_file=$3
  test_file=$4
  
  head -$train_length $data > $train_file
  head -`echo "($train_length + $dev_length)" | bc` $data | tail -$dev_length > $dev_file
  tail -$test_length $data > $test_file
}

en_basename=`basename $en_json`
ja_basename=`basename $ja_json`

split_data $en_shuffled $output_dir/$en_basename.train $output_dir/$en_basename.dev $output_dir/$en_basename.test 
split_data $ja_shuffled $output_dir/$ja_basename.train $output_dir/$ja_basename.dev $output_dir/$ja_basename.test 

rm $en_shuffled
rm $ja_shuffled
