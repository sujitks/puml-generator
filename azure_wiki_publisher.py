#!/usr/bin/env python3
"""
Azure DevOps Wiki Publisher
Publishes generated markdown documentation to Azure DevOps wiki
"""

import os
import sys
import base64
import requests
from pathlib import Path
import argparse
import json


class AzureDevOpsWikiPublisher:
    """Publishes documentation to Azure DevOps wiki"""
    
    def __init__(self, organization, project, wiki_id, pat_token):
        self.organization = organization
        self.project = project
        self.wiki_id = wiki_id
        self.pat_token = pat_token
        
        # Setup authentication
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self._get_auth_header()}'
        }
        
        self.base_url = f'https://dev.azure.com/{organization}/{project}/_apis/wiki/wikis/{wiki_id}'
    
    def _get_auth_header(self):
        """Create basic auth header from PAT token"""
        credentials = f':{self.pat_token}'
        encoded = base64.b64encode(credentials.encode()).decode()
        return encoded
    
    def create_or_update_page(self, path, content, comment="Updated by PlantUML Generator"):
        """Create or update a wiki page"""
        api_version = '7.0'
        url = f'{self.base_url}/pages?path={path}&api-version={api_version}'
        
        # Try to get existing page to get eTag
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                # Update existing page
                etag = response.headers.get('ETag')
                update_headers = self.headers.copy()
                update_headers['If-Match'] = etag
                
                data = {
                    'content': content
                }
                
                response = requests.put(url, headers=update_headers, json=data)
                
                if response.status_code in [200, 201]:
                    print(f"Updated page: {path}")
                    return True
                else:
                    print(f"Error updating page {path}: {response.status_code} - {response.text}")
                    return False
            else:
                # Create new page
                data = {
                    'content': content
                }
                
                response = requests.put(url, headers=self.headers, json=data)
                
                if response.status_code in [200, 201]:
                    print(f"Created page: {path}")
                    return True
                else:
                    print(f"Error creating page {path}: {response.status_code} - {response.text}")
                    return False
        
        except Exception as e:
            print(f"Exception publishing page {path}: {e}")
            return False
    
    def upload_attachment(self, file_path, page_path):
        """Upload an attachment (diagram) to the wiki"""
        api_version = '7.0'
        
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            file_name = Path(file_path).name
            url = f'{self.base_url}/attachments?name={file_name}&api-version={api_version}'
            
            headers = {
                'Content-Type': 'application/octet-stream',
                'Authorization': self.headers['Authorization']
            }
            
            response = requests.put(url, headers=headers, data=file_content)
            
            if response.status_code in [200, 201]:
                print(f"Uploaded attachment: {file_name}")
                return response.json().get('url')
            else:
                print(f"Error uploading attachment {file_name}: {response.status_code} - {response.text}")
                return None
        
        except Exception as e:
            print(f"Exception uploading attachment {file_path}: {e}")
            return None
    
    def publish_documentation(self, docs_dir, wiki_base_path='/PlantUML'):
        """Publish all documentation to wiki"""
        docs_path = Path(docs_dir)
        
        if not docs_path.exists():
            print(f"Documentation directory does not exist: {docs_dir}")
            return False
        
        # Find all markdown files
        md_files = list(docs_path.rglob('*.md'))
        png_files = list(docs_path.rglob('*.png'))
        
        print(f"Found {len(md_files)} markdown files and {len(png_files)} diagrams")
        
        # Upload diagrams first
        uploaded_diagrams = {}
        for png_file in png_files:
            rel_path = png_file.relative_to(docs_path)
            wiki_path = f"{wiki_base_path}/{rel_path.parent}/{png_file.name}"
            url = self.upload_attachment(png_file, wiki_path)
            if url:
                uploaded_diagrams[str(rel_path)] = url
        
        # Publish markdown files
        for md_file in md_files:
            rel_path = md_file.relative_to(docs_path)
            wiki_path = f"{wiki_base_path}/{rel_path.parent}/{md_file.stem}"
            
            # Read and adjust content for wiki
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update image references if we have uploaded versions
            for local_path, wiki_url in uploaded_diagrams.items():
                content = content.replace(f"]({Path(local_path).name})", f"]({wiki_url})")
            
            self.create_or_update_page(wiki_path, content)
        
        print(f"\nPublished to Azure DevOps wiki at: {wiki_base_path}")
        return True


def main():
    parser = argparse.ArgumentParser(description='Publish documentation to Azure DevOps wiki')
    parser.add_argument('docs_dir', help='Directory containing generated documentation')
    parser.add_argument('--organization', required=True, help='Azure DevOps organization')
    parser.add_argument('--project', required=True, help='Azure DevOps project')
    parser.add_argument('--wiki-id', required=True, help='Wiki identifier')
    parser.add_argument('--wiki-path', default='/PlantUML', help='Base path in wiki')
    parser.add_argument('--pat-token', help='Personal Access Token (or use AZURE_DEVOPS_PAT env var)')
    
    args = parser.parse_args()
    
    pat_token = args.pat_token or os.environ.get('AZURE_DEVOPS_PAT')
    if not pat_token:
        print("Error: PAT token required (use --pat-token or AZURE_DEVOPS_PAT env var)")
        sys.exit(1)
    
    publisher = AzureDevOpsWikiPublisher(
        args.organization,
        args.project,
        args.wiki_id,
        pat_token
    )
    
    success = publisher.publish_documentation(args.docs_dir, args.wiki_path)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
