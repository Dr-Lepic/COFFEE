"""Installation script for Java Kernel"""

import argparse
import json
import os
import sys
from jupyter_client.kernelspec import KernelSpecManager
from pathlib import Path


def install_kernel_spec(user=True, prefix=None):
    """Install the Java kernel spec"""
    
    # Get the path to the kernel.json file
    kernel_json_path = Path(__file__).parent / 'java_kernel' / 'kernel.json'
    
    if not kernel_json_path.exists():
        print(f"Error: kernel.json not found at {kernel_json_path}")
        sys.exit(1)
    
    # Read kernel.json
    with open(kernel_json_path) as f:
        kernel_json = json.load(f)
    
    # Update argv to use absolute path
    python_executable = sys.executable
    kernel_json['argv'][0] = python_executable
    
    # Create temporary directory for kernel spec
    import tempfile
    import shutil
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_kernel_dir = Path(tmpdir) / 'java'
        tmp_kernel_dir.mkdir()
        
        # Write updated kernel.json
        with open(tmp_kernel_dir / 'kernel.json', 'w') as f:
            json.dump(kernel_json, f, indent=2)
        
        # Copy logo files if they exist
        logo_dir = Path(__file__).parent / 'java_kernel'
        for logo_file in ['logo-32x32.png', 'logo-64x64.png']:
            logo_path = logo_dir / logo_file
            if logo_path.exists():
                shutil.copy(logo_path, tmp_kernel_dir / logo_file)
        
        # Install kernel spec
        ksm = KernelSpecManager()
        
        try:
            ksm.install_kernel_spec(
                str(tmp_kernel_dir),
                kernel_name='java',
                user=user,
                prefix=prefix
            )
            print("Java kernel installed successfully!")
            print(f"Kernel spec location: {ksm.get_kernel_spec('java').resource_dir}")
            
        except Exception as e:
            print(f"Error installing kernel spec: {e}")
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Install the Java Jupyter kernel'
    )
    parser.add_argument(
        '--user',
        action='store_true',
        help='Install kernel spec in user directory'
    )
    parser.add_argument(
        '--sys-prefix',
        action='store_true',
        help='Install kernel spec in sys.prefix'
    )
    parser.add_argument(
        '--prefix',
        help='Install kernel spec in given prefix'
    )
    
    args = parser.parse_args()
    
    user = args.user or not (args.sys_prefix or args.prefix)
    prefix = args.prefix
    
    if args.sys_prefix:
        prefix = sys.prefix
    
    install_kernel_spec(user=user, prefix=prefix)


if __name__ == '__main__':
    main()
