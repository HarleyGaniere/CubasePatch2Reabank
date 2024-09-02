import os
import re

def convert_cubase_to_reabank(cubase_file_name, reabank_file_name):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct full paths for the input and output files
    cubase_file_path = os.path.join(script_dir, cubase_file_name)
    reabank_file_path = os.path.join(script_dir, reabank_file_name)
    
    with open(cubase_file_path, 'r') as infile, open(reabank_file_path, 'w') as outfile:
        outfile.write("// ReaBank file generated from Cubase MIDI patch file\n\n")
        
        msb = 63  # MSB is constant at 63
        lsb = 0   # Start LSB
        program_number = 0
        patch_start = 0  # Start range for the first bank
        
        # Start by writing the first bank header
        outfile.write(f"Bank {msb} {lsb} Patches {patch_start} - {patch_start + 127}\n")
        
        for line in infile:
            # Match the pattern: "[p2, 0, 63, 0] Pn:CFX + FM EP"
            match = re.match(r'\[p\d+,\s*(\d+),\s*63,\s*(\d+)\]\s+(.+)', line.strip())
            if match:
                # Extract the patch name
                patch_name = match.group(3)
                
                # Write the patch/program line
                outfile.write(f"{program_number} {patch_name}\n")
                program_number += 1  # Increment program number

                # Check if program number reached 128, if so, reset and increment LSB for a new bank
                if program_number > 127:
                    lsb += 1  # Increment LSB for a new bank
                    patch_start += 128  # Update the patch start for the new bank range
                    program_number = 0  # Reset program number for the new bank
                    outfile.write(f"\nBank {msb} {lsb} Patches {patch_start} - {patch_start + 127}\n")
    
    print(f"Conversion complete! ReaBank file saved as '{reabank_file_name}'")

# Example usage with files in the same folder
cubase_file_name = "your_cubase_patch_file.txt"  # Make sure this file is in the same folder as the script
reabank_file_name = "output_reabank_file.reabank"
convert_cubase_to_reabank(cubase_file_name, reabank_file_name)
