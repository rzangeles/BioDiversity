// app.js

function buildSelect() {
    var url = '/names';

    Plotly.d3.json(url, function(error, response){
        if (error) {
            return console.warn(error);
        }

        var selector = document.getElementById("selDataset");

        for (i=0; i<response.length; i++) {
            var $option = document.createElement("option");
            $option.setAttribute("value", response[i]);
            $option.innerText = response[i];
            selector.appendChild($option)
        }
    });
    
};

function optionChanged(value) {
    var url = '/samples/' + value;
    var url4 = '/metadata/' + value;
    var url3 = '/samples_pie/' + value;
    
    console.log(url4);

    Plotly.d3.json(url3, function(error, response){
        if(error) {

            return console.warn(error);
        }

        var values = response[0]['sample_values'].slice(0,10);
        var labels = response[0]['otu_id'].slice(0,10);
        var $hover = response[0]['label'].slice(0,10);
           
        //log for the hover info
        // console.log($hover);

        var data = [{

            values: values,
            labels: labels,
            type: "pie",
            name: $hover,
            hoverinfo: 'all',
            hovertext: $hover
            
        }];

        var layout = {
            height:500,
            width: 800
        };

        Plotly.newPlot("plot", data, layout);
    });

    Plotly.d3.json(url, function(error, response){
        if(error) {
    
            return console.warn(error);
        }
                    
        var values2 = response[0]['sample_values'];
        var labels2 = response[0]['otu_id'];
        
        var $colors = []
        
        for (var i = 0; i<values2.length; i++) {
            $color_type = '#'+((1<<24)*(Math.random()+1)|0).toString(16).substr(1)
            $colors.push($color_type);
        }

        var $hover = response[0]['label'];

        var trace1 = {
    
            x: labels2,
            y: values2,
            mode: "markers",
            text: $hover,
            marker: {
                color: $colors,
                size: values2
            }
        };
    
        var data1 = [trace1]
    
        var layout1 = {
            title: "Bubble Chart Sample: " + values2,
            xlabel: "OTU ID",    
            height: 600,
            width:  600
        };
    
        Plotly.newPlot("plot2", data1, layout1);
            // Plotly.restyle("plot", data, 1);
    });
    
    // show the Metadata info

    Plotly.d3.json(url4, function(error, response){
        if(error) {

            return console.warn(error);
        }

        var age = response["AGE"];
        var bb_type = response["BBTYPE"];
        var ethnicity = response["ETHNICITY"];
        var gender = response["GENDER"];
        var location = response["LOCATION"];
        var sampleid = response["SAMPLEID"];

        console.log("MetaData: " + response);

        deleteRows();

        var meta_tbody = document.getElementById("meta_tr");
        var meta_td = document.createElement("td");
        meta_td.setAttribute("align", "left");
        var meta_p_age = document.createElement("p");
        meta_p_age.innerText = "AGE: " + age;
        var meta_br = document.createElement("br");
        var meta_p_bbtype = document.createElement("p");
        meta_p_bbtype.innerText = "BB TYPE: " + bb_type;
        var meta_br = document.createElement("br");

        var meta_p_ethnicity = document.createElement("p");
        meta_p_ethnicity.innerText = "ETHNICITY: " + ethnicity;
        var meta_br = document.createElement("br");
        var meta_p_gender = document.createElement("p");
        meta_p_gender.innerText = "BB TYPE: " + gender;
        var meta_br = document.createElement("br");
        var meta_p_location = document.createElement("p");
        meta_p_location.innerText = "BB TYPE: " + location;
        var meta_br = document.createElement("br");
        var meta_p_sampleid = document.createElement("p");
        meta_p_sampleid.innerText = "BB TYPE: " + sampleid;
        
        
        meta_td.appendChild(meta_p_age);
        meta_td.appendChild(meta_br);
        meta_td.appendChild(meta_p_bbtype);
        meta_td.appendChild(meta_br);
        meta_td.appendChild(meta_p_ethnicity);
        meta_td.appendChild(meta_br);
        meta_td.appendChild(meta_p_gender);
        meta_td.appendChild(meta_br);
        meta_td.appendChild(meta_p_location);
        meta_td.appendChild(meta_br);
        meta_td.appendChild(meta_p_sampleid);
        meta_td.appendChild(meta_br);
        
        
        meta_tbody.appendChild(meta_td);

    });


};

buildSelect();

function deleteRows() {

    var $tr = document.getElementsByTagName("td")[0];
    console.log($tr);

    if ($tr) {
    $tr.parentNode.removeChild($tr);
    }
    
    console.log("Deleting rows");
}

