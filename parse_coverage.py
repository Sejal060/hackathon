import xml.etree.ElementTree as ET

def parse_coverage():
    tree = ET.parse('coverage.xml')
    root = tree.getroot()
    line_rate = float(root.attrib["line-rate"])
    print(f"Overall Coverage: {line_rate * 100:.1f}%")
    
    # Get package-level coverage
    for package in root.findall(".//package"):
        package_name = package.attrib["name"]
        package_rate = float(package.attrib["line-rate"])
        print(f"  {package_name}: {package_rate * 100:.1f}%")

if __name__ == "__main__":
    parse_coverage()