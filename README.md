# TechFun's Uploader

A simple Python CLI tool for uploading large files to the free to use TechFun's file hosting service, with progress bar support and automatic chunked uploads.

## Features

- Upload files up to 50 GB in size
- Automatic server-side encryption with AES-256
- Chunked uploading for reliability
- Progress bar with `tqdm`
- Retry logic for failed uploads
- Option to use alternate (dark mode) URL

## Installation

First, clone or download this repository. Then install the tool using pip:

```bash
pip install .
```

This will install the CLI tool as `upload`.

## Usage

```bash
upload [OPTIONS] FILE
```

### Options

- `-n`, `--nigga`  
  Use the alternate (dark mode) URL for file access.

### Arguments

- `FILE`  
  Path to the file you want to upload.

### Example

```bash
upload myvideo.mp4
```

or using the alternate URL:

```bash
upload -n myvideo.mp4
```

## Requirements

- Python 3.6+
- [requests](https://pypi.org/project/requests/)
- [tqdm](https://pypi.org/project/tqdm/)
- [requests-toolbelt](https://pypi.org/project/requests-toolbelt/)

All dependencies are installed automatically during setup.

## License

MIT License

---

*Created by TechFun, 2025*
