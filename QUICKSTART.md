# Quick Start Guide

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install the kernel package:
```bash
pip install -e .
```

3. Install the kernel spec:
```bash
python install_kernel.py --user
```

4. Verify installation:
```bash
jupyter kernelspec list
```

## Running the Test Notebook

```bash
jupyter notebook test_java.ipynb
```

Or with JupyterLab:
```bash
jupyter lab test_java.ipynb
```

## Uninstalling

To remove the kernel:
```bash
jupyter kernelspec uninstall java
pip uninstall java_kernel
```

## Requirements

- Python 3.7+
- Java JDK (with javac and java in PATH)
- Jupyter Notebook or JupyterLab
