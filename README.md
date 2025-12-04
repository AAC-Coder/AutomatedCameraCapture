Fixed Crash Points and Safety Measures:
1. Import Failures (Previously could crash)
All imports wrapped in try-except

Multiple import strategies

Dummy modules for missing imports

Graceful degradation

2. Subprocess Issues (Installation could hang/crash)
Timeout handling with signal module

Multiple installation methods

Capture output to prevent hanging

Proper cleanup

3. File System Problems
Directory creation with permission testing

Multiple fallback directories (temp, CWD)

File write testing before attempting

Filename length and character sanitization

4. Camera Hardware Issues
Timeouts for camera operations

Multiple test attempts

Frame validation (size, emptiness)

Proper resource cleanup in finally blocks

5. Memory Issues
Catch MemoryError explicitly

Frame size validation

Early returns on memory errors

6. Thread/Signal Safety
Signal handler restoration

No threading, but safe for interruption

Proper cleanup on KeyboardInterrupt

7. Platform-Specific Issues
Windows/Linux/Mac compatibility

Different path separators

Platform-specific system info gathering

Environment variable fallbacks

8. OpenCV-Specific Crashes
cv2.error exception catching

Camera release even after errors

DestroyAllWindows() called safely

9. Unicode/Encoding Issues
UTF-8 encoding for log files

String sanitization for filenames

Safe string operations

10. Ultimate Safety Net
Top-level try-except for everything

Never uses bare except: statements

Always provides error messages

Clean exit codes

What Won't Crash This Version:
Missing modules - Uses fallbacks or installs automatically

No write permissions - Falls back to temp directory

Camera disconnected during capture - Handled gracefully

Out of memory - Catches MemoryError and exits cleanly

User interruption (Ctrl+C) - Proper cleanup and exit

Invalid filenames - Automatic sanitization

Camera in use - Detects and skips

OpenCV initialization failure - Continues without camera

Network issues (for MAC/hostname) - Uses fallbacks

Filesystem full - Fails gracefully with error message
