#!/usr/bin/env python3
"""
Website Downloader for Android - Download complete source code of any website
Usage: python website_downloader.py https://example.com
"""

import os
import sys
import re
import requests
import argparse
from urllib.parse import urlparse, urljoin
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import mimetypes

class WebsiteDownloader:
    def __init__(self, base_url, output_dir=None, max_depth=2, max_workers=5):
        self.base_url = base_url.rstrip('/')
        self.parsed_url = urlparse(self.base_url)
        self.domain = self.parsed_url.netloc
        
        if output_dir is None:
            clean_domain = re.sub(r'[^\w\-_]', '_', self.domain)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_dir = f"website_{clean_domain}_{timestamp}"
        else:
            self.output_dir = output_dir
            
        self.downloaded_urls = set()
        self.failed_urls = set()
        self.pending_urls = []
        self.max_depth = max_depth
        self.max_workers = max_workers
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
        })
        
        self.timeout = 15
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.allowed_extensions = {
            '.html', '.htm', '.css', '.js', '.json', '.xml',
            '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp',
            '.ico', '.ttf', '.woff', '.woff2', '.eot',
            '.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx'
        }
        
    def safe_filename(self, filename):
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        if len(filename) > 200:
            name, ext = os.path.splitext(filename)
            filename = name[:195] + ext
        return filename
        
    def save_file(self, content, filepath):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error saving file {filepath}: {str(e)}")
            return False
            
    def get_filepath_from_url(self, url):
        parsed = urlparse(url)
        path = parsed.path
        
        if not path or path.endswith('/'):
            path = path + 'index.html'
        elif '.' not in os.path.basename(path):
            path = path + '/index.html' if path.endswith('/') else path + '.html'
            
        path = path.split('?')[0].split('#')[0]
        
        path = path.lstrip('/')
        if not path:
            path = 'index.html'
            
        safe_path_parts = []
        for part in path.split('/'):
            safe_part = self.safe_filename(part)
            if safe_part:
                safe_path_parts.append(safe_part)
                
        safe_domain = self.safe_filename(self.domain)
        full_path = os.path.join(safe_domain, *safe_path_parts)
        
        if len(full_path) > 255:
            dirname = os.path.dirname(full_path)
            basename = os.path.basename(full_path)
            if len(dirname) > 200:
                full_path = basename
            else:
                full_path = os.path.join(dirname, basename[:255 - len(dirname) - 1])
                
        return os.path.join(self.output_dir, full_path)
        
    def extract_resources_regex(self, html_content, base_url):
        resources = set()
        
        patterns = {
            'links': r'<link[^>]+href=[\'"]([^\'"]+)[\'"]',
            'scripts': r'<script[^>]+src=[\'"]([^\'"]+)[\'"]',
            'images': r'<img[^>]+src=[\'"]([^\'"]+)[\'"]',
            'iframes': r'<iframe[^>]+src=[\'"]([^\'"]+)[\'"]',
            'anchors': r'<a[^>]+href=[\'"]([^\'"]+)[\'"]',
            'videos': r'<video[^>]+src=[\'"]([^\'"]+)[\'"]',
            'audios': r'<audio[^>]+src=[\'"]([^\'"]+)[\'"]',
            'sources': r'<source[^>]+src=[\'"]([^\'"]+)[\'"]',
            'embeds': r'<embed[^>]+src=[\'"]([^\'"]+)[\'"]',
        }
        
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                if match and not match.startswith(('data:', 'mailto:', 'tel:', 'javascript:', '#')):
                    absolute_url = urljoin(base_url, match)
                    parsed_absolute = urlparse(absolute_url)
                    if not parsed_absolute.netloc or parsed_absolute.netloc == self.domain:
                        ext = os.path.splitext(parsed_absolute.path)[1].lower()
                        if not ext or ext in self.allowed_extensions:
                            resources.add(absolute_url)
                            
        css_patterns = [
            r'@import\s+[\'"]([^\'"]+)[\'"]',
            r'url\([\'"]?([^\'"\)]+)[\'"]?\)',
        ]
        
        for pattern in css_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                if match and not match.startswith('data:'):
                    absolute_url = urljoin(base_url, match)
                    parsed_absolute = urlparse(absolute_url)
                    if not parsed_absolute.netloc or parsed_absolute.netloc == self.domain:
                        resources.add(absolute_url)
                        
        return list(resources)
        
    def should_download(self, url):
        parsed = urlparse(url)
        
        if parsed.netloc and parsed.netloc != self.domain:
            return False
            
        skip_extensions = {'.mp4', '.avi', '.mkv', '.mp3', '.zip', '.rar', '.7z'}
        ext = os.path.splitext(parsed.path)[1].lower()
        if ext in skip_extensions:
            return False
            
        skip_patterns = ['logout', 'login', 'admin', 'wp-admin', 'cart', 'checkout']
        for pattern in skip_patterns:
            if pattern in parsed.path.lower():
                return False
                
        return True
        
    def download_file(self, url, is_html=False):
        if url in self.downloaded_urls or url in self.failed_urls:
            return None
            
        if not self.should_download(url):
            return None
            
        try:
            print(f"Downloading: {url[:80]}...")
            
            if not url.startswith(('http://', 'https://')):
                url = urljoin(self.base_url, url)
                
            response = self.session.get(url, timeout=self.timeout, stream=True)
            response.raise_for_status()
            
            content_length = int(response.headers.get('content-length', 0))
            if content_length > 50 * 1024 * 1024:
                print(f"Skipping large file: {url}")
                self.failed_urls.add(url)
                return None
                
            content = response.content
            filepath = self.get_filepath_from_url(url)
            
            if self.save_file(content, filepath):
                self.downloaded_urls.add(url)
                print(f"✓ Saved: {os.path.basename(filepath)}")
                
                content_type = response.headers.get('Content-Type', '')
                if is_html or 'text/html' in content_type:
                    return content.decode('utf-8', errors='ignore')
                    
            return None
            
        except requests.exceptions.Timeout:
            print(f"⏱ Timeout: {url[:50]}...")
            self.failed_urls.add(url)
            return None
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed: {url[:50]}... - {str(e)[:30]}")
            self.failed_urls.add(url)
            return None
        except Exception as e:
            print(f"✗ Error: {url[:50]}... - {str(e)[:30]}")
            self.failed_urls.add(url)
            return None
            
    def download_website(self):
        print("=" * 50)
        print("Website Downloader for Android")
        print("=" * 50)
        print(f"URL: {self.base_url}")
        print(f"Output: {self.output_dir}")
        print(f"Max depth: {self.max_depth}")
        print(f"Max workers: {self.max_workers}")
        print("=" * 50)
        
        self.pending_urls = [(self.base_url, 0)]
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while self.pending_urls:
                batch = []
                new_pending = []
                
                for url, depth in self.pending_urls:
                    if (url not in self.downloaded_urls and 
                        url not in self.failed_urls and 
                        depth <= self.max_depth):
                        batch.append((url, depth))
                    else:
                        new_pending.append((url, depth))
                
                if not batch:
                    break
                    
                futures = {}
                for url, depth in batch:
                    is_html = (url == self.base_url or 
                              url.endswith(('.html', '.htm', '/')) or
                              '.php' in url or '.asp' in url)
                    futures[executor.submit(self.download_file, url, is_html)] = (url, depth)
                    
                for future in as_completed(futures):
                    url, depth = futures[future]
                    html_content = future.result()
                    
                    if html_content:
                        resources = self.extract_resources_regex(html_content, url)
                        
                        for resource in resources:
                            if (resource not in self.downloaded_urls and 
                                resource not in self.failed_urls):
                                resource_depth = depth + 1
                                new_pending.append((resource, resource_depth))
                                
                self.pending_urls = list(set(new_pending))
                
                print(f"\nProgress: {len(self.downloaded_urls)} downloaded, "
                      f"{len(self.failed_urls)} failed, "
                      f"{len(self.pending_urls)} pending\n")
                
                time.sleep(0.5)
                
        print("\n" + "=" * 50)
        print("DOWNLOAD COMPLETE!")
        print("=" * 50)
        print(f"Successfully downloaded: {len(self.downloaded_urls)} files")
        print(f"Failed downloads: {len(self.failed_urls)} files")
        print(f"Files saved in: {self.output_dir}")
        
        self.save_log()
        
    def save_log(self):
        log_file = os.path.join(self.output_dir, "download_log.txt")
        with open(log_file, 'w') as f:
            f.write(f"Website Download Log\n")
            f.write(f"URL: {self.base_url}\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Successfully downloaded: {len(self.downloaded_urls)} files\n\n")
            f.write("Downloaded files:\n")
            for url in sorted(self.downloaded_urls):
                f.write(f"{url}\n")
                
        print(f"Log saved to: {log_file}")
        
def check_android_storage():
    android_paths = [
        '/sdcard/',
        '/storage/emulated/0/',
        '/data/data/com.termux/files/home/'
    ]
    
    for path in android_paths:
        if os.path.exists(path):
            return path
    return os.getcwd()
    
def main():
    parser = argparse.ArgumentParser(description='Download complete source code of any website (Android optimized)')
    parser.add_argument('url', help='Website URL to download')
    parser.add_argument('-o', '--output', help='Output directory', default=None)
    parser.add_argument('-d', '--depth', type=int, default=2, 
                       help='Maximum depth for recursive downloads (default: 2 - lower for Android)')
    parser.add_argument('-w', '--workers', type=int, default=3, 
                       help='Number of concurrent downloads (default: 3 - lower for Android)')
    
    args = parser.parse_args()
    
    if not args.url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://")
        sys.exit(1)
        
    android_base = check_android_storage()
    print(f"Android storage detected at: {android_base}")
    
    try:
        downloader = WebsiteDownloader(
            args.url,
            output_dir=args.output,
            max_depth=args.depth,
            max_workers=args.workers
        )
        
        downloader.download_website()
        
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user")
        print(f"Partially downloaded files saved in: {downloader.output_dir}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)
        
if __name__ == "__main__":
    main()