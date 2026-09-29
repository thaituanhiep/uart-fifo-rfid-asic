#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
MASTER VERIFICATION SUITE - PicoRV32 RFID RDM6300 SoC
===============================================================================
Executes all design-step testbenches sequentially:
  - Step 2: Firmware & Communication Protocol (21 Tests)
  - Step 3: CPU PicoRV32 & 1KB Data SRAM (12 Tests)
  - Step 4: SPI Flash Controller - spimemio (10 Tests)
  - Step 5: RDM6300 5-Stage Autonomous Hardware Pipeline (12 Tests)
  - Step 6: Full SoC Integration (8 Tests)
===============================================================================
Total: 63 Test Cases
===============================================================================
"""

import sys
import os
import subprocess
import time
import io

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

STEPS = [
    {
        "id": "Step 2",
        "name": "Firmware & Protocol Testbench",
        "dir": "step2_firmware",
        "script": "test_firmware.py",
        "expected_tests": 21
    },
    {
        "id": "Step 3",
        "name": "PicoRV32 & 1KB SRAM Testbench",
        "dir": "step3_picorv32_sram",
        "script": "test_picorv32_sram.py",
        "expected_tests": 12
    },
    {
        "id": "Step 4",
        "name": "SPI Flash Controller (spimemio) Testbench",
        "dir": "step4_spimemio_flash",
        "script": "test_spimemio.py",
        "expected_tests": 10
    },
    {
        "id": "Step 5",
        "name": "RDM6300 5-Stage Hardware Pipeline Testbench",
        "dir": "step5_rdm6300_pipeline",
        "script": "test_rdm6300_pipeline.py",
        "expected_tests": 12
    },
    {
        "id": "Step 6",
        "name": "Full SoC Integration Testbench",
        "dir": "step6_top_soc_integration",
        "script": "test_top_soc.py",
        "expected_tests": 8
    }
]

def main():
    tb_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 80)
    print("       PicoRV32 RFID RDM6300 ASIC/FPGA - MASTER TESTBENCH SUITE")
    print("=" * 80)
    print(f"Base Directory: {tb_dir}\n")

    results = []
    total_passed = 0
    total_expected = sum(s["expected_tests"] for s in STEPS)
    start_time = time.time()

    for idx, step in enumerate(STEPS, 1):
        step_dir = os.path.join(tb_dir, step["dir"])
        step_script = os.path.join(step_dir, step["script"])

        print("-" * 80)
        print(f"[{idx}/{len(STEPS)}] RUNNING: {step['id']} - {step['name']}")
        print(f"       Folder: tb/{step['dir']}/")
        print(f"       Script: {step['script']}")
        print("-" * 80)

        step_start = time.time()
        res = subprocess.run(
            [sys.executable, step["script"]],
            cwd=step_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        step_duration = time.time() - step_start

        # Print script output indented
        for line in res.stdout.strip().splitlines():
            print(f"  | {line}")

        passed = (res.returncode == 0)
        results.append({
            "step": step["id"],
            "name": step["name"],
            "dir": step["dir"],
            "tests": step["expected_tests"],
            "passed": passed,
            "duration": step_duration
        })

        if passed:
            total_passed += step["expected_tests"]
            print(f"\n  >>> RESULT: {step['id']} PASSED ({step['expected_tests']}/{step['expected_tests']} Tests) in {step_duration:.2f}s\n")
        else:
            print(f"\n  >>> RESULT: {step['id']} FAILED (Exit Code {res.returncode}) in {step_duration:.2f}s\n")

    elapsed_total = time.time() - start_time

    # ========================================================================
    # Summary Table
    # ========================================================================
    print("=" * 80)
    print("                       VERIFICATION SUMMARY REPORT")
    print("=" * 80)
    print(f"{'Step':<8} | {'Module / Scope':<38} | {'Folder':<20} | {'Tests':<6} | {'Status'}")
    print("-" * 80)

    all_passed = True
    for r in results:
        status_str = "PASS [100%]" if r["passed"] else "FAIL [ERR]"
        if not r["passed"]:
            all_passed = False
        print(f"{r['step']:<8} | {r['name']:<38} | {r['dir']:<20} | {r['tests']:<6} | {status_str}")

    print("=" * 80)
    print(f"  TOTAL TESTS EXECUTED : {total_expected}")
    print(f"  TOTAL TESTS PASSED   : {total_passed} ({(total_passed / total_expected) * 100:.1f}%)")
    print(f"  TOTAL TESTS FAILED   : {total_expected - total_passed}")
    print(f"  TOTAL ELAPSED TIME   : {elapsed_total:.2f} seconds")
    print("=" * 80)

    if all_passed and total_passed == total_expected:
        print("  >>> ALL 63 TEST CASES ACROSS ALL 5 STEPS PASSED 100%! <<<")
        print("  >>> CHIP ARCHITECTURE & FIRMWARE VERIFIED SUCCESSFULLY <<<")
        print("=" * 80)
        sys.exit(0)
    else:
        print("  >>> SOME TEST CASES FAILED! PLEASE CHECK THE LOGS ABOVE. <<<")
        print("=" * 80)
        sys.exit(1)

if __name__ == "__main__":
    main()
