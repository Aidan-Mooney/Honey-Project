# Honey Project

A Python library to extract data from the Zettle API for an local artisan bee products company.

---

## Features

- Extracting data from the Zettle API
- Some Analysis for comparing two flavours of lipbalms

## Dependencies

- Python 3.8+
- make (required for running Makefile commands)
- requests
- python-dotenv
- pandas
- scipy

## Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd <repo-directory>
```

2. Create a virtual environment and install all dependencies:

```bash
make install-requirements
```

3. Test the module is working correctly:

```bash
make run-checks
```

## Set Up

1. Rename .env.example to .env.

2. Replace the 'change me' with the client ID and the client secret.

## Usage

### In Python:

```bash
python3 analysis/lipbalm.py
```
This will extract the data from the Zettle API and then perform a t test on the data for lemon and peppermint lib balms.

## File Structure

```
Honey-Project/
├── data/
|
├── src/
│   └── extract/
|       └── [multiple extract files]
├── test/
│   └── [test-extract]
|       └── [multiple test files]
├── test-data/
|
├── .env.example
├── LICENSE
├── Makefile
├── README.md
└── requirements.txt
```

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.