#!/usr/bin/env python
# coding: utf-8

# # DoseTestSteps.py
# Calculates doses for multiplicative dose step in an electron beam lithography dose test
# 
# Alan R. Bleier, Cornell NanoScale Facility, April 17, 2023
# 
# To use this script, enter: 
# 
# * N, the number of doses
# * D_0, the initial dose
# * D_N, the final dose
# * OutputFileLocation, ending in "/"
# * jdiName, the JEOL .jdi file name for the modulation table, including the ".jdi" at the end
# 
# Then run it in a jupyter notebook, or at a unix command line using
# 
# ```
# python3 DoseTestSteps.py
# ```
# 
# Output:
# 
# * Comma separated variable files of relative doses for reading into LayoutBEAMER Feature Dose Assignment module, using the Import... button (see the GenISys application note "Resist Contrast Measurement")
#     * Relative doses assigned to layer values  
#     * Relative doses assigned to datatype values  
# * JEOL .jdi file
# 
# **The GDS file for a contrast curve or a dose test is assumed to contain multiple copies of the same pattern in layers 1 through N. The .jdi file produced by this script can be included in the job deck file to assign relative doses to each layer. **
# 
# **If the GenISys LayoutBEAMER Feature Dose Assignment ("FDA") module imports the comma separated list produced by this script, it assigns doses to JEOL shot ranks 0 through N-1. So if FDA is used, the .jdi file produced by LayoutBEAMER should be used, NOT the .jdi file produced by this script.**
# 
# If proximity correction is needed for the dose test, then it is not possible to use multiple copies of the same pattern in one GDS file. In this case, one can just use the list of doses as base doses in multiple exposures in the JEOL schedule file.
# 
# This software is distributed under the BSD 3-Clause "New" or "Revised" License https://directory.fsf.org/wiki/License:BSD-3-Clause

# Copyright (c) 2023 Alan R. Bleier
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#     (1) Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer. 
# 
#     (2) Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.  
#     
#     (3)The name of the author may not be used to
#     endorse or promote products derived from this software without
#     specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE. 

# In[21]:


N = 18
D_0 = 75.0 # Must be a floating point number, not integer
D_N = 700.0 # Must be a floating point number, not integer
OutputFileLocation = "/afs/cnf.cornell.edu/home/staff/bleier_a/private/CAD/"
jdiName = "modulationtable.jdi"

print("Number of doses:  " + str(N))
print("Initial dose: " + str(D_0) + " uC/cm^2")
print("Final dose: " + str(D_N) + " uC/cm^2")

import numpy as np
f=np.exp((1/(N-1)) * (np.log(D_N) - np.log(D_0) ) )
print("Multiplicative factor from one step to the next: ", str(f) + "\n")


# In[22]:


doses = []
roundedDoses = []
relativeDoses = []
modulationTable = []

for n in range(1, N+1):
    doses.append(D_0 * f**(n-1))
    roundedDoses.append(round(D_0 * f**(n-1), 1))

print("Doses: " + "\n" + str(roundedDoses) + "\n") 
print ("Mean dose: " + str(round(np.mean(doses), 1)) + " uC/cm^2" + "\n")


# In[23]:


percentIncreasesForJDF = []
for n in range(0, N):
    percentIncreasesForJDF.append(round(100.0*(f**(n)-1),1))
# print("Percent increases from base dose, for JEOL job deck file: " + "\n" + str(percentIncreasesForJDF) + "\n")

# modulation table should look like this: MOD001: MODULAT ((0, 20.0), (1, 25.0))

modulationTable.clear()
modulationTable.append("MOD001: MODULAT (")
for n in range(0, N-1):
    modulationTable.append("(" + str(n+1) + ", " + str(percentIncreasesForJDF[n]) + "), ") 
modulationTable.append("(" + str(N) + ", " + str(percentIncreasesForJDF[N-1]) + "))")
print("Modulation table for JEOL job deck file: ")
print(' '.join(modulationTable) + "\n")


# In[24]:


# Write comma separated variable file of relative doses for reading into LayoutBEAMER Feature Dose Assignment 
# module, using the Import... button (see the GenISys application note "Resist Contrast Measurement")

for n in range(0, N):
    relativeDoses.append(doses[n]/doses[0])
# print("Doses relative to first dose: " + "\n" + str(relativeDoses))

LayersDosesList = OutputFileLocation + "LayersDosesList.csv"
print("The list of doses assigned to GDS layers for use with the LayoutBEAMER Feature Dose Assignment module is " + LayersDosesList + "\n")
file1 = open(LayersDosesList, "w")
for n in range(0, N):
    file1.write(str(n+1) + "(0)," + str(relativeDoses[n]) + "\n")
file1.close()

DatatypesDosesList = OutputFileLocation + "DatatypesDosesList.csv"
print("The list of doses assigned to GDS datatypes for use with the LayoutBEAMER Feature Dose Assignment module is " + DatatypesDosesList + "\n")
file1 = open(OutputFileLocation + "DatatypesDosesList.csv", "w")
for n in range(0, N):
    file1.write("0" + "(" + str(n+1) + ")," + str(relativeDoses[n]) + "\n")
file1.close()


# In[25]:


# Write JEOL .jdi modulation table file

jdiFile = OutputFileLocation + jdiName
print("The JEOL jdi file is " + jdiFile)
file1 = open(jdiFile, "w")
modulationTableString=str(' '.join(modulationTable))
file1.write(modulationTableString + "\n\n" + "; Modulation table for manual assignment of doses to layers \n; Not for use when BEAMER FDA module has been used\n")
file1.close()


# In[ ]:




