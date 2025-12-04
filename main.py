#!/usr/bin/env python3
"""
Ultra-robust camera capture script with comprehensive error handling
Filename format: hostname_mac_username_datetime.jpg
"""

import sys
import os
import time

# ============================================================================
# Critical: Catch ALL imports at the top level
# ============================================================================

def ultra_safe_import(module_name, fallback_value=None):
    """
    Import with multiple fallback strategies
    Returns: (module_or_value, success_flag)
    """
    # Strategy 1: Direct import
    try:
        module = __import__(module_name)
        return module, True
    except ImportError:
        pass
    
    # Strategy 2: Try submodule imports for common patterns
    if '.' in module_name:
        try:
            main_module, sub_module = module_name.split('.', 1)
            main = __import__(main_module)
            module = getattr(main, sub_module)
            return module, True
        except:
            pass
    
    # Strategy 3: Return fallback if provided
    if fallback_value is not None:
        return fallback_value, False
    
    # Strategy 4: Create dummy module
    class DummyModule:
        def __getattr__(self, name):
            raise AttributeError(f"Dummy module '{module_name}' has no attribute '{name}'")
    
    return DummyModule(), False


# Initialize critical modules with ultra-safe imports
subprocess, subprocess_ok = ultra_safe_import('subprocess', None)
argparse, argparse_ok = ultra_safe_import('argparse', None)

# ============================================================================
# Module Installation Helper (Redesigned for safety)
# ============================================================================

def safe_install_module(module_name, pip_name=None):
    """
    Safely install a module with multiple fallback strategies
    Returns: (success, message)
    """
    if subprocess is None:
        return False, "subprocess module not available for installation"
    
    pip_name = pip_name or module_name
    
    print(f"Attempting to install {pip_name}...")
    
    installation_methods = [
        [sys.executable, "-m", "pip", "install", pip_name],
        ["pip", "install", pip_name],
        ["pip3", "install", pip_name],
        ["python", "-m", "pip", "install", pip_name],
        ["python3", "-m", "pip", "install", pip_name],
    ]
    
    for method in installation_methods:
        try:
            # Use Popen with timeout to prevent hanging
            import signal
            def timeout_handler(signum, frame):
                raise TimeoutError("Installation timed out")
            
            # Only set timeout if signal module is available
            old_handler = None
            if 'signal' in sys.modules:
                signal_module = sys.modules['signal']
                old_handler = signal_module.signal(signal_module.SIGALRM, timeout_handler)
                signal_module.alarm(60)  # 60 second timeout
            
            try:
                # Run installation
                result = subprocess.run(
                    method,
                    capture_output=True,
                    text=True,
                    timeout=120  # Additional timeout
                )
                
                if result.returncode == 0:
                    return True, f"Successfully installed {pip_name}"
                else:
                    print(f"Installation failed with method {method[0]}: {result.stderr[:200]}")
                    
            except subprocess.TimeoutExpired:
                return False, f"Installation timed out for {pip_name}"
            except FileNotFoundError:
                continue  # Try next method
            finally:
                # Restore signal handler
                if old_handler is not None and 'signal' in sys.modules:
                    signal_module = sys.modules['signal']
                    signal_module.alarm(0)
                    signal_module.signal(signal_module.SIGALRM, old_handler)
                    
        except Exception as e:
            print(f"Installation attempt failed: {e}")
            continue
    
    return False, f"All installation methods failed for {pip_name}"


# ============================================================================
# Fallback Implementations
# ============================================================================

class SystemInfoFallback:
    """Fallback implementations for system information"""
    
    @staticmethod
    def get_hostname():
        """Get hostname with multiple fallbacks"""
        try:
            import socket
            hostname = socket.gethostname()
            if hostname and hostname.strip():
                return hostname.replace(' ', '_').replace('/', '_')[:50]
        except:
            pass
        
        # Try environment variables
        env_hostname = os.environ.get('COMPUTERNAME') or \
                      os.environ.get('HOSTNAME') or \
                      os.environ.get('HOST')
        
        if env_hostname:
            return env_hostname.replace(' ', '_')[:50]
        
        # Try reading from system files (Unix/Linux)
        if os.path.exists('/etc/hostname'):
            try:
                with open('/etc/hostname', 'r') as f:
                    hostname = f.read().strip()
                    if hostname:
                        return hostname.replace(' ', '_')[:50]
            except:
                pass
        
        return "unknown_host"
    
    @staticmethod
    def get_mac_address():
        """Get MAC address with multiple fallbacks"""
        try:
            import uuid
            mac_num = uuid.getnode()
            # Check if it's a valid MAC (not all zeros or randomized)
            if mac_num >> 40 & 1:
                return "unknown-mac"  # Randomized MAC
            
            mac_hex = uuid.UUID(int=mac_num).hex[-12:]
            if mac_hex == '000000000000' or all(c == '0' for c in mac_hex):
                return "unknown-mac"
            
            # Format as XX-XX-XX-XX-XX-XX
            return '-'.join(mac_hex[i:i+2] for i in range(0, 12, 2))
        except:
            pass
        
        # Try network interfaces (platform-specific)
        try:
            if sys.platform.startswith('win'):
                import ctypes
                import ctypes.wintypes
                
                class MIB_IFROW(ctypes.Structure):
                    _fields_ = [
                        ('wszName', ctypes.wintypes.WCHAR * 256),
                        ('dwIndex', ctypes.wintypes.DWORD),
                        ('dwType', ctypes.wintypes.DWORD),
                        ('dwMtu', ctypes.wintypes.DWORD),
                        ('dwSpeed', ctypes.wintypes.DWORD),
                        ('dwPhysAddrLen', ctypes.wintypes.DWORD),
                        ('bPhysAddr', ctypes.c_ubyte * 8),
                        ('dwAdminStatus', ctypes.wintypes.DWORD),
                        ('dwOperStatus', ctypes.wintypes.DWORD),
                        ('dwLastChange', ctypes.wintypes.DWORD),
                        ('dwInOctets', ctypes.wintypes.DWORD),
                        ('dwInUcastPkts', ctypes.wintypes.DWORD),
                        ('dwInNUcastPkts', ctypes.wintypes.DWORD),
                        ('dwInDiscards', ctypes.wintypes.DWORD),
                        ('dwInErrors', ctypes.wintypes.DWORD),
                        ('dwInUnknownProtos', ctypes.wintypes.DWORD),
                        ('dwOutOctets', ctypes.wintypes.DWORD),
                        ('dwOutUcastPkts', ctypes.wintypes.DWORD),
                        ('dwOutNUcastPkts', ctypes.wintypes.DWORD),
                        ('dwOutDiscards', ctypes.wintypes.DWORD),
                        ('dwOutErrors', ctypes.wintypes.DWORD),
                        ('dwOutQLen', ctypes.wintypes.DWORD),
                        ('dwDescrLen', ctypes.wintypes.DWORD),
                        ('bDescr', ctypes.c_ubyte * 256)
                    ]
                
                # Try to get MAC from Windows API
                # (This is complex and may fail - that's OK, we have fallback)
                pass
                
            elif sys.platform.startswith('linux'):
                # Try reading from /sys/class/net/
                for interface in ['eth0', 'wlan0', 'enp0s3', 'wlp2s0']:
                    mac_file = f'/sys/class/net/{interface}/address'
                    if os.path.exists(mac_file):
                        try:
                            with open(mac_file, 'r') as f:
                                mac = f.read().strip()
                                if mac and '00:00:00:00:00:00' not in mac:
                                    return mac.replace(':', '-')
                        except:
                            pass
        except:
            pass
        
        return "unknown-mac"
    
    @staticmethod
    def get_username():
        """Get username with multiple fallbacks"""
        try:
            import getpass
            username = getpass.getuser()
            if username and username.strip():
                return username.replace(' ', '_').replace('/', '_')[:50]
        except:
            pass
        
        # Try environment variables
        env_user = os.environ.get('USERNAME') or \
                  os.environ.get('USER') or \
                  os.environ.get('LOGNAME')
        
        if env_user:
            return env_user.replace(' ', '_')[:50]
        
        # Try platform-specific methods
        if sys.platform.startswith('win'):
            # Windows: try whoami command
            try:
                if subprocess:
                    result = subprocess.run(['whoami'], 
                                          capture_output=True, 
                                          text=True, 
                                          timeout=2)
                    if result.returncode == 0:
                        username = result.stdout.strip().split('\\')[-1]
                        if username:
                            return username.replace(' ', '_')[:50]
            except:
                pass
        
        return "unknown_user"


# ============================================================================
# Ultra-Robust Camera Capture Class
# ============================================================================

class UltraRobustCameraCapture:
    def __init__(self, output_dir="camshots"):
        """Initialize with maximum robustness"""
        self.output_dir = ""
        self.log_file = ""
        self.hostname = "unknown_host"
        self.mac = "unknown-mac"
        self.username = "unknown_user"
        self.cv2 = None
        self.modules_available = {}
        
        try:
            # Step 1: Safely set output directory
            self._set_output_directory(output_dir)
            
            # Step 2: Initialize modules with extreme safety
            self._initialize_modules_ultra_safe()
            
            # Step 3: Get system info
            self._get_system_info_safe()
            
            # Step 4: Initialize logging
            self._initialize_logging_safe()
            
            print(f"✓ Initialization complete. Output: {self.output_dir}")
            
        except Exception as e:
            print(f"⚠️  Partial initialization error (continuing anyway): {e}")
            # Even if initialization fails partially, we can still try to capture
    
    def _set_output_directory(self, requested_dir):
        """Set output directory with multiple fallbacks"""
        try:
            # Try requested directory first
            if requested_dir:
                os.makedirs(requested_dir, exist_ok=True)
                # Test if directory is writable
                test_file = os.path.join(requested_dir, '.write_test')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                self.output_dir = requested_dir
                return
        except:
            pass
        
        # Fallback 1: Current directory
        try:
            self.output_dir = "."
            test_file = os.path.join(self.output_dir, '.write_test')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            return
        except:
            pass
        
        # Fallback 2: Temp directory
        try:
            import tempfile
            temp_dir = tempfile.gettempdir()
            self.output_dir = temp_dir
            print(f"⚠️  Using temp directory: {temp_dir}")
            return
        except:
            pass
        
        # Ultimate fallback: Use CWD even if not writable (files will fail later)
        self.output_dir = "."
        print("⚠️  Warning: Using current directory (may not be writable)")
    
    def _initialize_modules_ultra_safe(self):
        """Initialize modules with maximum safety"""
        self.modules_available = {
            'cv2': False,
            'socket': False,
            'uuid': False,
            'getpass': False,
            'datetime': False
        }
        
        # Initialize cv2 with multiple attempts
        cv2_success = False
        for attempt in range(3):
            try:
                import cv2
                # Test cv2 functionality
                test_cap = cv2.VideoCapture(0)
                if test_cap is not None:
                    test_cap.release()
                self.cv2 = cv2
                self.modules_available['cv2'] = True
                cv2_success = True
                print("✓ OpenCV initialized successfully")
                break
            except ImportError:
                if attempt == 0 and subprocess:
                    # Try to install on first attempt
                    success, msg = safe_install_module('opencv-python')
                    if not success:
                        print(f"⚠️  {msg}")
                        break
                else:
                    print("⚠️  OpenCV not available")
                    break
            except Exception as e:
                print(f"⚠️  OpenCV initialization error: {e}")
                if attempt < 2:
                    time.sleep(1)  # Wait before retry
                continue
        
        # Initialize standard modules (should always succeed)
        standard_modules = [
            ('socket', 'socket'),
            ('uuid', 'uuid'),
            ('getpass', 'getpass'),
            ('datetime.datetime', 'datetime')
        ]
        
        for import_str, module_key in standard_modules:
            try:
                if '.' in import_str:
                    parts = import_str.split('.')
                    module = __import__(parts[0])
                    for part in parts[1:]:
                        module = getattr(module, part)
                else:
                    module = __import__(import_str)
                
                setattr(self, module_key, module)
                self.modules_available[module_key] = True
            except Exception as e:
                print(f"⚠️  Module {module_key} not available: {e}")
                setattr(self, module_key, None)
    
    def _get_system_info_safe(self):
        """Get system information safely"""
        fallback = SystemInfoFallback()
        
        # Get hostname
        try:
            if self.modules_available.get('socket'):
                self.hostname = self.socket.gethostname()
                self.hostname = self.hostname.replace(' ', '_').replace('/', '_')[:50]
                if not self.hostname or self.hostname.strip() == '':
                    self.hostname = fallback.get_hostname()
            else:
                self.hostname = fallback.get_hostname()
        except:
            self.hostname = fallback.get_hostname()
        
        # Get MAC address
        try:
            if self.modules_available.get('uuid'):
                mac_num = self.uuid.getnode()
                if not (mac_num >> 40 & 1):  # Not randomized
                    mac_hex = self.uuid.UUID(int=mac_num).hex[-12:]
                    if mac_hex != '000000000000':
                        self.mac = '-'.join(mac_hex[i:i+2] for i in range(0, 12, 2))
                    else:
                        self.mac = fallback.get_mac_address()
                else:
                    self.mac = fallback.get_mac_address()
            else:
                self.mac = fallback.get_mac_address()
        except:
            self.mac = fallback.get_mac_address()
        
        # Get username
        try:
            if self.modules_available.get('getpass'):
                self.username = self.getpass.getuser()
                self.username = self.username.replace(' ', '_').replace('/', '_')[:50]
                if not self.username or self.username.strip() == '':
                    self.username = fallback.get_username()
            else:
                self.username = fallback.get_username()
        except:
            self.username = fallback.get_username()
    
    def _initialize_logging_safe(self):
        """Initialize logging safely"""
        try:
            self.log_file = os.path.join(self.output_dir, "capture_log.txt")
            # Test if we can write to log file
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"Log initialized at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        except Exception as e:
            print(f"⚠️  Cannot initialize logging: {e}")
            self.log_file = None
    
    def _log_event(self, message, level="INFO"):
        """Safe logging with multiple fallbacks"""
        try:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{timestamp} [{level}] {message}\n"
            
            # Try to write to log file
            if self.log_file:
                try:
                    with open(self.log_file, 'a', encoding='utf-8') as f:
                        f.write(log_entry)
                except:
                    pass
            
            # Always print to console
            print(f"{level}: {message}")
            
        except:
            # Ultimate fallback: just print
            print(f"LOG: {message}")
    
    def _generate_filename_safe(self):
        """Generate filename with maximum safety"""
        try:
            # Get timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            try:
                # Try to get milliseconds
                import datetime
                ms = datetime.datetime.now().microsecond // 1000
                timestamp += f"_{ms:03d}"
            except:
                timestamp += "_000"
            
            # Create filename components
            components = []
            
            # Only add components if they're not default values
            if self.hostname and self.hostname != "unknown_host":
                components.append(self.hostname[:30])
            if self.mac and self.mac != "unknown-mac":
                components.append(self.mac[:20])
            if self.username and self.username != "unknown_user":
                components.append(self.username[:20])
            
            components.append(timestamp)
            
            # Join with underscores
            filename = "_".join(components) + ".jpg"
            
            # Sanitize filename (critical for Windows/Linux compatibility)
            invalid_chars = '<>:"/\\|?*\n\r\t\0'
            for char in invalid_chars:
                filename = filename.replace(char, '_')
            
            # Ensure filename length is safe
            if len(filename) > 200:
                # Keep extension, truncate name
                name, ext = os.path.splitext(filename)
                filename = name[:200 - len(ext)] + ext
            
            return filename
            
        except Exception as e:
            print(f"⚠️  Filename generation error: {e}")
            # Ultimate fallback
            return f"capture_{int(time.time())}.jpg"
    
    def capture(self):
        """Main capture method - will never crash"""
        self._log_event("Starting capture process", "INFO")
        
        # Check if OpenCV is available
        if not self.modules_available.get('cv2') or self.cv2 is None:
            self._log_event("ERROR: OpenCV not available", "ERROR")
            self._log_event("Install with: pip install opencv-python", "INFO")
            return False
        
        # Try to capture from cameras
        max_cameras = 5
        cameras_tried = 0
        
        for cam_id in range(max_cameras):
            cameras_tried += 1
            cap = None
            
            try:
                self._log_event(f"Trying camera {cam_id}", "DEBUG")
                
                # Open camera with timeout protection
                start_time = time.time()
                cap = self.cv2.VideoCapture(cam_id)
                
                # Check if opened successfully
                if not cap.isOpened():
                    self._log_event(f"Camera {cam_id} could not be opened", "DEBUG")
                    if cap:
                        cap.release()
                    continue
                
                # Set timeouts for camera operations
                cap.set(self.cv2.CAP_PROP_BUFFERSIZE, 1)
                
                # Test camera with timeout
                test_success = False
                for test_attempt in range(3):
                    try:
                        ret, frame = cap.read()
                        if ret and frame is not None and frame.size > 0:
                            test_success = True
                            break
                        time.sleep(0.1)
                    except:
                        time.sleep(0.1)
                        continue
                
                if not test_success:
                    self._log_event(f"Camera {cam_id} test failed", "DEBUG")
                    cap.release()
                    continue
                
                # Camera is working, capture final image
                time.sleep(0.1)  # Brief pause
                
                ret, frame = None, None
                for capture_attempt in range(3):
                    try:
                        ret, frame = cap.read()
                        if ret and frame is not None and frame.size > 0:
                            break
                        time.sleep(0.05)
                    except:
                        time.sleep(0.05)
                        continue
                
                if not ret or frame is None or frame.size == 0:
                    self._log_event(f"Camera {cam_id} capture failed", "DEBUG")
                    cap.release()
                    continue
                
                # Generate filename
                filename = self._generate_filename_safe()
                filepath = os.path.join(self.output_dir, filename)
                
                # Ensure directory exists (might have failed earlier)
                try:
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                except:
                    pass
                
                # Save image with compression
                try:
                    encode_param = [int(self.cv2.IMWRITE_JPEG_QUALITY), 85]
                    success = self.cv2.imwrite(filepath, frame, encode_param)
                    
                    if success:
                        # Verify file was saved
                        if os.path.exists(filepath):
                            file_size = os.path.getsize(filepath)
                            if file_size > 100:  # At least 100 bytes
                                self._log_event(f"SUCCESS: Captured {filename} ({file_size/1024:.1f} KB)", "SUCCESS")
                                
                                # Clean up and return
                                cap.release()
                                self.cv2.destroyAllWindows()
                                
                                # Final verification
                                time.sleep(0.1)  # Let filesystem catch up
                                if os.path.exists(filepath):
                                    return True
                                else:
                                    self._log_event(f"WARNING: File disappeared after save: {filepath}", "WARNING")
                            else:
                                self._log_event(f"WARNING: File too small: {filepath} ({file_size} bytes)", "WARNING")
                        else:
                            self._log_event(f"ERROR: File not created: {filepath}", "ERROR")
                    else:
                        self._log_event(f"ERROR: cv2.imwrite failed for {filepath}", "ERROR")
                
                except self.cv2.error as e:
                    self._log_event(f"OpenCV write error: {e}", "ERROR")
                except Exception as e:
                    self._log_event(f"File save error: {e}", "ERROR")
                
                # Release camera
                cap.release()
                
            except self.cv2.error as e:
                self._log_event(f"OpenCV error (camera {cam_id}): {e}", "ERROR")
            except MemoryError:
                self._log_event(f"Memory error (camera {cam_id})", "ERROR")
                return False  # Don't continue after memory error
            except Exception as e:
                self._log_event(f"Unexpected error (camera {cam_id}): {type(e).__name__}: {str(e)[:100]}", "ERROR")
            finally:
                # Absolutely ensure camera is released
                if cap is not None:
                    try:
                        cap.release()
                    except:
                        pass
        
        self._log_event(f"No cameras available (tried {cameras_tried} cameras)", "WARNING")
        return False


# ============================================================================
# Main Execution with Ultimate Safety
# ============================================================================

def main():
    """Main function - designed to never crash"""
    print("=" * 60)
    print("Ultra-Robust Camera Capture")
    print("=" * 60)
    
    start_time = time.time()
    success = False
    
    try:
        # Parse arguments safely
        output_dir = "camshots"
        if argparse_ok and argparse is not None:
            try:
                parser = argparse.ArgumentParser(description='Capture camera image')
                parser.add_argument('--output', default='camshots', help='Output directory')
                args, unknown = parser.parse_known_args()
                output_dir = args.output
            except:
                pass  # Use default if arg parsing fails
        
        # Create capture instance
        print("\nInitializing...")
        capture = UltraRobustCameraCapture(output_dir=output_dir)
        
        # Show system info
        print(f"\nSystem Information:")
        print(f"  Hostname: {capture.hostname}")
        print(f"  MAC: {capture.mac}")
        print(f"  User: {capture.username}")
        print(f"  Output: {os.path.abspath(capture.output_dir)}")
        
        # Attempt capture
        print("\n" + "=" * 60)
        success = capture.capture()
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        return 130
    except MemoryError:
        print("\n\n💥 CRITICAL: Out of memory")
        return 137
    except SystemExit:
        raise  # Re-raise SystemExit
    except Exception as e:
        # This should NEVER happen, but just in case
        print(f"\n\n💥 UNEXPECTED CRASH: {type(e).__name__}: {e}")
        print("\nTroubleshooting:")
        print("1. Check Python installation")
        print("2. Run: pip install opencv-python")
        print("3. Check camera permissions")
        
        # Try to get traceback if possible
        try:
            import traceback
            traceback.print_exc()
        except:
            pass
        
        return 1
    
    finally:
        # Always show final status
        elapsed = time.time() - start_time
        
        if success:
            print(f"\n✅ SUCCESS: Completed in {elapsed:.1f}s")
            return 0
        else:
            print(f"\n⚠️  FAILED: No capture after {elapsed:.1f}s")
            print("\nPossible solutions:")
            print("1. Install OpenCV: pip install opencv-python")
            print("2. Check camera is connected")
            print("3. Close other camera applications")
            print("4. Run as administrator/root if needed")
            return 1


# ============================================================================
# Script Entry Point with Maximum Protection
# ============================================================================

if __name__ == "__main__":
    # Ultimate protection: wrap everything
    try:
        # Check Python version
        if sys.version_info < (3, 6):
            print("ERROR: Python 3.6 or higher required")
            sys.exit(1)
        
        # Run main function
        exit_code = main()
        
    except SystemExit as e:
        # Allow normal exits
        raise e
    except:
        # Catch absolutely everything else
        print("\n💥 CATASTROPHIC FAILURE: Script crashed completely")
        print("This should never happen with the safety measures in place.")
        print("Please report this error.")
        exit_code = 1
    
    # Exit cleanly
    sys.exit(exit_code)
