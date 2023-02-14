import numpy as np
from numpy.random import Generator, PCG64
import plotly.graph_objects as go
import plotly.express as px
from collections import defaultdict
import copy


class Percolation():

    def __init__(self, Nx, Ny, p=0.593):

        self.Nx = Nx
        self.Ny = Ny
        self.Nsites = Nx*Ny
        self.p = p
        self.trials = 0
        self.cluster_iterations = 0
        self.rng = Generator(PCG64())
        self.compute_neighbor_sites()
        self.trial()

    def trial(self):
        """
        Generate random system and cluster sites
        """
        self.trials += 1
        self.compute_sites()
        self.compute_clusters()
        return self

    def compute_sites(self):
        """
        Fill sites
        """
        self.sites = self.rng.random((self.Nx, self.Ny)) < self.p
        self.sites.astype(np.int32)

    def compute_neighbor_sites(self):
        """
        Precompute sites of neighbors for the clustering loop
        """
        Nx = self.Nx
        Ny = self.Ny


        # neighbor_sites is dict of int -> (np.array(5,), np.array(5,))
        # Yes, to a tuple of two 1d arrays.
        # Outperforms numpy.zeros(shape = (Nx*Ny,2,5),dtype=np.int32).
        # The ambitious could try allocating numpy.zeros( Nx*Ny*2*5)
        # and make what might be slightly faster even less readable mess
        self.neighbor_sites = dict()

        idx_1d = -1  # Increment instead of computing i*Ny+j
        for i in range(Nx):
            for j in range(Ny):
                idx_1d += 1
                neighs = [
                    ((i-1) % Nx, j),  # Left
                    (i, j),           # Center
                    ((i+1) % Nx, j),  # Right
                    (i, (j-1) % Ny),  # Down
                    (i, (j+1) % Ny),  # Up
                    ]
                # Allows for a numpy slice if we transpose
                # into a Nx2 set of tuples. Hideous.
                neighs = tuple(np.array(neighs,dtype=np.uint32).T)
                self.neighbor_sites[idx_1d] = neighs


    def compute_clusters(self):

        Nx = self.Nx
        Ny = self.Ny
        Nsites = Nx * Ny
        # Empty sites set to Nx*Ny+1 (larger than any possible id)
        # Initialize sites with sequentially increasing cluster id
        empty_id = Nx*Ny+1
        clusters = np.ones((Nx, Ny), dtype=np.uint32) * empty_id
        c = 1
        for i in range(Nx):
            for j in range(Ny):
                if self.sites[i, j]:
                    clusters[i, j] = c
                    c += 1


        # Brute force clustering loop.
        # Merge to minimum of cluster of ids neighboring iteratively
        # Runtime is probably O(Nx*Ny)^2 * max_cluster_path_length
        # max cluster length in worst case (near percolation
        # threshold) can be significantly larger than max(Nx,Ny)
        # but probably is less than another factor of Nx*Ny.
        any_change = True

        while any_change:

            any_change = False

            self.cluster_iterations += 1

            idx_1d = -1 #1D index into neighbor list

            for i in range(Nx):
                for j in range(Ny):
                    idx_1d += 1
                    if clusters[i, j] == empty_id:
                        continue

                    min_cl_id = min(clusters[self.neighbor_sites[idx_1d]])
                    # Compute min over self site and 4 neighbors
                    #min_cl_id = min(clusters[self.neighbor_sites[idx_1d,0,:],
                    #                         self.neighbor_sites[idx_1d,1,:]])
                    if clusters[i, j] != min_cl_id:
                        any_change = True
                        clusters[i, j] = min_cl_id

        clusters[clusters == empty_id] = 0  # Set noncluster id to 0

        # Cluster sizes
        cluster_sizes = defaultdict(int)
        for i in range(Nx):
            for j in range(Ny):
                if clusters[i, j] != 0:
                    cluster_sizes[clusters[i, j]] += 1
        # Sort clusters largest to smallest
        sorted_cluster_sizes = sorted(
            cluster_sizes.items(),
            key=lambda x: x[1],
            reverse=True)

        # Store in class
        self.clusters = clusters
        self.cluster_sizes = cluster_sizes
        self.sorted_cluster_sizes = sorted_cluster_sizes
        self.max_cluster_size = sorted_cluster_sizes[0][1]

    def get_heatmap(self,
            logarithmic_cluster_size = False):
        """
        Get heatmap
        """


        # Heatmap needs to cluster by cluster size.
        self.heatmap = np.zeros((self.Nx, self.Ny),dtype=np.float32)
        for cl_id, cl_size in self.sorted_cluster_sizes:
            if logarithmic_cluster_size == True:
                self.heatmap[self.clusters == [cl_id]] = np.log(cl_size)
            else:
                self.heatmap[self.clusters == [cl_id]] = cl_size / self.Nsites

        self.heatmap[self.heatmap == 0] = np.NaN
        textarr = np.zeros((self.Nx,self.Ny),dtype=object)
        #self.cluster_sizes[0]=0
        for i in range(self.Nx):
            for j in range(self.Ny):
                if self.clusters[i,j] == 0:  #Unoccupied
                    msg=f"Site ({i}, {j}) is unoccupied"
                else:
                    round_digits = len(str(self.Nsites-1))  # ~correctish
                    # Apparently plotly eats '\n', so use html <br>
                    msg = f"Site ({i}, {j}) is occupied<br>"
                    if self.clusters[i,j] == self.sorted_cluster_sizes[0][0]:
                        msg += "Site is in largest cluster<br>"
                    msg += "Cluster size: "
                    msg += f"{self.cluster_sizes[self.clusters[i,j]]}<br>"
                    msg += f"Cluster size fraction: {self.heatmap[i,j]:.{round_digits}f}<br>"
                textarr[i,j]=msg

        # fig = px.imshow(self.clusters)
        p = go.Heatmap(
            z=self.heatmap,
            colorscale = 'sunsetdark',
            zmin = 0.0,
            zmax = 0.6,
            colorbar=dict(
                title='Cluster Size Fraction',
                titleside='right'
                ),
            hoverinfo = 'text',
            text= textarr
            )

        fig = go.Figure(p)
        fig.update_layout(dict(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            xaxis=dict(
                showgrid=False,
                showticklabels=False,
                ),
            yaxis=dict(
                showgrid=False,
                showticklabels=False,
                )

            ))
        return fig, p


    def write_heatmap(self,
            filename='perc.html',
            logarithmic_cluster_size=False):
        fig, _ = self.get_heatmap(logarithmic_cluster_size)
        fig.write_html(filename)

class AnimatedPlotly:

    _defaults=dict(
        animation_frame_duration=800,
        animation_transition='linear',
        animation_redraw=True,  # Default to false? shrug.
        # Set these to True if you want the html to open on its own
        # Set to false to reduce file sizes for webpage integration
        include_mathjax=False,  #'cdn' or False.
        include_plotlyjs=False,  #True, False, 'cdn'.
        )


    def __init__(self,

        filename,           # Name of output. I.e. "figure.html"
        plot_list,           # List of Plotly Figures
        slider_values,      # List of slider values (float, int)
        slider_label,       # Label for slider (string)
        ):
        """
        Convert list of plotly figure objects into an animation
        """

        # Load default parameters into self.params
        self.params = dict()
        self.params.update(**copy.deepcopy(self._defaults))
        self.filename=filename
        self.plot_list = plot_list
        self.slider_values = slider_values
        self.slider_label = slider_label

        if len(plot_list) < 2:
            raise ValueError("Must have at least 2 plots to animate")

        if not filename.endswith('.html'):
            filename = filename + '.html'


        self.fig_dict = dict(
            data=[],
            layout=go.Layout(),
            frames=[],
            )

        self.set_control_buttons()
        self.construct_animation_frames()
        self.configure_sliders()
        self.format_layout()

        self.fig = go.Figure(self.fig_dict)

    def set_control_buttons(self):

        #Add Play/Pause buttons

        self.fig_dict["layout"]["updatemenus"] = [
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
                            "duration": self.params['animation_frame_duration'],
                            "redraw": self.params['animation_redraw']
                            },
                        "fromcurrent": True,
                        "transition":
                            {
                            "duration": self.params['animation_frame_duration'],
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
                            "redraw": True
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

    def construct_animation_frames(self):

        self.fig_dict['data'] = plot_list[0]
        frames = []
        for frame_id, plot in enumerate(self.plot_list):
            data = [plot]  # list of one or more plots (equal length for
                          # all frames or error probably)
            name = f"frame_{frame_id}"
            frames.append(go.Frame(data=data, name=name))

        self.fig_dict['frames']=frames

    def configure_sliders(self):

        sliders_dict = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 14},
                "prefix": "Occupied Site Probability ",
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

        for frame_id in range(len(self.plot_list)):
            slider_step = {"args": [
                [f"frame_{frame_id}"], # Match frame text exactly  tag:FRAME_SLIDER_NAMES
                {"frame": {"duration": 50, "redraw": self.params['animation_redraw']},
                 "mode": "immediate",
                 "transition": {"duration": 50}}
            ],
                "label": f'{fig_values[frame_id]}%',
                "method": "animate"}
            sliders_dict["steps"].append(slider_step)


        self.fig_dict["layout"]["sliders"] = [sliders_dict]

    def format_layout(self):

        self.fig_dict['layout']['yaxis']['scaleanchor'] = 'x'
        self.fig_dict['layout']['xaxis']['gridcolor'] = 'rgba(0, 0, 0, 0)'
        self.fig_dict['layout']['yaxis']['gridcolor'] = 'rgba(0, 0, 0, 0)'
        self.fig_dict['layout']['yaxis']['color'] = 'rgba(0, 0, 0, 0)'
        self.fig_dict['layout']['xaxis']['color'] = 'rgba(0, 0, 0, 0)'
        self.fig_dict['layout']['plot_bgcolor'] = 'rgba(0,0,0,0)'
        self.fig_dict['layout']['height'] = 600


    def write_html(self):
        self.fig.write_html(
            self.filename,
            auto_play=False,
            # Make these are set to 'cdn', 'cdn' or 'cdn', 'True' if
            # you want freestanding html files to work.
            include_mathjax=self.params['include_mathjax'],
            include_plotlyjs=self.params['include_plotlyjs'],
            )


if __name__ == '__main__':

    plot_list = []
    fig_values = []
    for p in range(50,65):
        for i in range(1):
            L = 50
            perc = Percolation(L,L,p/100)
            print(f"p={p}%, lc size {perc.max_cluster_size}, lc fraction {perc.max_cluster_size / perc.Nsites}")
            #perc.write_heatmap(f"perc{p}.html", logarithmic_cluster_size=False)
            fig_values.append(p)
            _, plot = perc.get_heatmap()
            plot_list.append(plot)
    ap = AnimatedPlotly(f'animate_{perc.Nsites}.html', plot_list, fig_values, 'prob')
    ap.write_html()
