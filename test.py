from view.map import *

data = load_json()
data = filter_metropolitan_regions(data)
# fig = create_metropolitan_map(data)
fig = create_region_map(data, "75")
show_map(fig)