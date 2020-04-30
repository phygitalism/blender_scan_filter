# Scan Filter
Blender 2.8+ add-on for filtering 3D scanned geometry from floor and artifacts.

![Automated steps](/images/Scan_Filter_steps.gif) 

Original Mesh
![Original Mesh](/images/00_mesh.jpg  "Original Mesh")

Filtered Result
![Filtered Result](/images/05_result.jpg  "Filtered Result")

**Installation:** Blender -> Edit -> Preferences -> Add-ons -> Install -> select scan_filter.py

**Appearance:** Properties Window -> Object Tab -> Scan Filter

![UI](/images/UI.jpg  "UI")


**Properties:**
- Floor Height Limit - The ratio of floor height to the total height of the bounding box.
- Floor Normal Limit - Permissible angular variation between floor polygons and XY plane.
- Artifacts - Percentage of polygons per disconnected islands to be deleted.
- Area of interest - Area from center on XY plane to preserve geometry.