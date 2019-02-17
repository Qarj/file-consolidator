# file-consolidator 0.2.0

Consolidate files from sub folders of `--path` directly to `--path`

Files moved will be given a numeric prefix according to their source folder
to preserve sort order.

## Usage

Trial mode:
```
fcon --path test/three_files --trial
```

Move the files:
```
fcon --path test/three_files
```

Careful !!! This has the potential to mess up your file system very quickly and drastically!

## Run the unit tests

```
test_fcon
```

