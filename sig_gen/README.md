# ARC Test Suite Signature Generators

There are a collection of scripts in this directory which are usefully for generating the output signatures in the test suite files.  They use some of the raw cryptograhic code from dkimpy, so there is a bit of circularity here, but that code has proven to be accurate accorss several implementations.


## Files
These are the scripts in quesion:

### Validation

These scripts generate i=1 seals.
```
base1.py - standard script for generating AS & AMS from the first prototype message
base2.py - standard script for generating AS & AMS from the second prototype message
base1-multi.py -script for generationg AS & AMS from the first prototype message, where the AS & AMS are signed with different keys
```

This scrips behave as above, except for i>1 seals.
```
level1-1.py
level1-2.py
level2-1.py
level3-1.py
level4-1.py
```

### Sigining

Similar to the above, but for generating arc sets for the validation suite.  The only major difference is the folding option.

```
base_sig.py
level1-1_sig.py
level2-1_sig.py
```

### Actual back end work

```
sig_gen.py
```

Does the actual Arc Set generation, based on parameteres from the previous scripts.


## How these work.

Basically these scripts are functions for generating cryptographic signatures.  In particular the b=, bh= in AMS's, and the b= in the AS.  The scripts provide various keys, the relevant headers to sign, previous arc sets, and the miscelaneous other variables that go in to computing these signatures.  All of this data is organized in the various scripts, and then passes this info to the sig_gen function found in the relevant file.

sig_gen/base1.py, which generates the signatures for the cv_pass_i1_1 validation test is fairly well commented
