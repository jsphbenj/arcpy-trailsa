# Created: 28 May 2023
# Joseph Benjamin
# Objective: Create a script tool that calculates the Trail-Slope Alignment
# for Segments in a Trail

import arcpy

arcpy.CheckOutExtension("3D")
arcpy.env.overwriteOutput = True

# Define Variables

split_type_checkbox = arcpy.GetParameterAsText(0)  # Output options: "No Split", "Split at Vertices" , "Split At Set Intervals"
interval = arcpy.GetParameterAsText(1)

trail_layer = arcpy.GetParameterAsText(2)
dem_rast = arcpy.GetParameterAsText(3)

split_trail_layer = arcpy.GetParameterAsText(4)
aspect_rast = arcpy.GetParameterAsText(5)

tsa_expression = "ifelse(!TrailAngle!,!Z_MEAN!)"
tsa_code = """
def ifelse(TrailAngle, Z_MEAN):
    OG_TSA = abs(TrailAngle - Z_MEAN)
    if OG_TSA > 270:
        return abs(OG_TSA - 360)
    elif OG_TSA > 90:
        return abs(OG_TSA - 180)
    else:
        return OG_TSA
"""

try:

    # Split Line
    if split_type_checkbox == "Split at Set Intervals":
        # Generate Points Along Lines
        point_feature = "point_layer"
        arcpy.management.GeneratePointsAlongLines(trail_layer, point_feature, "DISTANCE",
                                                  Distance = str(interval),
                                                  Include_End_Points = "END_POINTS")
        print(arcpy.AddMessage("Points created at intervals."))

        # Split Line Points
        arcpy.management.SplitLineAtPoint(trail_layer, point_feature, split_trail_layer, "0.5 Meters")
        arcpy.management.Delete(point_feature)

        print(arcpy.AddMessage("Trail Split at Interval."))
    elif split_type_checkbox == "Split at Vertices":
        arcpy.management.SplitLine(trail_layer, split_trail_layer)
        print(arcpy.AddMessage("Trail Split at Vertices."))
    else:
        print(arcpy.AddMessage("Trail NOT split."))

    # Aspect Raster
    arcpy.ddd.SurfaceParameters(dem_rast, aspect_rast, "ASPECT")
    print(arcpy.AddMessage("Surface Parameters Created: Aspect."))

    # Add Fields
    # Aspect
    arcpy.ddd.AddSurfaceInformation(split_trail_layer, aspect_rast, "Z_MEAN")
    print(arcpy.AddMessage("Aspect Added to Trail Attributes."))

    # Angle
    arcpy.management.AddFields(split_trail_layer, [["TrailAngle", "DOUBLE"],
                                                   ["TSA", "DOUBLE"]])
    arcpy.management.CalculateGeometryAttributes(split_trail_layer, [["TrailAngle", "LINE_BEARING"]])
    print(arcpy.AddMessage("Trail Angle Calculated."))

    # Calculate TSA
    arcpy.management.CalculateField(split_trail_layer, "TSA", tsa_expression, "PYTHON3", tsa_code)
    print(arcpy.AddMessage("TSA Calculated."))

    print(arcpy.AddMessage("Script successful."))

except:
    arcpy.AddError("Script Failed. TSA not calculated.")
    arcpy.AddMessage(arcpy.GetMessages())
