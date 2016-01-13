"""graphdmc.py
Plot the dmc.hist file from a CASINO DMC job. Plot saved as SVG file.

NOTE: Unlike the graphdmc function this script has no support for dmc.hist files
without monotonically increasing lines

#Changes (Date DDMMYYYY,User,Change)
09012016    Shiv    Initial Commit
13012016    Shiv    Formatting
"""
import numpy as np
import re
import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
plt.rc('font', family='serif', size=12)
# Read Column Names
data_items = ["line_numbers"]
with open("dmc.hist") as infile:
    line = infile.readline()
    while (re.search('data items', line, re.IGNORECASE) is None):
        line = infile.readline()
    line = infile.readline()
    while (re.search('Raw QMC data', line, re.IGNORECASE) is None):
        data_items.append(line.replace("#", "").strip())
        line = infile.readline()
dmc = np.loadtxt('dmc.hist', dtype=np.float_)
# Plot
walkers = dmc[:, data_items.index("NCONF")]
fig = plt.figure(facecolor='white', figsize=(16, 9))
ax = fig.add_subplot(211)
plt.plot(dmc[:, 0], walkers, color='firebrick', linewidth=0.5)
plt.xlim(0, len(dmc))
plt.ylim(0, 1.1 * max(walkers))
for axis in ['top', 'bottom', 'left', 'right']:
    ax.spines[axis].set_linewidth(3)
ax.xaxis.set_tick_params(width=2.5, length=7)
ax.yaxis.set_tick_params(width=2.5, length=7)
plt.xlabel(r'$\tau$', fontsize=24)
plt.ylabel(r'Population', fontsize=24)
plt.title(
    r'Imaginary time evolution of walker population',
    y=1.08,
    fontsize=24)
# Energies plot
estimate = dmc[:, data_items.index("EBEST")]
avg_local = dmc[:, data_items.index("ETOT")]
reference = dmc[:, data_items.index("EREF")]
ax2 = fig.add_subplot(212)
plt.plot(dmc[:, 0], avg_local, color='black', linewidth=0.5)
plt.plot(dmc[:, 0], reference, color='firebrick', linewidth=0.5)
plt.plot(dmc[:, 0], estimate, color='chartreuse', linewidth=0.5)
plt.xlim(0, len(dmc))
# y lim is chosen from the min/max of average local energy because that has the
# largest variation
estimate_mean = np.sum(estimate) / len(estimate)
plt.ylim(min(avg_local), max(avg_local))
for axis in ['top', 'bottom', 'left', 'right']:
    ax2.spines[axis].set_linewidth(3)
ax2.xaxis.set_tick_params(width=2.5, length=7)
ax2.yaxis.set_tick_params(width=2.5, length=7)
avg_local_patch = mpatches.Patch(color='black', label='Total local energy')
reference_patch = mpatches.Patch(color='firebrick', label='Reference energy')
estimate_patch = mpatches.Patch(
    color='chartreuse',
    label='Best estimate energy')
ax2.legend(
    handles=[
        avg_local_patch,
        reference_patch,
        estimate_patch],
    fontsize=12)
plt.xlabel(r'$\tau$', fontsize=24)
plt.ylabel(r'Energy (a.u.)', fontsize=24)
plt.title(r'Imaginary time evolution of DMC energies', y=1.08, fontsize=24)
fig.tight_layout()
fig.savefig('output.svg', format="svg")
