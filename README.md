# Python Hash Cracker

A high-performance, multi-process hash cracker written in Python. This tool is designed for educational purposes to demonstrate dictionary attack techniques on various hash algorithms.

## Features

-   **Multi-Process Performance:** Utilizes multiple CPU cores to significantly speed up the cracking process.
-   **Auto-Detect Hash Type:** Automatically identifies common hash types (MD5, SHA1, SHA256, etc.) based on their length.
-   **Salt Support:** Capable of cracking hashes that use a salt (prefix or suffix).
-   **User-Friendly CLI:** Clear and colorful command-line interface with a progress bar and performance stats.
-   **File Output:** Saves successfully found credentials to an output file.

## Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/AhmetGultekin0/python-hash-cracker.git](https://github.com/AhmetGultekin0/python-hash-cracker.git)
    cd python-hash-cracker
    ```

2.  Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The basic command structure is as follows:

```bash
python hash_cracker.py <TARGET_HASH> <WORDLIST_FILE> [OPTIONS]
```

### Examples

**1. Auto-Detect and Crack an MD5 Hash:**
```bash
python hash_cracker.py 098f6bcd4621d373cade4e832627b4f6 wordlist.txt
```

**2. Crack a Salted SHA256 Hash and Save the Result:**
```bash
python hash_cracker.py <YOUR_SALTED_SHA256_HASH> wordlist.txt --salt "mysecret" --salt-position prefix -o found.txt
```

**3. Specify 4 CPU Cores for the Task:**
```bash
python hash_cracker.py <HASH> wordlist.txt -p 4
```

---

### **Ethical Disclaimer**

This tool is intended for educational and ethical testing purposes only. Do not use it for any illegal or malicious activities. The author is not responsible for any misuse of this software.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
