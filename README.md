# arcpy-tsa
calculate Trail Slope Alignment, a script tool made with arcpy

CONTENTS:  
- TSAScript.atbx - Toolbox with the ArcGIS script tool ready-to-use with any polyline  
- TSA_Calc.py - The python script used to generate the script tool  

EXPLANATION:  

Degradation Potential:  
www.usgs.gov/media/images/trailslope-alignment-tsa-fall-2022  
- Very High: 0° - 22° (Fall Aligned)  
- High: 23° - 45° (Fall Aligned)  
- Low: 46° - 68° (Side Hill)  
- Very Low: 69° - 90° (Side Hill)  

The two extreme TSA types that a trail can fall under are a 90-degree side-hill trail and a 0-degree fall-aligned trail. A side-hill trail follows the landscape’s contour lines, while a fall-aligned trail follows the slope of the landscape perpendicular to contour lines. Side-hill trails allow for easier water drainage. Because the trail follows the contours of the landscape, it is more difficult to walk outside the established tread. This decreases trail widening, which protects natural resources.
