import powerlaw
import matplotlib
matplotlib.use('agg')
from matplotlib.pylab import plot

counts=[116893,
    63762,
    35812,
    25942,
    21522,
    15294,
    12436,
    7693,
    6679,
    5918,
    5651,
    4748,
    4439,
    3861,
    3434,
    3417,
    3024,
    2932,
    2569,
    2468,
    2219,
    1722,
    1499,
    1450,
    1333,
    1315,
    1190,
    1139,
    1070,
    1027,
    928,
    845,
    818,
    781,
    742,
    702,
    609,
    575,
    558,
    516]
results = powerlaw.Fit(counts)
print(results.power_law.alpha)
print(results.power_law.xmin)
R, p = results.distribution_compare('power_law', 'lognormal')
print("R, p for power law and lognormal {}, {}".format(R,p))

R, p = results.distribution_compare('power_law', 'exponential')
print("R, p for power law and exponential {}, {}".format(R,p))

R, p = results.distribution_compare('lognormal', 'exponential')
print("R, p for lognormal and exponential {}, {}".format(R,p))

fit = results

fig = fit.plot_ccdf(linewidth=3, label='Empirical Data')
fit.power_law.plot_ccdf(ax=fig, color='r', linestyle='--', label='Power law fit')
fit.lognormal.plot_ccdf(ax=fig, color='g', linestyle='--', label='Lognormal fit')
fit.exponential.plot_ccdf(ax=fig, color='b', linestyle='--', label='Exponential fit')
####
fig.set_ylabel(u"p(X≥x)")
fig.set_xlabel("Chat Message Count")
handles, labels = fig.get_legend_handles_labels()
fig.legend(handles, labels, loc=3)

figname = 'ccdf'
matplotlib.pyplot.savefig(figname+'.png', bbox_inches='tight')

print("power law coefficient alpha {}".format(fit.alpha))
