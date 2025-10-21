#!/usr/bin/env python3
"""
PlantUML Processor
Processes PlantUML files, generates diagrams, creates markdown documentation
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
import shutil


class PlantUMLProcessor:
    """Processes PlantUML files and generates documentation"""
    
    def __init__(self, input_dir, output_dir, plantuml_jar=None):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.plantuml_jar = plantuml_jar or os.environ.get('PLANTUML_JAR', '/opt/plantuml.jar')
        
        if not self.input_dir.exists():
            raise ValueError(f"Input directory does not exist: {self.input_dir}")
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def find_puml_files(self):
        """Find all PlantUML files recursively"""
        puml_files = []
        for ext in ['*.puml', '*.plantuml', '*.pu']:
            puml_files.extend(self.input_dir.rglob(ext))
        return sorted(puml_files)
    
    def generate_diagram(self, puml_file):
        """Generate diagram from PlantUML file"""
        try:
            # Get relative path from input directory
            rel_path = puml_file.relative_to(self.input_dir)
            output_subdir = self.output_dir / rel_path.parent
            output_subdir.mkdir(parents=True, exist_ok=True)
            
            # Generate PNG diagram
            cmd = [
                'java', '-jar', self.plantuml_jar,
                '-tpng',
                '-o', str(output_subdir),
                str(puml_file)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"Error generating diagram for {puml_file}: {result.stderr}")
                return None
            
            # Return path to generated PNG
            png_file = output_subdir / (puml_file.stem + '.png')
            return png_file
        
        except Exception as e:
            print(f"Exception generating diagram for {puml_file}: {e}")
            return None
    
    def create_markdown(self, puml_file, diagram_path):
        """Create markdown file with embedded diagram"""
        try:
            rel_path = puml_file.relative_to(self.input_dir)
            md_path = self.output_dir / rel_path.parent / (puml_file.stem + '.md')
            
            # Read PlantUML content
            with open(puml_file, 'r', encoding='utf-8') as f:
                puml_content = f.read()
            
            # Get relative path from markdown to diagram
            diagram_rel = diagram_path.name if diagram_path else 'diagram.png'
            
            # Create markdown content
            md_content = f"""# {puml_file.stem}

## Diagram

![{puml_file.stem}]({diagram_rel})

## PlantUML Source

```plantuml
{puml_content}
```

**Source file:** `{rel_path}`
"""
            
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            return md_path
        
        except Exception as e:
            print(f"Exception creating markdown for {puml_file}: {e}")
            return None
    
    def process_all(self):
        """Process all PlantUML files"""
        puml_files = self.find_puml_files()
        
        if not puml_files:
            print(f"No PlantUML files found in {self.input_dir}")
            return []
        
        print(f"Found {len(puml_files)} PlantUML file(s)")
        
        results = []
        for puml_file in puml_files:
            print(f"Processing: {puml_file}")
            
            # Generate diagram
            diagram_path = self.generate_diagram(puml_file)
            
            # Create markdown
            md_path = self.create_markdown(puml_file, diagram_path)
            
            results.append({
                'puml': puml_file,
                'diagram': diagram_path,
                'markdown': md_path
            })
        
        # Create index
        self.create_index(results)
        
        return results
    
    def create_index(self, results):
        """Create an index markdown file listing all diagrams"""
        index_path = self.output_dir / 'index.md'
        
        content = "# PlantUML Documentation Index\n\n"
        content += f"Total diagrams: {len(results)}\n\n"
        
        # Group by directory
        by_dir = {}
        for result in results:
            puml_file = result['puml']
            rel_path = puml_file.relative_to(self.input_dir)
            dir_name = str(rel_path.parent) if rel_path.parent != Path('.') else 'root'
            
            if dir_name not in by_dir:
                by_dir[dir_name] = []
            by_dir[dir_name].append(result)
        
        for dir_name, items in sorted(by_dir.items()):
            content += f"\n## {dir_name}\n\n"
            for item in items:
                puml_file = item['puml']
                md_path = item['markdown']
                rel_path = puml_file.relative_to(self.input_dir)
                
                if md_path:
                    md_rel = md_path.relative_to(self.output_dir)
                    content += f"- [{puml_file.stem}]({md_rel})\n"
                else:
                    content += f"- {puml_file.stem} (error)\n"
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Created index at: {index_path}")


def main():
    parser = argparse.ArgumentParser(description='Process PlantUML files and generate documentation')
    parser.add_argument('input_dir', help='Input directory containing PlantUML files')
    parser.add_argument('-o', '--output', default='/output', help='Output directory for generated files')
    parser.add_argument('-j', '--jar', help='Path to PlantUML jar file')
    
    args = parser.parse_args()
    
    processor = PlantUMLProcessor(args.input_dir, args.output, args.jar)
    results = processor.process_all()
    
    print(f"\nProcessed {len(results)} file(s)")
    print(f"Output directory: {processor.output_dir}")


if __name__ == '__main__':
    main()
