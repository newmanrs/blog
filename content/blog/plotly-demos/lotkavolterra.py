import numpy as np
from scipy.integrate import ode
import plotly.graph_objects as go
import decimal

# ODE parameters for Lotka-Volterra Model

# dx/dt = alpha*x - beta x*y
# dy/dt = delta*x*y - gamma*y
# alpha, beta, gamma, delta > 0
alpha = 2/3
beta = 4/3
gamma = 1
delta = 1
t0 = 0
z0 = [1.0, 1.0]


# Integrator steps
Npts = 481   # If you see +1, it's so the slider includes endpoint
dt = '0.05'  # Use string not float for exact decimal fmt strings later on


# plot params
c1 = "#54278f"
c2 = "#807dba"
xmin = 0
xmax = 2
ymin = 0
ymax = 1.2

# output
outputfile = 'lotkavolterra.html'
inc_mathjax = False     # False or 'cdn'
inc_plotlyjs = False    # True, False, or 'cdn'

#Formatting parameters for plot
d = decimal.Decimal(dt)
tdecs = -d.as_tuple().exponent
tfmt = f".{tdecs}f"  #Make format based on decimals of dt
xfmt = ".3f"
yfmt = ".3f"
frame_duration = 16
marker_size = 20

def lotkavolterra(t, z, alpha, beta, gamma, delta):
    """
    Lotka-Volterra system in argument order for scipy.
    """
    x, y = z
    dzdt = [
        alpha * x - beta * x * y,
        delta * x * y - gamma * y
        ]
    return dzdt

# Config scipy ODE
r = ode(lotkavolterra).set_integrator('zvode', method='bdf')
r.set_initial_value(z0,t0).set_f_params(alpha,beta,gamma,delta)

t = np.zeros(Npts)
x = np.zeros(Npts)
y = np.zeros(Npts)
x[0] = z0[0]
y[0] = z0[1]

# Integrate
dt = float(dt)
for i in range(Npts-1):
    t[i+1] = r.t + dt
    # You'd think the integator would need
    # to know exact dt, but apparently not.
    z_i= r.integrate(r.t+dt)  #integrating dz/dx
    # Cast to real and pack into x,y vectors for plotting
    x[i+1] = np.real(z_i[0])
    y[i+1] = np.real(z_i[1])

def datapoint_text(idx : int, t, x, y):  # t,x,y arrays to index into
    return f"Time t={t[idx]:{tfmt}}, X(t)={x[idx]:{xfmt}}, Y(t)={y[idx]:{yfmt}}"

fig_dict = {
    "data":[
        go.Scatter(
            x=[x[0]],
            y=[y[0]],
            mode="markers",
            marker=dict(size=marker_size, color=c1),
            name = "t",
            hoverinfo = 'text',
            text = [datapoint_text(0,t,x,y)],
                ),
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            line=dict(width=2, color=c2),
            name = 'limit cycle',
            hoverinfo = 'text',
            text = [f"X(t)={i:{xfmt}}, Y(t)={j:{yfmt}}" for (i,j) in zip(x,y)]
            )],
    "layout":go.Layout(
        xaxis=dict(range=[xmin, xmax], autorange=False, zeroline=True),
        yaxis=dict(range=[ymin, ymax], autorange=False, zeroline=True),
        xaxis_title='x(t)',
        yaxis_title='y(t)',
        #title="Lotka-Volterra Predator-Prey Model",
        hovermode="closest",
        updatemenus=[]  # Button controls added here later
        ),
    "frames":
        [ # Begin list comprehension of frames for animation
            go.Frame(
                data=[
                    go.Scatter(
                        x=[x[k]], #List of one point
                        y=[y[k]],
                        hoverinfo = 'text',
                        text = [datapoint_text(k,t,x,y)], # Set mouseover
                        mode="markers",
                        marker=dict(color=c1, size=marker_size)
                    )
                    ],
                name = f'{k}' # Must match slider frame name
                )

        for k in range(Npts)
        ] # End list comprehension of frames
}

# Button control for start/stop and animation speed
fig_dict["layout"]["updatemenus"] = [
    {
    "buttons":
        [
            {
            "label": "Play",
            "method": "animate",
            "args": [
                None,
                {"frame":
                    {
                    "duration": frame_duration,
                    "redraw": False
                    },
                "fromcurrent": True,
                "transition":
                    {
                    "duration": frame_duration,
                    "easing": "linear"
                    }
                }],
            },
            # Pause Button
            {
            "label": "Pause",
            "method": "animate",
            "args": [
                [None],
                {"frame":
                    {
                    "duration": 0,
                    "redraw": False
                    },
                    "mode": "immediate"
                }],
            },
            # Reset Button
           # {
           # "label": "Reset",
           # "method": "animate",
           # "args": [
           #     None,
           #     {"frame":
           #         {
           #         "duration": 0,
           #         "redraw": False
           #         },
           #         "mode": "immediate",
           #     "fromcurrent": False
           #     }],
           # }
        ],
    "direction": "left",
    "pad": {"r": 0, "t": 0},
    "type": "buttons",
    "x": 0.0,
    "xanchor": "left",
    "y": -0.06,
    "yanchor": "top"
    }
]


sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 14},
        "prefix": r"Time ",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration":50, "easing": "cubic-in-out"},
    #"pad": {"b": 10, "t": 20},
    #"pad" : {"r": 50},
    "len": 1.0,
    "x": 0,
    "y": -0.05,
    "minorticklen" : 0,
    "steps": []
}

for i in range(0,Npts):
    slider_step = {"args": [
        [f'{i}'], # Match figure text exactly for slider to sync
        {"frame": {"duration": 50, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 50}}
    ],
        "label": f't={i*dt+t0:{tfmt}}',
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)


fig_dict["layout"]["sliders"] = [sliders_dict]



fig = go.Figure(fig_dict)

# lol why were examples not built in this api
# instead of dictionary madness?
fig.update_layout(
    # Move legend into graph
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99
        ),
    # Move title to LHS, and lower
    title=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0
        ),
    # Default margins are 80
    margin=dict(
        b=80,  # Bottom Top Left Right
        t=40,
        l=80,
        r=40,
        )
    )

fig.write_html(
    outputfile,
    auto_play=False,
    include_mathjax=inc_mathjax,
    include_plotlyjs=inc_plotlyjs)
print(f"Done writing html file {outputfile}")
