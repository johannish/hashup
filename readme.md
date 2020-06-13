# hashup
Hashdeep Utility Program

## Purpose
Help compare and audit output files from hashdeep. Yes, hashdeep has an audit mode, but it can only compare a working directory against an existing hashdeep output file. I'm insterested in answering questions like, "what files were lost between these two hashdeep runs?" "What duplicate files exist within this single hashdeep output?" "What are the differences between these two directory structures?"

## developing
### running unit tests
```
python -m unittest discover
```
or
```
python -m unittest test.test_hashdeep_csv
```


## to-do
* prettier output for "only in file 2" mode
* ability to configure ignore patterns
* Use hashdeep header to determine what columns exist in the file
