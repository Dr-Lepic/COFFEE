"""
Java Wrapper Kernel

A simple wrapper kernel that allows executing Java code in Jupyter notebooks.
This kernel compiles and runs Java code using the IPython kernel machinery.
"""

from ipykernel.kernelbase import Kernel
import subprocess
import tempfile
import os
import re
import sys


class JavaKernel(Kernel):
    implementation = 'Java'
    implementation_version = '0.1.0'
    language = 'java'
    language_version = '11'  # Will detect actual version
    language_info = {
        'name': 'java',
        'mimetype': 'text/x-java',
        'file_extension': '.java',
        'codemirror_mode': 'java',
    }
    banner = "Java Wrapper Kernel - Execute Java code in Jupyter"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._check_java_installation()
        self.class_counter = 0
        # Reusing the temp directory avoids creating/destroying directories per cell execution
        # and allows later cells to reference classes compiled in earlier cells
        self.temp_dir = tempfile.TemporaryDirectory()
        
    def do_shutdown(self, restart):
        """Clean up the temporary directory on shutdown"""
        self.temp_dir.cleanup()
        return super().do_shutdown(restart)
        
    def _check_java_installation(self):
        """Check if Java is installed and available"""
        try:
            result = subprocess.run(
                ['java', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            version_output = result.stderr if result.stderr else result.stdout
            
            # Extract version number
            version_match = re.search(r'version "(\d+)', version_output)
            if version_match:
                self.language_version = version_match.group(1)
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log.error("Java not found. Please install Java JDK.")
            
    def _extract_class_name(self, code):
        """Extract the main class name from Java code"""
        # Look for public class definition
        match = re.search(r'public\s+class\s+(\w+)', code)
        if match:
            return match.group(1)
        
        # Look for any class definition
        match = re.search(r'class\s+(\w+)', code)
        if match:
            return match.group(1)
            
        # If no class found, generate a default class name
        return None
    
    def _wrap_code_in_class(self, code):
        """Wrap code snippet in a main class if needed"""
        # Check if code already has a class definition
        if re.search(r'class\s+\w+', code):
            # Check if it has a main method
            if 'public static void main' not in code:
                # Add main method if missing
                lines = code.split('\n')
                # Find the class body and insert main method
                for i, line in enumerate(lines):
                    if '{' in line and 'class' in lines[max(0, i-1)] or 'class' in line:
                        # Insert after the opening brace
                        indent = '    '
                        main_method = [
                            f'{indent}public static void main(String[] args) {{',
                        ]
                        # Move existing code into main
                        lines.insert(i + 1, '\n'.join(main_method))
                        break
                return '\n'.join(lines)
            return code
        else:
            # Wrap in a default class with main method
            self.class_counter += 1
            class_name = f'JupyterJava{self.class_counter}'
            wrapped_code = f"""public class {class_name} {{
    public static void main(String[] args) {{
{self._indent_code(code, 2)}
    }}
}}"""
            return wrapped_code
    
    def _indent_code(self, code, levels):
        """Indent code by specified number of levels (4 spaces each)"""
        indent = '    ' * levels
        return '\n'.join(indent + line if line.strip() else line 
                        for line in code.split('\n'))
    
    def do_execute(self, code, silent, store_history=True, 
                   user_expressions=None, allow_stdin=False):
        """Execute Java code"""
        
        if not code.strip():
            return {
                'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': {},
            }
        
        # Wrap code in class if necessary
        full_code = self._wrap_code_in_class(code)
        
        # Extract class name
        class_name = self._extract_class_name(full_code)
        if not class_name:
            class_name = f'JupyterJava{self.class_counter}'
        
        # Use persisting temporary directory for compilation classes
        tmpdir = self.temp_dir.name
        
        # Write Java file
        java_file = os.path.join(tmpdir, f'{class_name}.java')
        with open(java_file, 'w', encoding='utf-8') as f:
            f.write(full_code)
        
        # Compile Java code
        try:
            compile_result = subprocess.run(
                ['javac', java_file],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=tmpdir
            )
            
            if compile_result.returncode != 0:
                if not silent:
                    error_message = compile_result.stderr
                    self.send_response(self.iopub_socket, 'stream', {
                        'name': 'stderr',
                        'text': f'Compilation Error:\n{error_message}'
                    })
                
                return {
                    'status': 'error',
                    'execution_count': self.execution_count,
                    'ename': 'CompilationError',
                    'evalue': 'Java compilation failed',
                    'traceback': [compile_result.stderr]
                }
            
            # Run compiled Java code
            run_result = subprocess.run(
                ['java', '-cp', tmpdir, class_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if not silent:
                # Send stdout
                if run_result.stdout:
                    self.send_response(self.iopub_socket, 'stream', {
                        'name': 'stdout',
                        'text': run_result.stdout
                    })
                
                # Send stderr
                if run_result.stderr:
                    self.send_response(self.iopub_socket, 'stream', {
                        'name': 'stderr',
                        'text': run_result.stderr
                    })
            
            if run_result.returncode != 0:
                return {
                    'status': 'error',
                    'execution_count': self.execution_count,
                    'ename': 'RuntimeError',
                    'evalue': 'Java execution failed',
                    'traceback': [run_result.stderr]
                }
            
        except subprocess.TimeoutExpired:
            if not silent:
                self.send_response(self.iopub_socket, 'stream', {
                    'name': 'stderr',
                    'text': 'Execution timed out (30 seconds limit)'
                })
            
            return {
                'status': 'error',
                'execution_count': self.execution_count,
                'ename': 'TimeoutError',
                'evalue': 'Execution exceeded time limit',
                'traceback': ['Execution timed out after 30 seconds']
            }
        
        except FileNotFoundError as e:
            if not silent:
                self.send_response(self.iopub_socket, 'stream', {
                    'name': 'stderr',
                    'text': f'Error: Java compiler not found. Please install JDK.\n{str(e)}'
                })
            
            return {
                'status': 'error',
                'execution_count': self.execution_count,
                'ename': 'JavaNotFoundError',
                'evalue': 'Java not found',
                'traceback': [str(e)]
            }
        
        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=JavaKernel)
