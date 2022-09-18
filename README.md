# ⚡ _**FastGen**_

Start FastAPI Projects in Lightning Speed

Built With **Typer** To Help With <span style="color:green">**FastAPI**</span>.

## Installation

```console
$ python -m pip install fastgen
```

**Usage**:

```console
$ fastgen [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
- `--help`: Show this message and exit.

**Commands**:

- `info`
- `startproject`

## `fastgen info`

**Usage**:

```console
$ fastgen info [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

## `fastgen startproject`

**Usage**:

```console
$ fastgen startproject [OPTIONS] ⭐ Project Name
```

**Arguments**:

- `⭐ Project Name`: [required]

**Options**:

- `--dir 📁 Directory Path`
- `--package-manager 📦 Package Manager`: [default: pip]
  ( Options are pip , poetry "Comming Soon" )
- `--migrations / --no-migrations`: [default: False]
- `--docker / --no-docker`: [default: False]
- `--testing / --no-testing`: [default: False]
- `--database 📅 Database`: [default: postgresql] ( Options are postgresql,mysql,sqlite )
- `--help`: Show this message and exit.
