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
z0 = [[1.0, 0.6], [1.0,0.8], [1.0, 1.0],[1.0,0.52]]
Ntraj = len(z0)


# Stride the integrator arrays to reduce
# number of plot points by this factor to
# decouple plot lagginess from ODE integrator
# accuracy (tied to dt)
stride = 2
# Integrator steps
Npts = 600 +stride+1  # +stride+1 makes endpoint inclusive
dt = '0.04'  # Use string not float for exact decimal fmt strings later on

# plot params
carr = ["#54278f",
        "#33a02c",
        "#54cbd1",
        "#1f78b4",
        "#ee7f22",
        "#c90000",
        "#9c1c93",
        "#fb9a99",
        ]

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
marker_size = 12

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
odeints = []

#Allocate data arrays
t = np.zeros(Npts)
x = np.zeros((Npts,Ntraj))
y = np.zeros((Npts,Ntraj))

# ODE integrators, method selected by 'does not concurrent error'.
# For a quick plot probably don't need rigorous testing of accuracy
# anyways.
for i in range(Ntraj):
    r = ode(lotkavolterra).set_integrator('dopri5',  method='bdf')
    r.set_f_params(alpha,beta,gamma,delta)
    r.set_initial_value(z0[i],t0)
    odeints.append(r)

    x[0][i] = z0[i][0]
    y[0][i] = z0[i][1]

# Integrate
dt = float(dt)
for i in range(Npts-1):
    t[i+1] = r.t + dt

    for j in range(Ntraj):
        z_i= odeints[j].integrate(r.t+dt)  # integrating dz/dx
        # Cast to real and pack into x,y vectors for plotting
        x[i+1][j] = np.real(z_i[0])
        y[i+1][j] = np.real(z_i[1])


# Stride data to speed up the final plot
t = t[0::stride]
x = x[0::stride,:]
y = y[0::stride,:]
Npts = Npts//stride
dt = dt*stride


def datapoint_text(row : int, col : int, t, x, y):
    """
    Mousever helper function for the scatterplot individual points.
    """
    ti = t[row]
    xi = x[row][col]
    yi = y[row][col]
    return f"Time t={ti:{tfmt}}, x(t)={xi:{xfmt}}, y(t)={yi:{yfmt}}"

# Begin core of the plot function in older build-a-dict blindly and
# yolo at once API.  Example plotly animations got ugly to change here
# when they start populating lists of nested dictionaries 5 levels deep
# containing list comprehensions.
fig_dict = {
    "data":[],
    "layout": go.Layout(
        xaxis=dict(range=[xmin, xmax], autorange=False, zeroline=True),
        yaxis=dict(range=[ymin, ymax], autorange=False, zeroline=True),
        xaxis_title='x(t)',
        yaxis_title='y(t)',
        #title="PlotTitle",
        hovermode="closest",
        updatemenus=[]  # Button controls added here later
        ),
    "frames": [], # Plot frames added here later.
   }

def make_frame_figure_data(tidx):

    data = []
    for col in range(Ntraj):
        # Plot the initial conditions as a marker
        # at the current tidx point
        p = go.Scatter(
            name=f"Trajectory {col}",
            x=[x[tidx][col]],
            y=[y[tidx][col]],
            mode="markers",
            marker=dict(size=marker_size, color=carr[col]),
            hoverinfo='text',
            text=[datapoint_text(0,col,t,x,y)],
            )
        data.append(p)

        # Update the trajectory only on tidx = 0
        #  i.e. these parts are fixed and need not be redrawn
        if tidx == 0:
            # Trajectory plots
            p = go.Scatter(
                x=x[:,col],
                y=y[:,col],
                mode="lines",
                line=dict(width=2, color=carr[col]),
                name=f'x<sub>0</sub>={z0[col][0]}, y<sub>0</sub>={z0[col][1]}',
                hoverinfo='text',
                # Text needs to be list for each point too
                text=[f"x(t={t:{tfmt}})={i:{xfmt}}, y(t={t:{tfmt}})={j:{yfmt}}"
                    for (i,j,t) in zip(x[:,col],y[:,col],t)]
                )
            data.append(p)
            # Fixed ghost of initial scatterpoint
            p = go.Scatter(
                name=f"fixed_small_inital_cond {col}",
                x=[x[tidx][col]],
                y=[y[tidx][col]],
                mode="markers",
                marker=dict(size=int(marker_size*2/3), color=carr[col]),
                hoverinfo='text',
                text=[datapoint_text(0,col,t,x,y)],
                showlegend=False
                )
            data.append(p)

        else:
            # not t=0, pass no-op object that gives no updates
            # merge logic is probably __dict__.update(**kwargs)
            p = go.Scatter()
            data.append(p)
            data.append(p)
    return data


fig_dict['data']=make_frame_figure_data(tidx=0)

#fig_dict["frames"] needs list above plots to update
frames = []
frame_names = [f'frame_{k}' for k in range(Npts)]
for k in range(Npts):
    data = make_frame_figure_data(tidx=k)
    # Frame_names are used to sync with sliders by the
    # backend so this must match at tag:FRAME_SLIDER_NAMES
    frames.append(go.Frame(data=data, name = frame_names[k]))

fig_dict['frames'] = frames

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
        [frame_names[i]], # Match frame text exactly  tag:FRAME_SLIDER_NAMES
        {"frame": {"duration": 50, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 50}}
    ],
        "label": f't={i*dt+t0:{tfmt}}',
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)


fig_dict["layout"]["sliders"] = [sliders_dict]



fig = go.Figure(fig_dict)

# lol why were examples I read not built in this api
# instead of awkwardly documented giant dictionaries
fig.update_layout(
    # Move legend into graph
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=1.33
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

