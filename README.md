# gastroglot

A collection of glue code for the task of translating Japanese recipes into English, using data from the Japanese and English versions of Cookpad ([http://cookpad.com/](http://cookpad.com/) and [https://en.cookpad.com/](https://en.cookpad.com/), respectively).

## Dependencies

* [MeCab](https://code.google.com/p/mecab/)
* [MeCab python binding](http://mecab.googlecode.com/svn/trunk/mecab/doc/bindings.html)
* [cdec](https://github.com/redpony/cdec)
* [hunalign](https://github.com/mrorii/hunalign)

## Prerequisite

You will first need to crawl Cookpad and extract Japanese and English recipes.
Refer to https://github.com/mrorii/cookbot for an example Cookpad crawler.

We assume that the recipes are saved in a file where each line
is a JSON-encoded item representing a single recipe.
An example recipe should look like the following:

```json
{
    "id": 2189047,
    "name": "Julienne burdock beef roll"
    "description": "It is good for bento",
    "ingredients": [
        {
            "name": "Japanese leek",
            "quantity": "About 15 cm of a thick one"
        },
        {
            "name": "Enoki mushrooms",
            "quantity": "As needed"
        }
    ],
    "advice": "Use two meat for one roll if the meat is too thin",
    "history": "To eat many kind of vegetables and burdock, I rolled it in beef."
}
```

## Steps

### Preprocessing

Clone the repo:

```bash
git clone https://github.com/mrorii/gastroglot.git
cd gastroglot
```

From now on, we will refer to `GASTROGLOT` as the path where gastroglot was cloned.

Put the crawled `cookpad.en.json` and `cookpad.ja.json` into the `data` directory.
We first need to find the subset of the Japanese recipes that correspond to the English recipes. During this step, it will print out to standard error recipe IDs found in the English file but not the Japanese file. If there are any recipes that are not found in the Japanese file, be sure to crawl Cookpad again and add them to the file:

```bash
python find_parallel_recipes.py data/cookpad.en.json data/cookpad.ja.json > data/cookpad.ja.p.json
```

Next, we align the Japanese and English recipes by sorting:

```bash
python sort_recipes.py data/cookpad.en.json > data/cookpad.en.sorted.json
python sort_recipes.py data/cookpad.ja.p.json > data/cookpad.ja.sorted.json
```

Split recipes into train, dev, and test:

```bash
mkdir -p data/split
./split_data.sh data/cookpad.en.sorted.json data/cookpad.ja.sorted.json data/split
```

Tokenize (both by sentence and by word) and lower-case all of the text (Note: if you want to detokenize and recase the output from the translation system, use the scripts from [moses](http://www.statmt.org/moses/)):

```bash
for t in train dev test
  do
  python tokenize_all.py data/split/cookpad.en.sorted.json.$t --lang en | perl lowercase.pl > data/split/cookpad.en.$t.tok
  python tokenize_all.py data/split/cookpad.ja.sorted.json.$t --lang ja | perl lowercase.pl > data/split/cookpad.ja.$t.tok
done
```

(Optional) Inspect top N words (for manually generating the en-ja dic for hunalign):

```bash
python inspect_frequent_words.py data/cookpad.ja.json --lang ja --n 1000 > top_words.txt
```

(Optional) Check that ingredients are the same size:

```bash
python check_ingredients_alignment.py data/cookpad.ja.sorted.json data/cookpad.en.sorted.json
```

### Sentence Alignment

Install hunalign:

```bash
git clone https://github.com/mrorii/hunalign.git
cd hunalign/src/hunalign
make
```

From now on, we will refer to HUNALIGN as the path where hunalign was installed.

Generate input for hunalign (i.e. separate text into chunks that hunalign can handle):

```bash
cd $GASTROGLOT
mkdir -p data/hunalign
for t in train dev test
  do
  python generate_hunalign_input.py \
    data/split/cookpad.ja.$t.tok \
    data/split/cookpad.en.$t.tok \
    data/hunalign/cookpad.$t \
    data/hunalign/cookpad.$t.batchfile \
    --b 5000
done
```

Run hunalign in batch mode:

```bash
cd $HUNALIGN
for t in train dev test
  do
  src/hunalign/hunalign $GASTROGLOT/data/en-ja.dic -batch \
                        $GASTROGLOT/data/hunalign/cookpad.$t.batchfile
done
```

Convert the alignment indices into actual text:

```bash
# train
# Assuming that the training file was split into 7 chunks,
for i in {1..7}
  do
  scripts/ladder2text.py ~/dev/gastroglot/data/hunalign/cookpad.train.$i.align \
                         ~/dev/gastroglot/data/hunalign/cookpad.train.$i.ja \
                         ~/dev/gastroglot/data/hunalign/cookpad.train.$i.en \
                         > ~/dev/gastroglot/data/hunalign/cookpad.train.$i.align.txt
done

# dev and test
# Assuming that there's only 1 chunk for dev and test,
for t in dev test
  do
  scripts/ladder2text.py ~/dev/gastroglot/data/hunalign/cookpad.$t.1.align \
                         ~/dev/gastroglot/data/hunalign/cookpad.$t.1.ja \
                         ~/dev/gastroglot/data/hunalign/cookpad.$t.1.en \
                         > ~/dev/gastroglot/data/hunalign/cookpad.$t.align.txt
done
cat data/hunalign/cookpad.train.*.align.txt > data/hunalign/cookpad.train.align.txt
```

Generate cdec input:

```bash
# generate cdec format files (excluding ingredients)
cd $GASTROGLOT
mkdir -p data/cdec

for t in train dev test
  do
  python generate_cdec_input_from_hunalign.py data/hunalign/cookpad.$t.align.txt \
                                              > data/cdec/cookpad.$t.hunalign.ja-en
done

# generate cdec format files (for ingredients)
for t in train dev test
  do
  python generate_cdec_input_from_ingredient.py data/split/cookpad.ja.$t.tok \
                                                data/split/cookpad.en.$t.tok \
                                                > data/cdec/cookpad$t.ingredient.ja-en
done

# concatenate results from both
for t in train dev test
  do
  cat data/cdec/cookpad.$t.hunalign.ja-en data/cdec/cookpad.$t.ingredient.ja-en \
                                          > data/cdec/cookpad.$t.ja-en
done
```

### cdec

The commands below are basically copied from [http://www.cdec-decoder.org/guide/tutorial.html](http://www.cdec-decoder.org/guide/tutorial.html), so refer to that page for details about command-line options.

Install cdec. From now on, we will refer to `CDEC` as the path where cdec was installed.

```bash
export DATA_DIR=$GASTROGLOT/data/cdec
```

Filter training corpus sentence lengths:

```bash
$CDEC/corpus/filter-length.pl -80 $DATA_DIR/cookpad.train.ja-en \
                                  > $DATA_DIR/cookpad.train.filtered.ja-en
```

Run word bidirectional word alignments (Estimated time: ~10 minutes):

```bash
$CDEC/word-aligner/fast_align -i $DATA_DIR/cookpad.train.filtered.ja-en -d -v -o \
                              > $DATA_DIR/cookpad.train.ja-en.fwd_align
$CDEC/word-aligner/fast_align -i $DATA_DIR/cookpad.train.filtered.ja-en -d -v -o -r \
                              > $DATA_DIR/cookpad.train.ja-en.rev_align
```

Symmetrize word alignments (Estimated time: 5 seconds):

```bash
$CDEC/utils/atools -i $DATA_DIR/cookpad.train.ja-en.fwd_align \
                   -j $DATA_DIR/cookpad.train.ja-en.rev_align -c grow-diag-final-and \
                   > $DATA_DIR/training.gdfa
```

Compile the training data (Estimated time: ~1 minute):

```bash
export PYTHONPATH=`echo $CDEC/python/build/lib.*`
python -m cdec.sa.compile -b $DATA_DIR/cookpad.train.filtered.ja-en \
                          -a $DATA_DIR/training.gdfa \
                          -c $DATA_DIR/extract.ini \
                          -o $DATA_DIR/training.sa
```

Extract grammars for the dev and devtest sets (Estimated time: 15 minutes):

```bash
python -m cdec.sa.extract -c $DATA_DIR/extract.ini \
                          -g $DATA_DIR/dev.grammars \
                          -j 2 \
                          -z \
                          < $DATA_DIR/cookpad.dev.ja-en \
                          > $DATA_DIR/cookpad.dev.ja-en.sgm

python -m cdec.sa.extract -c $DATA_DIR/extract.ini \
                          -g $DATA_DIR/test.grammars \
                          -j 2 \
                          -z \
                          < $DATA_DIR/cookpad.test.ja-en \
                          > $DATA_DIR/cookpad.test.ja-en.sgm
```

Build the target language model (Estimated time: 1 minute):

```bash
$CDEC/corpus/cut-corpus.pl 2 $DATA_DIR/cookpad.train.ja-en | \
    $CDEC/klm/lm/builder/builder --order 3 > $DATA_DIR/cpad.lm
```

Compile the target language model:

```bash
$CDEC/klm/lm/build_binary $DATA_DIR/cpad.lm $DATA_DIR/cpad.klm
```

Create a cdec.ini configuration file:

Create a `cdec.ini` file in $CDEC containing the following lines,
making sure to substitute $DATA_DIR with the absolute path:

    formalism=scfg
    add_pass_through_rules=true
    feature_function=WordPenalty
    feature_function=KLanguageModel $DATA_DIR/cpad.klm

Try running the decoder with the command:

```bash
cd $CDEC
$CDEC/decoder/cdec -c cdec.ini
```

Tune the system parameters using development data with MIRA:

```bash
cd $CDEC
mkdir -p $DATA_DIR/mira
python $CDEC/training/mira/mira.py -d $DATA_DIR/cookpad.dev.ja-en.sgm \
                                   -t $DATA_DIR/cookpad.test.ja-en.sgm \
                                   -c cdec.ini \
                                   -j 2 \
                                   --output-dir $DATA_DIR/mira
```
