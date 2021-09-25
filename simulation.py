import math
import time
import random
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


GRAPH_CONFIG = {"n": 100,
                "l": 1,
                "d": 2,
                "times": 100,
                "animate": True,
                "style": "markers",
                "speed": 2.00,
                "color": "#215A21",
                "pi_color": "#0900A4",
                "bg_color": "#FFFFFF",
                "marker_size": 7.00}


def estimate_pi(runs, needles, d_width, n_length):
    if graph_submitted:
        if "pi" not in st.session_state:
            st.warning("Please run the simulation before applying the changes.")
        else:
            return st.session_state["pi"]
    else:
        latest_iteration = st.empty()
        bar = st.progress(0)
        pi_values = []
        sim_start = time.time()
        for i in range(runs):
            n_hits = 0

            for _ in range(needles):
                x = random.uniform(0, d_width/2)
                theta = random.uniform(0, math.pi/2)

                x_cross = x - (n_length/2)*math.cos(theta)
                if x_cross < 0:
                    n_hits += 1

            if n_hits == 0:
                pi_estimation = 0
                pi_values.append(pi_estimation)
            else:
                pi_estimation = needles/n_hits
                pi_values.append(pi_estimation)
            st.session_state["sim_time"] = time.time() - sim_start
            latest_iteration.text(f'Replication {i+1}')
            p = ((i/runs)+(1/runs))*100
            bar.progress(int(p))
        return pi_values


def draw_static(val):
    fig = go.Figure(go.Scatter(x=np.arange(1, GRAPH_CONFIG["times"]+1),
                               y=val,
                               mode=GRAPH_CONFIG["style"],
                               marker=dict(
        color=GRAPH_CONFIG["color"],
        size=GRAPH_CONFIG["marker_size"]))
    )

    fig.update_layout(title="Buffon's Needle Simulation",
                      title_x=0.5,
                      xaxis_title='Replication',
                      yaxis_title='Pi Estimation',
                      width=800, height=600,
                      margin=dict(l=20, r=20, t=30, b=20),
                      yaxis_range=(math.pi-2, math.pi+2),
                      xaxis_range=(-10, GRAPH_CONFIG["times"]+10),
                      plot_bgcolor=GRAPH_CONFIG["bg_color"])
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    return fig


def draw_animated(val):
    fig = go.Figure(go.Scatter(y=val[:0],
                               mode=GRAPH_CONFIG["style"],
                               name="Testing Points",
                               marker=dict(
        color=GRAPH_CONFIG["color"],
        size=GRAPH_CONFIG["marker_size"]))
    )

    fig.update_layout(title="Buffon's Needle Simulation",
                      title_x=0.5,
                      xaxis_title='Replication',
                      yaxis_title='Pi Estimation',
                      width=800, height=600,
                      margin=dict(l=20, r=20, t=30, b=20),
                      yaxis_range=(math.pi-2, math.pi+2),
                      xaxis_range=(-10, GRAPH_CONFIG["times"]+10),
                      plot_bgcolor=GRAPH_CONFIG["bg_color"],

                      updatemenus=[dict(buttons=[dict(
                          args=[None, {"frame": {"duration": GRAPH_CONFIG["speed"],
                                                 "redraw": False},
                                        "fromcurrent": True,
                                        "transition": {"duration": 0}}],
                          label="Run",
                          method="animate")],
                          type='buttons',
                          showactive=False,
                          y=1,
                          x=1.11,
                          xanchor='right',
                          yanchor='top')])

    frames = [go.Frame(data=[go.Scatter(x=np.arange(1, GRAPH_CONFIG["times"]+1), y=val[:i+1])])
              for i in range(1, GRAPH_CONFIG["times"])]

    fig.update(frames=frames)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=False, zeroline=False)
    return fig


def convert_df(dict):
    df = pd.DataFrame.from_dict(dict)
    return df.to_csv().encode('utf-8')


st.title("Buffon's Needle Experiment")

st.markdown("""
 * Use the sidebar to set the plot parameters.
 * Your plot will appear below.
 * Be careful when using a large number of replication or number of needles parameters
   since the script stores the result in session storage to allow you easily change graph
   configures without having to rerun the simulation.  If you use large numbers in the number
   of replication or the number of needles parameters, your browser or computer may slow down
   or crash during the simulation. All responsibility belongs to the user.
 * Make sure you press the apply button after the graph configuration changed,
   and press the run button after the simulation parameters changed.
""")

with st.expander("See Details"):
    placeholder = st.empty()
    placeholder.markdown("""
    >**Suppose we have a surface that has been divided with equally spaced parallel
    >lines and we drop a needle onto the surface. What is the probability or the
    >chance of a needle lies in a position where it crosses one of the lines of the surface?**
    """)
    st.image("https://miro.medium.com/max/875/1*s9RQ4hFDJJrhNG6Y6Zer1Q.png",
             caption='The needle crosses the upper parallel line', width=600)

with st.sidebar.form("params"):
    st.markdown("## Select parameters")
    GRAPH_CONFIG["n"] = st.number_input(
        "Number of Needles", format="%i", min_value=1, value=GRAPH_CONFIG["n"], max_value=10000)
    GRAPH_CONFIG["l"] = st.number_input(
        "Needle Length", min_value=1, value=GRAPH_CONFIG["l"])
    GRAPH_CONFIG["d"] = st.number_input(
        "Distance Between Parallel Lines", min_value=1, value=GRAPH_CONFIG["d"])
    GRAPH_CONFIG["times"] = st.number_input(
        "Number of Replications", format="%i", min_value=1, value=GRAPH_CONFIG["times"], max_value=1000)

    params_submitted = st.form_submit_button("Run")

with st.sidebar.form("graph"):
    with st.expander("Graph Configuration"):

        choice = st.selectbox("Graph Style", ("Static", "Animated"))
        if choice == "Static":
            GRAPH_CONFIG["animate"] = False
        else:
            GRAPH_CONFIG["animate"] = True

        GRAPH_CONFIG["style"] = st.selectbox("Style", ("markers", "lines"))

        if GRAPH_CONFIG["animate"]:
            GRAPH_CONFIG["speed"] = st.number_input(
                "Animation Duration", min_value=0.00, value=GRAPH_CONFIG["speed"])

        col1, col2, col3 = st.columns(3)
        with col1:
            GRAPH_CONFIG["bg_color"] = st.color_picker(
                'Background Color', value=GRAPH_CONFIG["bg_color"])
        with col2:
            GRAPH_CONFIG["pi_color"] = st.color_picker(
                'Pi Color', value=GRAPH_CONFIG["pi_color"])
        with col3:
            GRAPH_CONFIG["color"] = st.color_picker(
                'Marker Color', value=GRAPH_CONFIG["color"])

        if GRAPH_CONFIG["style"] == "markers":
            GRAPH_CONFIG["marker_size"] = st.number_input(
                "Marker Size", min_value=1.00, value=GRAPH_CONFIG["marker_size"])
        show = st.checkbox('Show Pi line', value=True)

    graph_submitted = st.form_submit_button("Apply")

if params_submitted or graph_submitted:
    est = estimate_pi(GRAPH_CONFIG["times"],
                      GRAPH_CONFIG["n"],
                      GRAPH_CONFIG["d"],
                      GRAPH_CONFIG["l"],
                      )
    if not est == None:
        st.session_state["pi"] = est
    if "pi" in st.session_state and st.session_state["pi"] != None:
        if GRAPH_CONFIG["animate"]:
            fig = draw_animated(st.session_state["pi"])
        else:
            fig = draw_static(st.session_state["pi"])
        if show:
            fig.add_hline(math.pi, line_color=GRAPH_CONFIG["pi_color"])

        col4, col5, col6 = st.columns(3)
        with col4:
            avg = np.average(st.session_state["pi"])
            avg_r = np.round(avg, 5)
            st.metric("Average Estimation", avg_r)
            error = np.abs(math.pi-avg_r)
            error_r = np.round(error, 5)
            st.metric("Error", error_r)
        with col5:
            st.metric("Number of Replications", GRAPH_CONFIG["times"])
            st.metric("Number of Needles", GRAPH_CONFIG["n"])
        with col6:
            st.metric("Simulation Time", str(
                st.session_state["sim_time"])[:6] + " sec")
            st.download_button(
                label='Download CSV', data=convert_df(st.session_state["pi"]),
                file_name='file.csv', mime='text/csv'
            )
        st.plotly_chart(fig)