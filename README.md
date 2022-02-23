# file-consolidator 0.2.1

[![GitHub Super-Linter](https://github.com/Qarj/file-consolidator/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)
![Tests](https://github.com/Qarj/file-consolidator/workflows/Tests/badge.svg)

Consolidate files from sub folders of `--path` directly to `--path`

Files moved will be given a numeric prefix according to their source folder
to preserve sort order.

## Usage

Trial mode:

```sh
fcon.py --path test/three_files --trial
```

Move the files:

```sh
fcon.py --path test/three_files
```

Careful !!! This has the potential to mess up your file system very quickly and drastically!

Version

```sh
fcon.py --version
```

Verbose output

```sh
fcon.py --verbose
```

Delayed output - show STDOUT at end rather than immediate

```sh
fcon.py --delayed
```

## Debian / Ubuntu installation

Clone project

```sh
mkdir ~/git
cd ~/git
git clone https://github.com/Qarj/file-consolidator
```

Copy to path and activate

```sh
cd file-consolidator
sudo cp fcon.py /usr/local/bin
sudo chmod +x /usr/local/bin/fcon.py
fcon.py --version
```

## Run the unit tests

```sh
chmod +x test_fcon.py
./test_fcon.py
```
