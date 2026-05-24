"""Entry point for the Java kernel"""

from ipykernel.kernelapp import IPKernelApp
from .kernel import JavaKernel

if __name__ == '__main__':
    IPKernelApp.launch_instance(kernel_class=JavaKernel)
