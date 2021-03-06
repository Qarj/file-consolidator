# file-consolidator 0.2.1

Consolidate files from sub folders of `--path` directly to `--path`

Files moved will be given a numeric prefix according to their source folder
to preserve sort order.

## Usage

Trial mode:

```
fcon.py --path test/three_files --trial
```

Move the files:

```
fcon.py --path test/three_files
```

Careful !!! This has the potential to mess up your file system very quickly and drastically!

Version

```
fcon.py --version
```

Verbose output

```
fcon.py --verbose
```

Delayed output - show STDOUT at end rather than immediate

```
fcon.py --delayed
```

## Debian / Ubuntu installation

Clone project

```
mkdir ~/git
cd ~/git
git clone https://github.com/Qarj/file-consolidator
```

Copy to path and activate

```
cd file-consolidator
sudo cp fcon.py /usr/local/bin
sudo chmod +x /usr/local/bin/fcon.py
fcon.py --version
```

## Run the unit tests

```
chmod +x test_fcon.py
./test_fcon.py
```
