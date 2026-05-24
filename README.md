# COFFEE - Java Kernel for Jupyter

> Execute Java code directly in Jupyter Notebooks with automatic compilation and error reporting.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Exists

Jupyter Notebooks are the standard for interactive Python development, but bringing compiled languages like Java into this ecosystem historically requires complex setups, heavyweight JVM integrations, or custom IDEs. This kernel provides a lightweight, pure-Python wrapper around your system's Java Development Kit (JDK). It leverages IPython's proven kernel machinery to compile and execute Java code on the fly — meaning you can start prototyping Java applications, algorithms, and data structures interactively in seconds without bloated editors.

## Quick Start

Get the kernel running locally in less than a minute. 

```bash
# Clone the repository and navigate to it
pip install -e .
python install_kernel.py --user

# Start your notebook
jupyter notebook
```

Next, open Jupyter, click **New > Java**, and paste this into a cell:

```java
System.out.println("Hello from Java in Jupyter!");
```
*Press `Shift + Enter` to run it. You should see your text printed immediately.*

## Installation

**Prerequisites**:
- **Python**: 3.7+
- **Jupyter**: Installed via `pip install jupyter`
- **Java JDK**: Version 8 or newer installed and available in your system `PATH`. Verify this by running `java -version` and `javac -version` in your terminal.

Execute the following commands in your terminal:

```bash
# 1. Install setup requirements
pip install -r requirements.txt

# 2. Install the kernel Python package in development mode
pip install -e .

# 3. Register the kernel spec with Jupyter
python install_kernel.py --user
```

Verify the installation succeeded by listing your kernels:

```bash
jupyter kernelspec list
# You should see 'java' listed alongside python3
```

## Usage

### Basic Snippets

You don't need to write boilerplate `public class Main` wrappers for simple logic. The kernel automatically translates and wraps naked snippets in an executable class holding a `main` method before compilation.

```java
int sum = 0;
for (int i = 1; i <= 10; i++) {
    sum += i;
}
System.out.println("Sum of 1-10: " + sum);
```

### Complete Classes

If you prefer building complete structures, you can define your own complete classes directly in the cell. The kernel parses your code, extracts the public class name, and runs it as an independent application.

```java
import java.util.List;
import java.util.Arrays;

public class DataStructures {
    public static void main(String[] args) {
        List<String> fruits = Arrays.asList("Apple", "Banana", "Cherry");
        fruits.forEach(System.out::println);
    }
}
```

## Documentation

- **[User Guide & Tutorial](USER_GUIDE.md)**: Deep dive into using the kernel, handling errors, and understanding wrapper behavior. Let this be your starting point if you've never used Java in a Notebook before.

## License

MIT © Java Kernel Contributors
