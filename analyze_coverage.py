import xml.etree.ElementTree as ET

def analyze_coverage():
    tree = ET.parse('coverage.xml')
    root = tree.getroot()
    
    print("Coverage Analysis:")
    print("=" * 50)
    
    # Get all classes and their coverage
    classes = []
    for cls in root.findall('.//class'):
        filename = cls.attrib["filename"]
        line_rate = float(cls.attrib["line-rate"])
        classes.append((filename, line_rate))
    
    # Sort by coverage (lowest first)
    classes.sort(key=lambda x: x[1])
    
    print("Files by coverage (lowest first):")
    for filename, line_rate in classes:
        print(f"  {filename}: {line_rate * 100:.1f}%")
    
    print("=" * 50)
    print("Files with coverage < 50%:")
    low_coverage = [c for c in classes if c[1] < 0.5]
    for filename, line_rate in low_coverage:
        print(f"  {filename}: {line_rate * 100:.1f}%")
    
    print("=" * 50)
    print("Files with coverage >= 50%:")
    high_coverage = [c for c in classes if c[1] >= 0.5]
    for filename, line_rate in high_coverage:
        print(f"  {filename}: {line_rate * 100:.1f}%")

if __name__ == "__main__":
    analyze_coverage()