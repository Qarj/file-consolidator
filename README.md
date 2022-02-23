# file-consolidator 0.2.1

[![GitHub Super-Linter](https://github.com/Qarj/file-consolidator/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)
![Tests](https://github.com/Qarj/file-consolidator/workflows/Tests/badge.svg)

Consolidate files from sub folders of `--path` directly to `--path`

Files moved will be given a numeric prefix according to their source folder
to preserve sort order.

## Usage

Trial mode:

```sh
fcon --path test/three_files --trial
```

Move the files:

```sh
fcon --path test/three_files
```

Careful !!! This has the potential to mess up your file system very quickly and drastically!

Version

```sh
fcon --version
```

Verbose output

```sh
fcon --verbose
```

Delayed output - show STDOUT at end rather than immediate

```sh
fcon --delayed
```

## Debian / Ubuntu installation

Clone project

```sh
mkdir $HOME/git
cd $HOME/git
git clone https://github.com/Qarj/file-consolidator
```

Create symbolic link and activate

```sh
cd $HOME/git/file-consolidator
chmod +x fcon.py
sudo ln -sf $HOME/git/file-consolidator/fcon.py /usr/local/bin/fcon
fcon --version
```

## Run the unit tests

```sh
chmod +x test_fcon.py
python3 test_fcon.py
```
