"""Advanced signal processing challenges focusing on audio compression."""

import re
import numpy as np
from typing import Any, Tuple, List, Dict
from src.core.challenge import (
    Challenge, ChallengeLevel, MathematicalDomain, 
    MathematicalRequirement, TestCase
)


class AudioCompressionChallenge(Challenge):
    """Audio compression challenge requiring advanced signal processing and transforms."""
    
    def __init__(self):
        mathematical_requirements = [
            MathematicalRequirement(
                concept="Fourier Transform",
                description="Derive and implement the Discrete Fourier Transform and its Fast algorithm",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Wavelet Transform",
                description="Derive and implement a wavelet transform for multi-resolution analysis",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Psychoacoustic Model",
                description="Implement a mathematical model of human hearing for perceptual coding",
                proof_required=True
            ),
            MathematicalRequirement(
                concept="Quantization and Entropy Coding",
                description="Implement optimal bit allocation and entropy coding",
                complexity_analysis=True
            )
        ]
        
        # Generate test cases programmatically
        test_cases = self._generate_test_cases()
        
        super().__init__(
            title="Advanced Audio Compression System",
            description="""
Implement a complete audio compression system based on mathematical transforms and psychoacoustic principles.

Your implementation must include:
1. A time-frequency transform (FFT, MDCT, or Wavelet Transform)
2. A psychoacoustic model based on human auditory perception
3. Quantization with optimal bit allocation
4. Entropy coding for the final bitstream

Mathematical Proof Requirements:
- Derive the mathematical basis for your chosen transform (FFT, MDCT, or Wavelets)
- Prove the properties of your transform that make it suitable for audio compression
- Derive the mathematical model for frequency masking in your psychoacoustic model
- Analyze the rate-distortion tradeoff in your compression system

Example Usage:
```python
# Create audio compressor with psychoacoustic model
compressor = AudioCompressor(
    transform_type="mdct",
    window_size=1024,
    psychoacoustic_model="simplified"
)

# Read audio file and compress
original_audio = read_audio_file("sample.wav")
compressed_data = compressor.compress(original_audio, target_bitrate=128000)

# Decompress audio
reconstructed_audio = compressor.decompress(compressed_data)

# Calculate quality metrics
snr = signal_to_noise_ratio(original_audio, reconstructed_audio)
compression_ratio = len(original_audio) * 16 / len(compressed_data)  # Assuming 16-bit audio
```
            """,
            level=ChallengeLevel.ADVANCED,
            domain=MathematicalDomain.CALCULUS,
            mathematical_requirements=mathematical_requirements,
            test_cases=test_cases,
            time_limit=1500.0
        )
    
    def _generate_test_cases(self) -> List[TestCase]:
        """Generate test cases for audio compression implementations."""
        test_cases = []
        
        # Generate synthetic audio signal for testing
        sample_rate = 44100
        duration = 1.0  # 1 second
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        
        # Simple test signal with multiple frequencies
        freqs = [440, 880, 1320]  # A4, A5, E6
        test_signal = sum(0.5 * np.sin(2 * np.pi * f * t) for f in freqs) / len(freqs)
        
        # Test case for DFT/FFT implementation
        test_cases.append(TestCase(
            input_data={
                "operation": "transform",
                "signal": test_signal.tolist()[:1024],  # First 1024 samples
                "transform_type": "fft"
            },
            expected_output={
                "transform_valid": True,
                "inverse_transform_error": lambda x: x < 1e-10,  # Error should be near zero
                "peaks_at_correct_frequencies": True
            },
            description="FFT implementation and validation"
        ))
        
        # Test case for wavelet transform
        test_cases.append(TestCase(
            input_data={
                "operation": "transform",
                "signal": test_signal.tolist()[:1024],
                "transform_type": "wavelet",
                "wavelet_type": "db4"  # Daubechies 4 wavelet
            },
            expected_output={
                "transform_valid": True,
                "multi_resolution_property": True,
                "inverse_transform_error": lambda x: x < 1e-10
            },
            description="Wavelet transform implementation"
        ))
        
        # Test case for psychoacoustic model
        test_cases.append(TestCase(
            input_data={
                "operation": "masking_threshold",
                "signal": test_signal.tolist()[:4096],
                "sample_rate": sample_rate
            },
            expected_output={
                "threshold_follows_spectrum": True,
                "threshold_shape_valid": True,
                "accounts_for_masking": True
            },
            description="Psychoacoustic model"
        ))
        
        # Test case for full compression system
        test_cases.append(TestCase(
            input_data={
                "operation": "compress",
                "signal": test_signal.tolist(),
                "sample_rate": sample_rate,
                "target_bitrate": 64000  # 64 kbps
            },
            expected_output={
                "compression_ratio": lambda x: x > 5.0,  # At least 5:1 compression
                "snr": lambda x: x > 20.0,  # SNR at least 20 dB
                "perceptual_quality": lambda x: x > 3.5  # PEAQ score > 3.5 (out of 5)
            },
            description="Complete audio compression system",
            timeout=20.0
        ))
        
        # Test case for bit allocation and entropy coding
        test_cases.append(TestCase(
            input_data={
                "operation": "bit_allocation",
                "spectrum": np.abs(np.fft.rfft(test_signal[:1024])).tolist(),
                "masking_threshold": [0.01] * 513,  # Simplified masking threshold
                "available_bits": 2048
            },
            expected_output={
                "bits_used_efficiently": True,
                "follows_perceptual_importance": True,
                "entropy_coding_gain": lambda x: x > 1.2  # At least 20% gain from entropy coding
            },
            description="Bit allocation and entropy coding"
        ))
        
        return test_cases
    
    def verify_mathematical_reasoning(self, submission: str) -> Tuple[float, str]:
        """Verify mathematical reasoning in audio compression solution."""
        score = 0.0
        feedback_parts = []
        
        # Check for transform derivation
        if self._contains_transform_derivation(submission):
            score += 0.25
            feedback_parts.append("✓ Mathematical transform properly derived")
        else:
            feedback_parts.append("✗ Missing derivation of the mathematical transform")
        
        # Check for psychoacoustic model
        if self._contains_psychoacoustic_model(submission):
            score += 0.25
            feedback_parts.append("✓ Psychoacoustic model mathematically explained")
        else:
            feedback_parts.append("✗ Missing mathematical explanation of psychoacoustic principles")
        
        # Check for quantization analysis
        if self._contains_quantization_analysis(submission):
            score += 0.25
            feedback_parts.append("✓ Quantization and bit allocation properly analyzed")
        else:
            feedback_parts.append("✗ Missing analysis of quantization and bit allocation")
        
        # Check for entropy coding
        if self._contains_entropy_coding_explanation(submission):
            score += 0.25
            feedback_parts.append("✓ Entropy coding mathematically explained")
        else:
            feedback_parts.append("✗ Missing mathematical explanation of entropy coding")
        
        return score, "; ".join(feedback_parts)
    
    def analyze_complexity(self, submission: str) -> Tuple[bool, str]:
        """Analyze if submission meets complexity requirements."""
        # Check for efficient implementations
        if (self._has_efficient_transform(submission) and 
            self._has_efficient_coding(submission)):
            return True, "Efficient algorithms for transforms and entropy coding detected"
        elif self._has_efficient_transform(submission):
            return False, "Transform implementation is efficient, but entropy coding needs improvement"
        elif self._has_efficient_coding(submission):
            return False, "Entropy coding is efficient, but transform implementation needs improvement"
        else:
            return False, "Both transform and entropy coding implementations need efficiency improvements"
    
    def _contains_transform_derivation(self, text: str) -> bool:
        """Check if submission derives the mathematical transform."""
        patterns = [
            r'fourier\s+transform',
            r'discrete\s+cosine\s+transform',
            r'modified\s+discrete\s+cosine\s+transform',
            r'wavelet\s+transform',
            r'time-frequency\s+resolution'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_psychoacoustic_model(self, text: str) -> bool:
        """Check if submission explains the psychoacoustic model."""
        patterns = [
            r'psychoacoustic\s+model',
            r'masking\s+threshold',
            r'critical\s+band',
            r'bark\s+scale',
            r'frequency\s+masking'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_quantization_analysis(self, text: str) -> bool:
        """Check if submission analyzes quantization and bit allocation."""
        patterns = [
            r'quantization',
            r'bit\s+allocation',
            r'rate.*distortion',
            r'signal-to-noise\s+ratio',
            r'perceptual\s+weighting'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _contains_entropy_coding_explanation(self, text: str) -> bool:
        """Check if submission explains entropy coding."""
        patterns = [
            r'entropy\s+coding',
            r'huffman\s+coding',
            r'arithmetic\s+coding',
            r'information\s+theory',
            r'lossless\s+compression'
        ]
        return any(re.search(pattern, text.lower()) for pattern in patterns)
    
    def _has_efficient_transform(self, code: str) -> bool:
        """Check for efficient transform implementation."""
        patterns = [
            r'fft',
            r'fast\s+fourier\s+transform',
            r'butterfly',
            r'cooley.*tukey',
            r'numpy\.fft'
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)
    
    def _has_efficient_coding(self, code: str) -> bool:
        """Check for efficient entropy coding."""
        patterns = [
            r'huffman\s+tree',
            r'arithmetic\s+coding',
            r'range\s+coding',
            r'priority\s+queue',
            r'compressio.*ratio'
        ]
        return any(re.search(pattern, code.lower()) for pattern in patterns)