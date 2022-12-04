import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dataset import dino
import dfprint

# LIVE VERSION OF THIS PROJECT CAN BE FOUND @ https://ilillill-dinosaurs-main-91zl3w.streamlit.app/

non_0_size_dinos = dino[dino["length"] != 0]  # There are 0 values in the 'length' column, when calculating sizes I will use this DataFrame instead of the main one

st.set_page_config(layout="wide", page_title="Dinosaurs", page_icon="🦖")

bg_image = '<style> .stApp {background-image: url("https://raw.githubusercontent.com/Ilillill/projects/main/dinologo_match_light.png");background-position: 95% 10%; background-repeat: no-repeat; background-size: 100px 100px;} </style>'
st.markdown(bg_image, unsafe_allow_html=True)

images = False
if st.checkbox("Include images"):
    images = True

with st.sidebar:
    st.title("DINOSAURS!")
    dino_selector = st.selectbox("Select species or start typing to search:", dino["name"].unique(), index=3)  # Image of the first dino is just a placeholder, so I set the index to a different entry
    selected_dino = dino.loc[dino["name"] == dino_selector]
    if st.button("Pick randomly"):
        selected_dino = dino.sample(n=1)
    if images:
        selected_dino_image = selected_dino["image"].iloc[0]
        st.image(selected_dino_image)
    st.write(f"Name: {selected_dino['name'].iloc[0].capitalize()} {selected_dino['species'].iloc[0].capitalize()}")
    st.write(f"Type: {selected_dino['diet'].iloc[0].capitalize()} {selected_dino['type'].iloc[0].capitalize()}")
    st.write(f"Size: {selected_dino['length'].iloc[0]}m")
    st.write(f"Period: {selected_dino['period'].iloc[0].capitalize()} ({selected_dino['period_from'].iloc[0]} - {selected_dino['period_to'].iloc[0]} mln years ago)")
    st.write(f"Discovered: {selected_dino['lived_in'].iloc[0]}, {selected_dino['discovered'].iloc[0]}")
    st.markdown(selected_dino["link"].iloc[0])
    st.subheader("Size comparison:")
    fig_size_comparison = px.timeline(selected_dino, x_start=selected_dino["length"]-selected_dino["length"], x_end=selected_dino["length"], height=175)
    fig_size_comparison.update_layout(yaxis={'visible': False}, xaxis={"type": "linear"})
    fig_size_comparison.data[0].x = selected_dino["length"].tolist()
    fig_size_comparison.add_shape(type="line", x0=0, y0=0, x1=1.8, y1=0, line=dict(color="red", width=8,))
    st.plotly_chart(fig_size_comparison, use_container_width=True)
    st.text("Average human height (red)")
    st.text(f"{selected_dino['name'].iloc[0].capitalize()} length (blue)")

dino_time = dino['period_from'].max() - dino['period_to'].min()
with st.container():
    lbl1, lbl2, lbl3, lbl4, lbl5 = st.columns(5)
    with lbl1:
        st.markdown(f"<h1 style='text-align: center;'>{len(dino)}</h1><h6 style='text-align: center;'>Species</h6>", unsafe_allow_html=True)
    with lbl2:
        st.markdown(f"<h1 style='text-align: center;'>{dino_time}</h1><h6 style='text-align: center;'>Mln years range</h6>", unsafe_allow_html=True)
    with lbl3:
        st.markdown(f"<h1 style='text-align: center;'>{dino.nunique()['major_group']}</h1><h6 style='text-align: center;'>Groups</h6>", unsafe_allow_html=True)

st.markdown("---")

st.markdown(f"<h1 style='text-align: center;'>Timeline</h1>", unsafe_allow_html=True)

st.write(f"Non-avian dinosaurs existed for **{dino_time} million** years.")

oldest_fossil = dino["period_from"].max()
oldest_fossil_df = dino[dino["period_from"] == oldest_fossil]  # dino.iloc[dino["period_from"].idxmax()] returns only one entry
st.write(f"The oldest fossils are **{oldest_fossil} mln** years old:")
st.write(oldest_fossil_df[['name', 'species', 'type', 'major_group', 'length', 'diet', 'period', 'period_from', 'period_to', 'lived_in', 'discovered', 'named_by']])

species_kp = dino[dino["period_to"] < 67]
st.write(f"**{len(species_kp['name'])}** of known species were present during the K-P Extinction Event:")
st.write(species_kp[['name', 'species', 'type', 'major_group', 'length', 'diet', 'period', 'period_from', 'period_to', 'lived_in', 'discovered', 'named_by']])

st.subheader("All dinosaurs timeline & sizes")
fig_all = px.scatter(non_0_size_dinos, x=non_0_size_dinos["period_to"], y=non_0_size_dinos["length"], size=non_0_size_dinos["length"], color="name", labels={"name": "Species", "period_to": "Mln years ago", "length": "Size"})
fig_all.update_xaxes(autorange="reversed")
st.plotly_chart(fig_all, use_container_width=True)

st.markdown("---")

st.markdown(f"<h1 style='text-align: center;'>Major groups</h1>", unsafe_allow_html=True)

with st.container():
    gr_col1, gr_col2 = st.columns([4, 1])
    with gr_col1:
        fig_gr = px.sunburst(dino, path=["type", "major_group"], template="presentation")
        if st.checkbox("Show species in groups"):
            fig_gr = px.sunburst(dino, path=["type", "major_group", "name"], template="presentation")

        st.plotly_chart(fig_gr, use_container_width=True)
    with gr_col2:
        groups = dino["major_group"].value_counts().reset_index()
        groups = groups.rename(columns={"index": "Group", "major_group": "Species"})
        groups.set_index("Group", inplace=True)
        st.write(groups)

st.subheader("Major groups timeline")
major_group_ranges = dino.groupby("major_group").agg({"period_to": "min", "period_from": "max"}).reset_index()
major_group_ranges["delta"] = major_group_ranges["period_to"] - major_group_ranges["period_from"]
fig_timeline = px.timeline(major_group_ranges, x_start="period_from", x_end="period_to", y="major_group", text="major_group", labels={"major_group": "Major group", "period_from": "From (mln years ago)", "period_to": "To (mln years ago)"})
fig_timeline.update_layout(xaxis_title="MLN years ago", yaxis={'visible': False}, xaxis={"type": "linear"})
fig_timeline.update_xaxes(autorange="reversed")
fig_timeline.data[0].x = major_group_ranges.delta.tolist()
st.plotly_chart(fig_timeline, use_container_width=True)

st.header("Select group")
group_selector = st.selectbox("Select group or start typing to search:", dino["major_group"].unique())
selected_group = dino[dino["major_group"] == group_selector]

st.write(f"{group_selector}: {len(dino[dino['major_group'] == group_selector])} species")

selected_for_sizes = non_0_size_dinos[non_0_size_dinos["major_group"] == group_selector].reset_index(drop=True)
st.subheader("Sizes in group")
if st.checkbox(f"Largest: {np.round(selected_for_sizes['length'].max(), 1)}m {selected_for_sizes.iloc[selected_for_sizes['length'].idxmax()]['name'].capitalize()}"):
    st.text(selected_for_sizes.iloc[selected_for_sizes['length'].idxmax()][['name', 'species', 'type', 'length', 'diet', 'period', 'period_from', 'period_to', 'lived_in', 'discovered']].to_string())
if st.checkbox(f"Smallest: {np.round(selected_for_sizes['length'].min(), 1)}m {selected_for_sizes.iloc[selected_for_sizes['length'].idxmin()]['name'].capitalize()}"):
    st.text(selected_for_sizes.iloc[selected_for_sizes['length'].idxmin()][['name', 'species', 'type', 'length', 'diet', 'period', 'period_from', 'period_to', 'lived_in', 'discovered']].to_string())
st.write(f"Average: {np.round(selected_for_sizes['length'].mean(), 1)}m")

st.subheader("Group distribution")
group_diversity = selected_group.groupby("lived_in").count().reset_index()
group_diversity["species"] = group_diversity["species"].astype(str)
color_setting = group_diversity["lived_in"]
if st.checkbox("Show number of species"):
    color_setting = group_diversity["species"]
fig_gr_loc = px.choropleth(group_diversity, locations=group_diversity["lived_in"], color=color_setting, locationmode="country names", labels={"lived_in": "Location", "species": f"Species of {group_selector} discovered"})
st.plotly_chart(fig_gr_loc, use_container_width=True)

if st.checkbox("Show species in this group"):
    st.write(selected_group[['name', 'species', 'type', 'major_group', 'length', 'diet', 'period', 'period_from', 'period_to', 'lived_in', 'discovered', 'named_by']])
    if images:
        st.subheader("Images")
        chunks = [selected_group["image"].iloc[x:x+5] for x in range(0, len(selected_group), 5)]
        for chunk in chunks:
            i = 0
            with st.container():
                im_col1, im_col2, im_col3, im_col4, im_col5 = st.columns(5)
                col = [im_col1, im_col2, im_col3, im_col4, im_col5]
                for ch in chunk:
                    with col[i]:
                        st.image(ch, width=150)
                        st.write(dino["name"].loc[dino["image"] == ch].iloc[0].capitalize())
                        i += 1

st.markdown("---")


def scatter_location(selection, title):
    return px.scatter_geo(selection, locations="lived_in", locationmode="country names", color="lived_in", size="species", text="species", size_max=50, labels={"lived_in": "Location", "species": "Species discovered"}, title=title)


def heatmap_location(selection, title):
    return px.choropleth(selection, locations="lived_in", locationmode="country names", color="name", labels={"lived_in": "Location", "name": "Species discovered"}, title=title)


st.markdown(f"<h1 style='text-align: center;'>Species diversity</h1>", unsafe_allow_html=True)

st.write(f"Dinosaurs were discovered in {dino['lived_in'].nunique()} countries: {', '.join(dino['lived_in'].unique())}")

dino_locations = dino.groupby("lived_in").count().reset_index()
dino_triassic = dino[dino["period"].str.contains('Triassic')]
dino_locations_triassic = dino_triassic.groupby("lived_in").count().reset_index()
dino_jurassic = dino[dino["period"].str.contains('Jurassic')]
dino_locations_jurassic = dino_jurassic.groupby("lived_in").count().reset_index()
dino_cretaceous = dino[dino["period"].str.contains('Cretaceous')]
dino_locations_cretaceous = dino_cretaceous.groupby("lived_in").count().reset_index()

if st.checkbox("Show heatmap"):
    with st.container():
        c1_col1, c1_col2 = st.columns(2)
        with c1_col1:
            st.plotly_chart(heatmap_location(dino_locations, "Entire Mesozoic"), use_container_width=True)
        with c1_col2:
            st.plotly_chart(heatmap_location(dino_locations_triassic, "Triassic"), use_container_width=True)
    with st.container():
        c2_col1, c2_col2 = st.columns(2)
        with c2_col1:
            st.plotly_chart(heatmap_location(dino_locations_jurassic, "Jurassic"), use_container_width=True)
        with c2_col2:
            st.plotly_chart(heatmap_location(dino_locations_cretaceous, "Cretaceous"), use_container_width=True)
else:
    with st.container():
        c1_col1, c1_col2 = st.columns(2)
        with c1_col1:
            st.plotly_chart(scatter_location(dino_locations, "Entire Mesozoic"), use_container_width=True)
        with c1_col2:
            st.plotly_chart(scatter_location(dino_locations_triassic, "Triassic"), use_container_width=True)
    with st.container():
        c2_col1, c2_col2 = st.columns(2)
        with c2_col1:
            st.plotly_chart(scatter_location(dino_locations_jurassic, "Jurassic"), use_container_width=True)
        with c2_col2:
            st.plotly_chart(scatter_location(dino_locations_cretaceous, "Cretaceous"), use_container_width=True)

st.markdown("---")

st.markdown(f"<h1 style='text-align: center;'>Size</h1>", unsafe_allow_html=True)

average_dinosaur = non_0_size_dinos["length"].mean()
st.write(f"AVERAGE DINOSAUR: {np.round(average_dinosaur, 1)}m")

largest_dinosaur = non_0_size_dinos["length"].max()
largest_dinosaur_df = dino[dino["length"] == largest_dinosaur]
st.write(f"LARGEST DINOSAUR: {largest_dinosaur}m")
st.write(largest_dinosaur_df[['name', 'species', 'type', 'major_group', 'length', 'diet', 'period', 'period_from', 'period_to', 'lived_in', 'discovered', 'named_by']])

smallest_dinosaur = non_0_size_dinos["length"].min()
smallest_dinosaur_df = dino[dino["length"] == smallest_dinosaur]
st.write(f"SMALLEST DINOSAUR: {smallest_dinosaur}m")
st.write(smallest_dinosaur_df[['name', 'species', 'type', 'major_group', 'length', 'diet', 'period', 'period_from', 'period_to', 'lived_in', 'discovered', 'named_by']])

theropods = dino[dino["taxonomy"].str.contains("Theropoda")]
largest_theropod = theropods["length"].max()
largest_theropod_df = theropods[theropods["length"] == largest_theropod]
st.write(f"LARGEST THEROPOD {largest_theropod}m (was it the T-Rex??)")
st.write(largest_theropod_df[['name', 'species', 'type', 'major_group', 'length', 'diet', 'period', 'period_from', 'period_to', 'lived_in', 'discovered', 'named_by']])

dromaeosaurs = dino[dino["taxonomy"].str.contains("Paraves")]
largest_dromaeosaur = dromaeosaurs["length"].max()
largest_dromaeosaur_df = dromaeosaurs[dromaeosaurs["length"] == largest_dromaeosaur]
st.write(f"LARGEST DROMAEOSAUR {largest_dromaeosaur}m:")
st.write(largest_dromaeosaur_df[['name', 'species', 'type', 'major_group', 'length', 'diet', 'period', 'period_from', 'period_to', 'lived_in', 'discovered', 'named_by']])

st.subheader("Filter species by size")
size_slider = st.slider(label="Size in meters", min_value=0, max_value=int(largest_dinosaur), value=10, step=1)
dino_by_size = non_0_size_dinos[non_0_size_dinos["length"].between(size_slider, size_slider+0.99)]
if dino_by_size.empty:
    st.write(f"There are no know {size_slider}m long dinosaurs")
else:
    st.write(f"{size_slider} m - {size_slider+1} m: {len(dino_by_size)} species found")
    st.write(dino_by_size[['name', 'species', 'type', 'major_group', 'length', 'diet', 'period', 'period_from', 'period_to', 'lived_in', 'discovered', 'named_by']])

st.subheader("Sizes in each major group")
families_grouped = non_0_size_dinos.groupby("major_group")
largest_in_family = families_grouped["length"].max().reset_index()
average_in_family = families_grouped["length"].mean().reset_index()
smallest_in_family = families_grouped["length"].min().reset_index()
bar_largest = go.Bar(x=largest_in_family["major_group"], y=np.round(largest_in_family["length"], 2), name="Largest in group")
bar_average = go.Bar(x=average_in_family["major_group"], y=np.round(average_in_family["length"], 2), name="Average size in group")
bar_smallest = go.Bar(x=smallest_in_family["major_group"], y=np.round(smallest_in_family["length"], 2), name="Smallest in group")
fig_sizes = go.Figure()
fig_sizes.add_traces(bar_largest)
fig_sizes.add_traces(bar_average)
fig_sizes.add_traces(bar_smallest)
st.plotly_chart(fig_sizes, use_container_width=True)

st.subheader("Timeline of average sauropod sizes")
sauropods = non_0_size_dinos[non_0_size_dinos["taxonomy"].str.contains('Sauropodomorpha')].groupby("period_to")
fig_sauropods = px.line(sauropods, x=sauropods["period_to"].max(), y=sauropods["length"].mean(), labels={'x': 'Mln years ago', "y": "Average sauropod size"}, line_shape="spline")
fig_sauropods.update_layout(showlegend=False)
fig_sauropods.update_xaxes(autorange="reversed")
st.plotly_chart(fig_sauropods, use_container_width=True)
st.write("I was trying to find out if we would still have large sauropods if the extinction never happened. The chart doesn't indicate their sizes were really dropping towards the end of Cretaceous, but rather that their sizes were fluctuating every xx mln years.")

st.subheader("How T-rex's size compared to other large carnivores?")
theropods = non_0_size_dinos[non_0_size_dinos["type"] == "large theropod"].sort_values("length")
fig_trex = px.bar(theropods[-10:], x="name", y="length")
fig_trex["data"][0]["marker"]["color"] = ["red" if fig_data == "tyrannosaurus" else "#636efa" for fig_data in fig_trex["data"][0]["x"]]  # print(fig_trex) # print(fig_trex["data"][0]["marker"]["color"])  #636efa
st.plotly_chart(fig_trex, use_container_width=True)

st.markdown("---")

st.markdown(f"<h1 style='text-align: center;'>Discoveries</h1>", unsafe_allow_html=True)

st.write("Top 10 people with most discoveries")
discoverers = dino["named_by"].value_counts().reset_index()
discoverers = discoverers.rename(columns={"index": "Name", "named_by": "Species discovered"})
discoverers.set_index("Name", inplace=True)
st.write(discoverers[:10].transpose())

st.subheader("Number of species by fossil age")
dino_diversity = dino["period_to"].value_counts().reset_index()
dino_diversity = dino_diversity.rename(columns={"index": "Fossils age", "period_to": "Number of species"})
fig_diversity = px.scatter(dino_diversity, x="Fossils age", y="Number of species", text="Number of species", size="Number of species", size_max=50, color="Number of species")
fig_diversity.update_xaxes(autorange="reversed")
fig_diversity.update_layout(xaxis_title="MLN years ago", yaxis_title="Number of species", showlegend=False)
st.plotly_chart(fig_diversity, use_container_width=True)

st.subheader("Number of discoveries by year")
dino_discoveries = dino["discovered"].value_counts().reset_index()
dino_discoveries = dino_discoveries.rename(columns={"index": "Year", "discovered": "Species"})
fig_discoveries = px.bar(dino_discoveries, x="Year", y="Species", color="Species")
fig_discoveries.update_layout(xaxis_title="Year", yaxis_title="Number of discoveries")
st.plotly_chart(fig_discoveries, use_container_width=True)

st.markdown("---")

st.markdown(f"<h1 style='text-align: center;'>About the dataset</h1>", unsafe_allow_html=True)

with st.expander("DISPLAY DATA", expanded=False):
    st.dataframe(dino)

with st.expander("INFO", expanded=False):
    st.write('DATASET SOURCE: https://github.com/kjanjua26/jurassic-park | https://www.kaggle.com/datasets/kjanjua/jurassic-park-the-exhaustive-dinosaur-dataset')
    with st.container():
        df_col1, df_col2 = st.columns(2)
        with df_col1:
            st.header("Original dataset:")
            st.text(dfprint.dataset_before)
        with df_col2:
            st.header("Edited dataset:")
            st.text(dfprint.dataset_after)

    st.header("Dataset describe:")
    st.text(dfprint.dataset_describe)

with st.container():
    dwn1, dwn2, dwn3 = st.columns([1, 1, 2])
    with dwn1:
        st.download_button(
            "Download dataset as CSV",
            data=dino.to_csv().encode("utf-8"),
            file_name="dino_df.csv",
            mime="text/csv",
        )
    with dwn2:
        st.download_button(
            "Download dataset as HTML",
            data=dino.to_html().encode("utf-8"),
            file_name="dino_df.html",
            mime="text/html",
        )

# This isn't a very scientific chart, I just wanted to see if plotly can animate this. Looks cool! :)
# Unfortunately it will not work on Codio with the installed version of Pandas (1.1.5) (works on my PC and online). Version 1.4.0 is required and I don't know if I am allowed to update modules myself.
# AttributeError: 'DataFrameGroupBy' object has no attribute 'value_counts'
# Pandas reference: pandas.core.groupby.DataFrameGroupBy.value_counts - New in version 1.4.0.

# st.markdown('---')
# st.subheader("Lifeline of non-avian dinosaurs")
# dino_lifeline = dino[["period_to"]].groupby("period_to").value_counts()
# dino_lifeline = dino_lifeline.reindex(range(250), fill_value=0).reset_index()  # fill gaps between existing millions of years and fill them with species count of 0
# dino_lifeline = dino_lifeline.rename(columns={"period_to": "years", 0: "species"})
# dino_lifeline = dino_lifeline.sort_values("years", ascending=False).reset_index(drop=True)  # reset index so the oldest year is first
# lifeline_fig = px.scatter(dino_lifeline, x="years", y="species", animation_frame="years", range_x=[250, 0], range_y=[-4, 27], color_discrete_sequence=["red"], labels={"years": "Mln years ago", "species": "Number of species present"})
# lifeline_fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 40
# lifeline_fig.add_vline(x=64, line_width=2, line_color="red", line_dash="dash", annotation_text="K-Pg Extinction Event")
# st.plotly_chart(lifeline_fig, use_container_width=True)
