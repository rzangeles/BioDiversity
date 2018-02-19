# Import dependencies
from flask import Flask, render_template, jsonify, request, redirect
import pandas as pd



#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Routes
#################################################


# Main route
@app.route('/')
def home():
    return render_template('index.html')


# List of Sample Names

@app.route('/names')
def names():
   file3 = pd.read_csv("belly_button_biodiversity_samples.csv")
   sample_names = list(file3)
   del sample_names[0]

   return jsonify(sample_names)

# List of OTU descriptions
@app.route('/otu')
def otu():
    file2 = pd.read_csv("belly_button_biodiversity_otu_id.csv")
    descriptions = file2.rename(columns={"lowest_taxonomic_unit_found":"Description"})

    descriptions_unique = set(descriptions["Description"])
    descriptions_unique = list(descriptions_unique)

    return jsonify(descriptions_unique)

# MetaData for a given sample

@app.route('/metadata/<sample>')
def metadata(sample):

    file1 = pd.read_csv("Belly_Button_Biodiversity_Metadata.csv")
    
    new_file = file1.to_dict('records')

    newlist=[]
    for i in new_file:
        s={}
        for k in i.keys():
            s[k] = str(i[k])
        newlist.append(s)

    new_sample = sample.replace(" ", "").upper()

    for item in newlist:
        search_item = "BB_" + str(item['SAMPLEID'])

        if (search_item == new_sample):


            return jsonify(item)
    
    error_msg = {"error": f"Sample with name {sample} not found."}
    return jsonify(error_msg), 404

# MetaData for a given sample (for Meta Data section)
# Convert dictionary to a list

@app.route('/metadata_list/<sample>')
def metadata_list(sample):

    file1 = pd.read_csv("Belly_Button_Biodiversity_Metadata.csv")
    
    new_file = file1.to_dict('records')
    new_file_list = list(new_file)
    
          
    return jsonify(new_file_list)
    
# Weekly Washing Frequency Sample

@app.route('/wfreq/<sample>')
def freq(sample):
    
    file1 = pd.read_csv("Belly_Button_Biodiversity_Metadata.csv")
    
    new_file = file1.to_dict('records')
    new_sample = sample.replace(" ", "").upper()

    for item in new_file:
        search_item = "BB_" + str(item['SAMPLEID'])

        if (search_item == new_sample):

            return jsonify(int(item["WFREQ"]))
    
    error_msg = {"error": f"Sample with name {sample} not found."}
    return jsonify(error_msg), 404


    
    # error_msg = {"error": f"Sample with name {sample} not found."}
    # return jsonify(error_msg), 404

# OTU IDs and Sample Values for a given sample

@app.route('/samples/<sample>')
def samples(sample):

    file3 = pd.read_csv("belly_button_biodiversity_samples.csv")
    # file2 = pd.read_csv("belly_button_biodiversity_otu_id.csv")
           
    updated_list = file3[["otu_id", sample]]
    updated_list = updated_list.rename(columns={sample: "sample_values"})
    sorted_list = updated_list.sort_values("sample_values", ascending=False).astype(str)

    # sorted_merge_list = sorted_list.merge(file2, how="outer", on="otu_id")

    # sorted_merge_list["sample_values"] = sorted_merge_list["sample_values"].astype(str)
    # sorted_merge_list["otu_id"] = sorted_merge_list["otu_id"].astype(str)

    final_dict = {}
    final_list = []

    final_dict["sample_values"] = list(sorted_list["sample_values"])
    final_dict["otu_id"] = list(sorted_list["otu_id"])
    
    
    final_list.append(final_dict)

    return jsonify(final_list)

# OTU IDs and Sample Values for a given sample

@app.route('/samples_pie/<sample>')
def samples_pie(sample):

    file3 = pd.read_csv("belly_button_biodiversity_samples.csv")
    file2 = pd.read_csv("belly_button_biodiversity_otu_id.csv")
           
    updated_list = file3[["otu_id", sample]]
    updated_list = updated_list.rename(columns={sample: "sample_values"})
    sorted_list = updated_list.sort_values("sample_values", ascending=False)

    sorted_merge_list = sorted_list.merge(file2, how="outer", on="otu_id")

    sorted_merge_list["sample_values"] = sorted_merge_list["sample_values"].astype(str)
    sorted_merge_list["otu_id"] = sorted_merge_list["otu_id"].astype(str)

    final_dict = {}
    final_list = []

    final_dict["sample_values"] = list(sorted_merge_list["sample_values"])
    final_dict["otu_id"] = list(sorted_merge_list["otu_id"])
    final_dict["label"] = list(sorted_merge_list["lowest_taxonomic_unit_found"])

    final_list.append(final_dict)

    return jsonify(final_list)

if __name__ == "__main__":
    app.run(debug=True)
