#!/usr/bin/env python3
"""Test file for the blockcode library."""

import random
from blockcode import Block_code, weight, send, binary

def test_basic_functionality():
    """Test basic encoding, decoding, and error correction."""
    print("Testing basic functionality...")
    b = Block_code([0, 22, 13, 27])
    
    # Test properties
    assert b.k == 2, f"Expected k=2, got {b.k}"
    assert b.n == 5, f"Expected n=5, got {b.n}"
    print(f"✓ Block code parameters: k={b.k}, n={b.n}, d_min={b.d_min}")
    print(f"✓ Max detectable errors: {b.max_detectable}")
    print(f"✓ Max correctable errors: {b.max_correctable}")

def test_encoding_decoding():
    """Test encoding and decoding without errors."""
    print("\nTesting encoding and decoding...")
    b = Block_code([0, 22, 13, 27])
    
    for msg in range(1 << b.k):
        encoded = b.encode(msg)
        decoded = b.decode(encoded)
        assert msg == decoded, f"Failed: msg={msg}, encoded={encoded}, decoded={decoded}"
    
    print(f"✓ All {1 << b.k} messages encode and decode correctly")

def test_error_correction():
    """Test error correction capabilities."""
    print("\nTesting error correction...")
    b = Block_code([0, 22, 13, 27])
    
    test_iterations = 1000
    errors_corrected = 0
    
    for _ in range(test_iterations):
        for msg in range(1 << b.k):
            codeword = b.encode(msg)
            
            # Test with random number of errors up to max_detectable - 1
            num_errors = random.randint(0, b.max_detectable - 1)
            received = send(codeword, b.n, num_errors)[0]
            
            try:
                corrected = b.correct(received)
                decoded = b.decode(corrected)
                assert msg == decoded, f"Failed: msg={msg}, decoded={decoded}"
                errors_corrected += num_errors
            except ValueError as e:
                print(f"✗ Error correction failed: {e}")
                return False
    
    print(f"✓ All {test_iterations * (1 << b.k)} test cases passed")
    print(f"✓ Total errors corrected: {errors_corrected}")
    return True

def test_helper_functions():
    """Test helper functions."""
    print("\nTesting helper functions...")
    
    # Test weight function
    assert weight(0) == 0, "weight(0) should be 0"
    assert weight(1) == 1, "weight(1) should be 1"
    assert weight(7) == 3, "weight(7) should be 3"
    assert weight(8) == 1, "weight(8) should be 1"
    print("✓ weight() function works correctly")
    
    # Test binary function
    assert binary(0, 4) == [0, 0, 0, 0], "binary(0) failed"
    assert binary(5, 4) == [0, 1, 0, 1], "binary(5) failed"
    assert binary(15, 4) == [1, 1, 1, 1], "binary(15) failed"
    print("✓ binary() function works correctly")

def test_edge_cases():
    """Test edge cases and error handling."""
    print("\nTesting edge cases...")
    b = Block_code([0, 22, 13, 27])
    
    # Test encoding/decoding of boundary values
    msg_min = 0
    msg_max = (1 << b.k) - 1
    
    encoded_min = b.encode(msg_min)
    encoded_max = b.encode(msg_max)
    
    assert msg_min == b.decode(encoded_min), "Failed to decode min message"
    assert msg_max == b.decode(encoded_max), "Failed to decode max message"
    print("✓ Boundary values handled correctly")
    
    # Test detectable but uncorrectable errors (2 errors)
    # Code can detect these but should raise error since not correctable
    codeword = b.encode(3)  # Valid message
    detectable_errors = b.max_detectable  # 2 errors
    (received, error_pattern, error_positions) = send(codeword, b.n, detectable_errors)
    
    print(f"  Testing {detectable_errors} detectable errors (should raise error)")
    try:
        b.correct(received)
        print(f"  ⚠ Warning: Should have raised error for uncorrectable errors\n errors= {detectable_errors}, error_pattern = {binary(error_pattern, b.n)}, error_positions = {error_positions}, n = {b.n}")
    except ValueError as e:
        print(f"  ✓ Correctly detected uncorrectable errors: {e}")

def main():
    """Run all tests."""
    print("=" * 50)
    print("BLOCKCODE LIBRARY TEST SUITE")
    print("=" * 50)
    
    try:
        #test_basic_functionality()
        #test_encoding_decoding()
        #test_helper_functions()
        test_edge_cases()
        #success = test_error_correction()
        
        #print("\n" + "=" * 50)
        #if success:
        #    print("ALL TESTS PASSED ✓")
        #else:
        #    print("SOME TESTS FAILED ✗")
        #print("=" * 50)
        
    except Exception as e:
        print(f"\n✗ TEST SUITE FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
