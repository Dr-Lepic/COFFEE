# COFFEE - Java Kernel User Guide

**What you'll build**: A solid understanding of how to write, execute, and debug Java code within interactive Jupyter Notebooks.

**What you'll learn**:
- Using snippets vs. full classes
- Understanding compilation behaviors and scope across cells
- Troubleshooting common execution errors

**Prerequisites**:
- [x] Java JDK 8+ installed on your machine
- [x] Python 3.7+ and Jupyter installed
- [x] The `java_kernel` installed (reference the [README](README.md) if you haven't set this up)

---

## Step 1: Your First Interactive Snippet

Traditionally, Java requires a structured `class` and a `public static void main` method just to print a single line of text. This kernel removes that friction so you can focus on the logic.

Start and open a new Jupyter Notebook, select the **Java** kernel from the top-right dropdown, and enter:

```java
System.out.println("Welcome to interactive Java!");
```

Execute the cell (by pressing `Shift + Enter`).

**What happens behind the scenes?**
The kernel analyzes your snippet and detects it isn't wrapped in a defined class. It automatically creates an anonymous class (e.g., `JupyterJava1`), adds a `main` method, inserts your code, and compiles it with `javac`. The execution stdout is then streamed back to your notebook I/O panel.

## Step 2: Working with Full Classes

As your code grows more advanced, you may want to structure it using standard Object-Oriented patterns and custom methods. You can write complete Java classes exactly as you would in an IDE or a `.java` file.

```java
import java.util.HashMap;
import java.util.Map;

public class ScoreTracker {
    public static void main(String[] args) {
        Map<String, Integer> scores = new HashMap<>();
        scores.put("Alice", 95);
        scores.put("Bob", 87);
        
        scores.forEach((name, score) -> {
            System.out.println(name + " scored " + score);
        });
    }
}
```

The kernel uses Regex to parse your code, detects the class name `public class ScoreTracker`, saves the file accordingly as `ScoreTracker.java`, compiles it, and executes it.

## Step 3: Understanding Scope and Limitations

Unlike dynamic environments like Python in Jupyter, Java is statically typed and strictly compiled. This introduces several constraints you need to be aware of:

1. **Independent Cell Executions**: Each cell executes as its own distinct Java process. Local variables declared in Cell 1 (e.g., `int x = 5;`) are **not** directly injected into the just-in-time scope of Cell 2 since they lived in the previous cell's generated `main` method scope.
2. **Import Statements**: If you use `java.util.List` in a cell, you must include `import java.util.List;` at the top of *that specific cell*.
3. **Execution Timeouts**: Infinite loops are dangerous. The kernel actively enforces a **30-second timeout** on execution. If your code exceeds this (excluding compilation time), the kernel kills the JVM process and throws a `TimeoutError`.

## Step 4: Troubleshooting

### "Java compilation failed"
You'll see this if you miss a semicolon, forget an import, or mismatch braces. The kernel streams `javac` errors directly to the cell enabling rapid fixes.

**Fix**: Read the compilation traceback provided in the red error output, identify the line referenced, and correct the syntax.

### "Java not found"
The kernel relies on the `java` and `javac` binaries existing in your system environment.

**Fix**: Ensure the Java Development Kit (JDK) specifically - not just the runtime (JRE) - is installed. Add the JDK's `bin` folder to your system `PATH`. Restart your terminal or notebook server so it reloads the `PATH`.

### Stripped Package Declarations
If you include a declaration like `package com.mycompany;` in your cell, the kernel silently strips it out before compilation.

**Why**: The kernel compiles everything at the root level inside a shared temporary directory across the Jupyter session. Standard nested package directory structures (e.g. `tmpdir/com/mycompany`) aren't supported yet; stripping it ensures your code still executes splendidly rather than crashing on missing path routes point-of-execution directories.

## Next Steps

- Explore the architecture behind the kernel in **[ARCHITECTURE.md](ARCHITECTURE.md)**.
