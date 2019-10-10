# UrbanTreeCanopy

'~'*WIP*'~'


### Project Objective

Rapid assessment methods for mapping green infrastructure in cities

Trees and other vegetation in urban areas provide a variety of benefits to people and ecosystems, notably water quality, flood management, heat mitigation, air quality, biodiversity and carbon sequestration.  The specific features of vegetation and their contexts influence the level of benefits that they can provide. Factors include the location (proximity to water, impermeable surfaces, pollution, other vegetation, etc.) and kinds of vegetation (height, species, etc.).   

WRI proposes to work in collaboration with Nat Geo to develop a globally-transferable, remote sensing-based method for rapid assessment of the spatial inventory of urban green infrastructure. The resulting methods would quantify and assess spatial distribution and relevant categorization of trees and other vegetation in urban areas at high-resolution.  Resulting in high-resolution maps of urban vegetation and tree cover, these analyses could inform goal setting, benchmarking and monitoring, program targeting and cost-benefit assessment. These findings could be deployed to encourage action by cities through initiatives like Cities4Forests or to systematize and expand finance for green infrastructure through development banks. 

By end of 2019, we aim to have prototype methods producing reasonable results for both outputs using both NAIP and Airbus imagery inputs, and predictions for use in local engagements for at least 1 city in US and 1 city outside US, as selected by the WRI/NatGeo project teams.

### Proposed outputs and methods

- Produce binary raster maps of vegetated cover and trees (two datasets) for urban areas anywhere on Earth and whenever imagery is available
- Working from high-resolution (~0.5-1.5m) RGBN imagery – NAIP (US, free), Airbus SPOT or Pleiades (global, commercial but available to NatGeo/WRI for analysis for at least 2019)
- Lower resolution (10m) alternative for vegetated cover: Sentinel (but resolution too coarse for tree/street-level assessment or siting applications)
- Output: Vegetated cover – Method: NDVI with threshold and seasonally adjusted
- Output: Tree canopy – Method: machine learning model trained on RGBN-based NDVI and LIDAR-based height data, applicable for predictions to RGBN-only imagery

### Methodology

- Acquisition of high resolution satellite imagery - NAIP, SPOT, Pleiades. (*UTC_Core-1*)
- Acquisition of LiDAR point cloud data and conversion to digital surface model tif. (*UTC_Core-1*)
- Creation of NDVI and elevation masks from the imagery and DSM, respectively. The intersection of these masks produces a 'composite mask' which is used as training inputs for the Convolutional Neural Network. The composite masks can be produced as binary, classified, or semi-continuous. (*UTC_Core-2*)
- 



