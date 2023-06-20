import xml.etree.ElementTree as ET
import pandas as pd

cols = ["label", "number_in_reference", "number_in_list", "expected", "plus_minus", "pValue", "fold_enrichment", "fdr", "mapped_id_list"]
rows = []

# Parsing the XML file
xmlparse = ET.parse('paper.xml')
root = xmlparse.getroot()
results = root.findall(".//result")
for result in results:
    label = result.find("term/label").text
    number_in_reference = result.find("number_in_reference").text
    number_in_list = result.find("input_list/number_in_list").text
    expected = result.find("input_list/expected").text
    plus_minus = result.find("input_list/plus_minus").text
    pValue = result.find("input_list/pValue").text
    fold_enrichment = result.find("input_list/fold_enrichment").text
    fdr = result.find("input_list/fdr").text
    mapped_ids = result.findall("input_list/mapped_id_list/mapped_id")
    mapped_id_list = ", ".join(mapped_id.text for mapped_id in mapped_ids)
  
    rows.append({"label": label,
                 "number_in_reference": number_in_reference,
                 "number_in_list": number_in_list,
                 "expected": expected,
                 "plus_minus": plus_minus,
                 "pValue": pValue,
                 "fold_enrichment": fold_enrichment,
                 "fdr": fdr,
                 "mapped_id_list": mapped_id_list})

df = pd.DataFrame(rows, columns=cols)

df.to_csv('paper_celdc.csv', index=False)
