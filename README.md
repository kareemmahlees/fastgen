<p align="center" class="logo">
<img src=".\docs\logo.png" alt="logo" >
</p>

<p align="center" class="name">
FastGen
</p>

<p align="center" class="slogan"> <em>A CLI for your next FastAPI Project</em></p>

<style>
    .slogan{
        margin-top:-9px;
        padding-bottom:15px;
        font-size:15px
    }
    .logo{
        padding-bottom:10px;
        padding-top:25px
    }
    .name{
      font-size:20px;
      font-weight:bold
    }
</style>

---

<!-- # ⚡ _**FastGen**_

Start FastAPI Projects in Lightning Speed

Built With **Typer** To Help With <span style="color:green">**FastAPI**</span>. -->

## 👀 **Take A Look**

this is a glanc of the project structure you will have once you use **FastGen**

![dirs_images](./docs/dir.png)

## **Navigate Quickly**

[installation](#✨-installation)<br>
[commands](#🧭-commands)

- [info](#fastgen-info)
- [new](#fastgen-new)
- [g](#fastgen-g)

## ✨ **Installation**

Using pip :

```console
$ python -m pip install fastgen
```

Using Poetry :

```console
$ poetry add fastgen
```

## 🧭 **Commands**

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
- `new`

## **`fastgen info`**

**Usage**:

```console
$ fastgen info [OPTIONS]
```

**Options**:

- `--help`: Show this message and exit.

## **`fastgen new`**

**Usage**:

```console
$ fastgen new [OPTIONS] ⭐ Project Name
```

**Arguments**:

- `⭐ Project Name`: <span style="color:pink">**required**

**Options**:

- `--dir 📁 Directory Path`
- `--package-manager 📦 Package Manager`: [default: pip]
  ( Options are pip , poetry )
- `--migrations / --no-migrations`: [default: False]
- `--docker / --no-docker`: [default: False]
- `--testing / --no-testing`: [default: False]
- `--database 📅 Database`: [default: postgresql] ( Options are postgresql,mysql,sqlite )
- `--orm ⚙️ ORM`: [default: False]
- `--help`: Show this message and exit.

## **`fastgen g`**

**Usage**:

```console
$ fastgen g [OPTIONS] <component> <component_name>
```

**Available Components**
| Component | In stock |
|--------------|------------|
| router | generates new rotuer at app/api/routers |
| model | generates new sqlmodel or sqlalchemy mode at app/database/models |
| schema | generates new pydantic schema at app/api/schemas

**Options**

- `--model-type` : available only for model components , optional values are ( sqlmodel , sqlalchemy )
- `--path` : specifiy where to create the component **RELATIVE TO THE CURRENT WORKING DIRECOTRY** if not in default path

- **Note** : the naming is preferred to be in lower case so it can be resolved correctly

**Arguments**

```console

```

## 🪲 **Encountered A Problem !**

feel free to open an issue discussing the problem you faced

## 🤝🏻 **Contributing**

please refer to [Contribution Guide](./CONTRIBUTING.md)
