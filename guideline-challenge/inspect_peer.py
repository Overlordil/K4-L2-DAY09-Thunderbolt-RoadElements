import zipfile, xml.etree.ElementTree as ET  
z = zipfile.ZipFile('project/07_blind_handoff/peer_output/bdd_drivable_blind.zip')  
root = ET.fromstring(z.read('annotations.xml'))  
for image in root.findall('./image'):  
   name = image.attrib['name']; pts = []  
   for polygon in image.findall('polygon'):  
      if polygon.attrib.get('label') == 'drivable_area':  
         xs=[]; ys=[];  
         for p in polygon.attrib['points'].split(';'):  
            x,y = map(float,p.split(',')); xs.append(x); ys.append(y)  
         pts.append((min(xs), min(ys), max(xs), max(ys)))  
   print(name, pts)  
