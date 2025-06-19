"""
Pytest configuration and shared fixtures for TaskValidator tests.
"""

import pytest
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.validation.task_validator import TaskValidator


@pytest.fixture(scope="session")
def validator():
    """Shared TaskValidator instance for all tests."""
    return TaskValidator()


@pytest.fixture
def sample_excellent_submission():
    """High-quality submission for testing."""
    class ExcellentSubmission:
        def __init__(self):
            self.code = """
def binary_search(arr, target):
    '''
    Search for target in sorted array using binary search.
    Time complexity: O(log n)
    Space complexity: O(1)
    '''
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Not found
            """
            
            self.mathematical_reasoning = """
Binary Search Algorithm Analysis:

Theorem: Binary search finds an element in a sorted array in O(log n) time.

Proof:
At each step, we eliminate half of the remaining search space.
Starting with n elements, after k iterations we have at most ⌈n/2^k⌉ elements.

The algorithm terminates when we have ≤ 1 element, so:
⌈n/2^k⌉ ≤ 1
n/2^k ≤ 1
n ≤ 2^k
log₂(n) ≤ k

Therefore, the algorithm terminates in at most ⌈log₂(n)⌉ iterations.

Correctness Invariant:
If target exists in the array, it must be in arr[left:right+1].
This invariant is maintained throughout the algorithm.

Base case: Initially, target could be anywhere in arr[0:n-1].
Inductive step: After comparing with arr[mid], we eliminate either
arr[left:mid-1] or arr[mid+1:right], preserving the invariant.

Space complexity: O(1) as we only use constant additional variables.
            """
    
    return ExcellentSubmission()


@pytest.fixture
def sample_poor_submission():
    """Low-quality submission for testing."""
    class PoorSubmission:
        def __init__(self):
            self.code = """
def find_thing(stuff, thing):
    for i in range(len(stuff)):
        if stuff[i] == thing:
            return i
    return -1
            """
            
            self.mathematical_reasoning = """
This function finds stuff.
            """
    
    return PoorSubmission()


@pytest.fixture
def sample_syntax_error_submission():
    """Submission with syntax errors for testing error handling."""
    class SyntaxErrorSubmission:
        def __init__(self):
            self.code = """
def broken_function(x:
    return x * 2
            """
            
            self.mathematical_reasoning = """
This function should multiply by 2.
            """
    
    return SyntaxErrorSubmission()


# Test configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )