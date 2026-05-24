# Java Kernel for Jupyter

A simple wrapper kernel that allows you to execute Java code in Jupyter notebooks. This kernel uses IPython's kernel machinery to compile and run Java code.

## Features

- Execute Java code directly in Jupyter notebooks
- Automatic compilation and execution
- Support for both complete Java classes and code snippets
- Error handling and display of compilation/runtime errors
- Supports Java 8+

## Prerequisites

Before installing the Java kernel, make sure you have:

1. **Python 3.7+** installed
2. **Java JDK** (Java Development Kit) installed and available in your system PATH
   - To verify, run: `java -version` and `javac -version`
3. **Jupyter** installed (`pip install jupyter`)

## Installation

### Step 1: Install the package

```bash
# Install the package in development mode
pip install -e .
```

This will install the required dependencies:
- `ipykernel`
- `jupyter_client`

### Step 2: Install the kernel spec

```bash
# Install for current user
python install_kernel.py --user

# Or install system-wide (may require admin/sudo)
python install_kernel.py
```

### Step 3: Verify installation

```bash
# List installed kernels
jupyter kernelspec list
```

You should see `java` in the list of available kernels.

## Usage

### Starting Jupyter

```bash
# Start Jupyter Notebook
jupyter notebook

# Or start JupyterLab
jupyter lab
```

### Creating a Java notebook

1. Click "New" and select "Java" from the kernel list
2. Start writing Java code!

### Code Examples

#### Example 1: Simple Hello World

```java
System.out.println("Hello from Java in Jupyter!");
```

#### Example 2: Complete Class

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        
        // You can use loops
        for (int i = 0; i < 5; i++) {
            System.out.println("Count: " + i);
        }
    }
}
```

#### Example 3: Code Snippet (auto-wrapped in class)

```java
// This will be automatically wrapped in a class with main method
int sum = 0;
for (int i = 1; i <= 10; i++) {
    sum += i;
}
System.out.println("Sum of 1-10: " + sum);
```

#### Example 4: Using Java features

```java
import java.util.*;

public class DataStructures {
    public static void main(String[] args) {
        List<String> fruits = Arrays.asList("Apple", "Banana", "Cherry");
        
        System.out.println("Fruits:");
        for (String fruit : fruits) {
            System.out.println("- " + fruit);
        }
        
        Map<String, Integer> scores = new HashMap<>();
        scores.put("Alice", 95);
        scores.put("Bob", 87);
        
        System.out.println("\nScores:");
        scores.forEach((name, score) -> 
            System.out.println(name + ": " + score)
        );
    }
}
```

## How it Works

This kernel is a wrapper around the Java compiler and runtime:

1. **Code Reception**: When you execute a cell, the kernel receives your Java code
2. **Code Wrapping**: If your code doesn't contain a class definition, it's automatically wrapped in a class with a `main` method
3. **Compilation**: The code is saved to a temporary `.java` file and compiled using `javac`
4. **Execution**: If compilation succeeds, the compiled class is executed using `java`
5. **Output**: Standard output and errors are sent back to the notebook

## Limitations

- Each cell is compiled and executed independently
- No state is preserved between cells (unlike Python notebooks)
- Maximum execution time is 30 seconds per cell
- Limited to console output (no GUI support)
- Import statements need to be included in each cell that uses them

## Troubleshooting

### "Java not found" error

Make sure Java JDK is installed and in your PATH:

```bash
# Windows (PowerShell)
java -version
javac -version

# If not found, install Java JDK and add to PATH
```

### "Compilation Error"

Check your Java syntax. Common issues:
- Missing semicolons
- Unmatched braces
- Incorrect class/method declarations

### Kernel not appearing in Jupyter

Try reinstalling:

```bash
# Uninstall kernel spec
jupyter kernelspec uninstall java

# Reinstall
python install_kernel.py --user
```

## Uninstallation

```bash
# Remove kernel spec
jupyter kernelspec uninstall java

# Uninstall package
pip uninstall java_kernel
```

## Development

### Project Structure

```
java_kernel/
├── java_kernel/
│   ├── __init__.py      # Package initialization
│   ├── __main__.py      # Entry point
│   ├── kernel.py        # Main kernel implementation
│   └── kernel.json      # Kernel specification
├── setup.py             # Package setup
├── install_kernel.py    # Kernel installation script
└── README.md           # This file
```

### Running in Development Mode

```bash
# Install in editable mode
pip install -e .

# Install kernel spec
python install_kernel.py --user
```

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Future Enhancements

- Support for external libraries (classpath management)
- Better error messages with line numbers
- Support for multi-cell classes
- Variable persistence between cells
- Integration with Maven/Gradle dependencies

## Credits

Built using IPython's kernel machinery and inspired by other Jupyter language kernels.
