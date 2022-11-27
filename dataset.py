import pandas as pd

####################################################################################################
###########################    ADD IMAGE COLUMN AND EXPORT TO NEW CSV    ###########################
####################################################################################################
''' As this dataset was provided with a link to the source website (Natural History Museum), I decided
to add images for each entry. I used BeautifulSoup to get the content and added it to a new
column. As this operation was very time consuming I ran it once, then exported and re-imported the updated dataset'''


def run_once_add_image_column():
    def get_image(webpage):
        response = requests.get(webpage)
        image_page = response.text
        dino_soup = BeautifulSoup(image_page, "html.parser")
        return dino_soup.find("img", {"class": "dinosaur--image"})["src"]
    import requests
    from bs4 import BeautifulSoup
    dino_no_images = pd.read_csv("./dino.csv")
    list_images = []
    for lnk in dino_no_images["link"]:
        try:
            list_images.append(get_image(str(lnk)))
        except TypeError:
            list_images.append("")
    dino_no_images["image"] = list_images
    dino_no_images.to_csv("./dino_updated.csv")
# run_once_add_image_column()

####################################################################################################
################################    IMPORT, CLEAN AND EDIT DATA    #################################
####################################################################################################


dino = pd.read_csv("./dino_updated.csv", index_col=0)
dino.dropna(subset=["image"], inplace=True)

''' LIVED_IN COLUMN - REMOVE NAN '''
dino.dropna(subset=["lived_in"], inplace=True)

''' CREATE "DISCOVERED" COLUMN FROM NAMED_BY '''
dino["discovered"] = dino["named_by"].str.extract(r"(\d{4})")  # use regex to match date from "named_by" string and add it to a new column
dino["discovered"] = pd.to_numeric(dino["discovered"], errors="coerce")  # Convert to numeric values and mark non convertable string as NaN
dino.dropna(subset=["discovered"], inplace=True)  # Remove NaN
dino["discovered"] = dino["discovered"].astype(int)  # Convert values to integer

''' TIDY UP NAMED_BY '''
dino["named_by"].replace((r"(\d{4})", "\\(", "\\)"), "", regex=True, inplace=True)  # Remove date and brackets
dino["named_by"] = dino["named_by"].str.strip()

''' CLEAN LENGTH & CONVERT TO INT'''
dino["length"].fillna(0.0, inplace=True)  # Replace NaN with 0.0
dino["length"].replace("m", "", regex=True, inplace=True)  # Remove 'm' for meters
dino["length"] = dino["length"].astype(float)  # Convert data to float

''' SPECIES COLUMN '''
dino.fillna({"species": dino["name"]}, inplace=True)  # If species NaN replace it with name

''' CHECK TYPES AND FIX ERRORS '''
dino.loc[dino["type"] == "1.0m", ["type"]] = "euornithopod"  # set the correct type

''' CREATE MAJOR_GROUPS COLUMN FROM TAXONOMY '''
major_groups_list = ["Herrerasauridae", "Guaibasauridae", "Plateosauridae", "Riojasauridae", "Massospondyildae", "Vulcanodontidae", "Turiasauria", "Cetiosauridae",
                     "Diplodocoidea", "Brachiosauridae", "Titanosauria", "Coelophysoidea", "Ceratosauria", "Megalosauroidea", "Carnosauria", "Megaraptora", "Tyrannosauroidea",
                     "Compsognathidae", "Ornithomimosauria", "Alvarezsauroidea", "Therizinosauria", "Oviraptorosauria", "Deinonychosauria", "Heterodontosauridae",
                     "Stegosauria", "Ankylosauria", "Pachycephalosauria", "Ceratopsia", "Ornithopoda", "Anchisauria", "Dromaeosauridae", "Spinosauroidea",
                     "Alvarezsauridae", "Eusauropoda", "Prosauropoda", "Therizinosauroidea", "Avialae", "Troodontidae"]

for m_g in major_groups_list:
    dino.loc[dino["taxonomy"].str.contains(m_g), "major_group"] = m_g
dino.fillna({"major_group": "Other"}, inplace=True)  # Create Other group from invalid entries

''' PERIOD COLUMN '''
dino["period"].replace(" million years ago", "", regex=True, inplace=True)  # remove unnecessary text

''' CREATE PERIOD_FROM and PERIOD_TO COLUMNS'''
periods = dino["period"].str.findall(r"(\d+)")  # Find all from - to ranges in periods column
p_f = []
p_t = []

for mlny in periods:  # Create lists for period_from and period_to and append values
    if len(mlny) > 1:
        p_f.append(int(mlny[0]))
        p_t.append(int(mlny[1]))
    elif len(mlny) == 1:
        p_f.append(int(mlny[0]))
        p_t.append(int(mlny[0]) + 10)
    else:
        p_f.append(pd.NA)
        p_t.append(pd.NA)

dino["period_from"] = p_f  # Create new tables from lists
dino["period_to"] = p_t

dino.dropna(subset=["period_from"], inplace=True)  # Clean columns and change data type to int
dino["period_from"] = dino["period_from"].astype(int)
dino.dropna(subset=["period_to"], inplace=True)
dino["period_to"] = dino["period_to"].astype(int)

''' REMOVE NUMBERS AND CLEAN THE PERIODS COLUMN (leve only text description)'''
dino["period"].replace((r"(\d+)", "-"), "", regex=True, inplace=True)
dino["period"] = dino["period"].str.strip()

''' FINALLY REORGANIZE THE DATASET COLUMNS '''
dino = dino[['name', 'species', 'type', 'length', 'diet', 'period', 'period_from', 'period_to', 'lived_in', 'discovered', 'major_group', 'taxonomy', 'named_by', 'link', 'image']]
