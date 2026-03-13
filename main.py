# ------------------------------------------------------------
# Student Name       : Kiran Manikandan
# Student ID         : 24062131
# University         : University of Hertfordshire
# Last Modifide Date : 13-03-2025

# Copyright (c) 2026 Kiran Manikandan
# ------------------------------------------------------------

import sys
import os

# ----- Faced problem with fetching the file. So, added a quick fix by importing the directory -----
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.simulation import SimulationManager

def main():
    print("=" * 60)
    print("HOME ROBOT SIMULATOR")
    print("=" * 60)
    print("\n OBJECTIVE:")
    print("  Guide the robot from start to target while avoiding")
    print("  furniture and obstacles in a family-friendly home.")
    print("\n FEATURES:")
    print("  • 5-sensor obstacle detection")
    print("  • Real-time collision avoidance")
    # print("  • Multiple home layouts")
    print("  • Performance tracking")
    print("\n CONTROLS:")
    print("  SPACE - Pause/Resume")
    print("  R - Reset simulation")
    print("  Arrow Up /Arrow Down - Increase/Decrease speed")
    print("  0 - Mixed home layout")
    print("  1 - Living room layout")
    print("  2 - Kitchen layout")
    print("  3 - Bedroom layout")
    print("\n Starting simulation...\n")
    
    # ----- Create and Run Simullation -----
    simulation_manager = SimulationManager()
    simulation_manager.run()

if __name__ == "__main__":
    main()