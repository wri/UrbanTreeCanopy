# UrbanTreeCanopy

Rapid assessment methods for mapping green infrastructure in cities

Trees and other vegetation in urban areas provide a variety of benefits to people and ecosystems, notably water quality, flood management, heat mitigation, air quality, biodiversity and carbon sequestration.  The specific features of vegetation and their contexts influence the level of benefits that they can provide. Factors include the location (proximity to water, impermeable surfaces, pollution, other vegetation, etc.) and kinds of vegetation (height, species, etc.).  For air quality and heat mitigation, for example, variations in these factors can results in variation of benefits by two orders of magnitude. The factors that matter most vary across benefit area: strategies aimed at cooling, for example, would consider different aspects of vegetation and location than those aimed at managing stormwater or promoting biodiversity. Most of this information, however is missing for cities – particularly those in the global south who could most benefit from cost-effective nature-based solutions. 

WRI proposes to work in collaboration with Nat Geo to develop a globally-transferable, remote sensing-based method for rapid assessment of the spatial inventory of urban green infrastructure. The resulting methods would quantify and assess spatial distribution and relevant categorization of trees and other vegetation in urban areas at high-resolution.  Resulting in high-resolution maps of urban vegetation and tree cover, these analyses could inform goal setting, benchmarking and monitoring, program targeting and cost-benefit assessment. These findings could be deployed to encourage action by cities through initiatives like Cities4Forests or to systematize and expand finance for green infrastructure through development banks. 

Proposed outputs and methods

Produce binary raster maps of vegetated cover and trees (two datasets) for urban areas anywhere on Earth and whenever imagery is available
•	Working from high-resolution (~0.5-1.5m) RGBN imagery – NAIP (US, free), Airbus SPOT or Pleiades (global, commercial but available to NatGeo/WRI for analysis for at least 2019)
•	Lower resolution (10m) alternative for vegetated cover: Sentinel (but resolution too coarse for tree/street-level assessment or siting applications)
•	Output: Vegetated cover – Method: NDVI with threshold and seasonally adjusted
•	Output: Tree canopy – Method: machine learning model trained on RGBN-based NDVI and LIDAR-based height data, applicable for predictions to RGBN-only imagery

By end of 2019, we aim to have prototype methods producing reasonable results for both outputs using both NAIP and Airbus imagery inputs, and predictions for use in local engagements for at least 1 city in US and 1 city outside US, as selected by the WRI/NatGeo project teams. 
