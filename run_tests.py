#!/usr/bin/env python3
"""
Test Runner Script

This script runs the test suite for the Business Automation System.
"""

import os
import sys
import subprocess
import argparse

def run_tests(test_path=None, verbose=False):
    """
    Run the test suite.
    
    Args:
        test_path: Path to specific test file or directory
        verbose: Whether to run tests in verbose mode
    """
    # Set up command
    cmd = ['pytest']
    
    # Add verbose flag if requested
    if verbose:
        cmd.append('-v')
    
    # Add test path if specified
    if test_path:
        cmd.append(test_path)
    
    # Run tests
    result = subprocess.run(cmd)
    
    return result.returncode

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Run the test suite for the Business Automation System')
    parser.add_argument('--path', help='Path to specific test file or directory')
    parser.add_argument('-v', '--verbose', action='store_true', help='Run tests in verbose mode')
    
    args = parser.parse_args()
    
    # Run tests
    return run_tests(args.path, args.verbose)

if __name__ == '__main__':
    sys.exit(main())

