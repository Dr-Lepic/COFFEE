"""
Simple test script to verify the Java kernel works
"""

import subprocess
import sys
import json
import tempfile
import os

def test_java_available():
    """Test if Java is available"""
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        print("✓ Java is available")
        print(f"  Version: {result.stderr.split('\\n')[0]}")
        return True
    except FileNotFoundError:
        print("✗ Java not found")
        return False

def test_javac_available():
    """Test if Java compiler is available"""
    try:
        result = subprocess.run(['javac', '-version'], capture_output=True, text=True)
        print("✓ Java compiler is available")
        print(f"  Version: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("✗ Java compiler not found")
        return False

def test_kernel_installed():
    """Test if kernel is installed"""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'jupyter', 'kernelspec', 'list'],
            capture_output=True,
            text=True
        )
        if 'java' in result.stdout:
            print("✓ Java kernel is installed")
            return True
        else:
            print("✗ Java kernel not found in kernelspec list")
            return False
    except Exception as e:
        print(f"✗ Error checking kernel: {e}")
        return False

def test_kernel_execution():
    """Test if the kernel can execute Java code"""
    print("\nTesting kernel execution...")
    
    test_code = '''
System.out.println("Hello from Java!");
int sum = 0;
for (int i = 1; i <= 5; i++) {
    sum += i;
}
System.out.println("Sum: " + sum);
'''
    
    try:
        # Import the kernel
        from java_kernel.kernel import JavaKernel
        
        # Create a mock kernel instance
        kernel = JavaKernel()
        
        # Execute the code
        result = kernel.do_execute(test_code, False)
        
        if result['status'] == 'ok':
            print("✓ Kernel execution successful")
            return True
        else:
            print(f"✗ Kernel execution failed: {result}")
            return False
            
    except Exception as e:
        print(f"✗ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("Java Kernel Test Suite")
    print("=" * 50)
    
    tests = [
        ("Java Runtime", test_java_available),
        ("Java Compiler", test_javac_available),
        ("Kernel Installation", test_kernel_installed),
        ("Kernel Execution", test_kernel_execution),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\nTesting {name}...")
        results.append(test_func())
    
    print("\n" + "=" * 50)
    print(f"Tests passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("\n✓ All tests passed! The Java kernel is ready to use.")
        print("\nTo start using it, run:")
        print("  jupyter notebook")
        print("\nThen create a new notebook and select 'Java' as the kernel.")
    else:
        print("\n✗ Some tests failed. Please check the output above.")

if __name__ == '__main__':
    main()
