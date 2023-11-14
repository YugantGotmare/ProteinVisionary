import streamlit as st
from stmol import showmol
import py3Dmol
import requests
import biotite.structure.io as bsio

# Set page title and favicon
st.set_page_config(page_title='Protein Predictor', layout='wide')

# Sidebar
st.sidebar.title('Project Description')
st.sidebar.write('## Protein Structure Predictor powered by ESMFold')
st.sidebar.write('Welcome to the Protein Structure Predictor! This tool utilizes the ESMFold model to predict the 3D structure of a protein based on its amino acid sequence.')

st.sidebar.write('### How to Use')
st.sidebar.write('1. Enter a protein sequence in the text area on the main page.')
st.sidebar.write('2. Click the "Predict" button to initiate the structure prediction.')
st.sidebar.write('3. Visualize the predicted protein structure and download the PDB file.')

st.sidebar.write('### About ESMFold')
st.sidebar.write('[ESMFold](https://esmatlas.com/about) is an end-to-end single-sequence protein structure predictor based on the ESM-2 language model. For more information, read the [research article](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2) and the [news article](https://www.nature.com/articles/d41586-022-03539-1) published in *Nature*.')

st.sidebar.write('### Acknowledgments')
st.sidebar.write('This project uses the [Py3Dmol](https://pypi.org/project/py3dmol/) library for visualizing molecular structures.')

# Main content
st.title('Protein Structure Predictor')
# st.write('Welcome to the Protein Structure Predictor! Enter a protein sequence and click "Predict" to visualize its structure.')

# Protein sequence input
DEFAULT_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
txt = st.text_area('Input protein sequence', DEFAULT_SEQ, height=100)
st.write('')  # Add an empty line for spacing

# Predict button
if st.button('Predict'):
    st.subheader('Predicting...')
    with st.spinner('Please wait...'):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=txt, verify=False)
        pdb_string = response.content.decode('utf-8')

        with open('predicted.pdb', 'w') as f:
            f.write(pdb_string)

        struct = bsio.load_structure('predicted.pdb', extra_fields=["b_factor"])
        b_value = round(struct.b_factor.mean(), 4)

        # Display protein structure
        st.subheader('Visualization of Predicted Protein Structure')
        pdbview = py3Dmol.view(width=800, height=500)
        pdbview.addModel(pdb_string, 'pdb')
        pdbview.setStyle({'cartoon': {'color': 'spectrum'}})
        pdbview.setBackgroundColor('white')
        pdbview.zoomTo()
        pdbview.zoom(2, 800)
        pdbview.spin(True)
        showmol(pdbview, height=500, width=800)

        # Display plDDT value
        st.subheader('plDDT')
        st.write('plDDT is a per-residue estimate of the confidence in prediction on a scale from 0-100.')
        st.info(f'plDDT: {b_value}')

        # Download PDB button
        st.download_button(label="Download PDB", data=pdb_string, file_name='predicted.pdb', mime='text/plain')
