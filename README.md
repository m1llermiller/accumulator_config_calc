# Accumulator Config Generator

Program flow from user perspective:
* Selects a cell type, selects target voltage and voltage tolerance, selects energy target and energy tolerance
* All potential accumulator configurations for the given cell choice are taken - all viable configurations are output onto a spreadsheet
* Additional rules (for FSUK compliance) can then be tested against for each configuration

Unlike the excel spreadsheet version of this program, all calculations will be based purely on the cells - not the cells within the ENEPAQ style strips.
This program is purely to represent the cumulative properties of the cells - not the accumulator as a whole. 

Assumption for this program is that all the cell modules will be placed in series. 

