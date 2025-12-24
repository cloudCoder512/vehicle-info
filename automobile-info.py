import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue
import requests
import brotli
import zlib
import json
import time
from datetime import datetime

# ==========================================
# Enhanced GUI Implementation with Professional Styling
# ==========================================

class ProfessionalVehicleInfoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Information Dashboard")
        self.root.geometry("1200x750")
        
        # Professional color scheme
        self.colors = {
            'sidebar': '#2c3e50',
            'header': '#3498db',
            'main_bg': '#ecf0f1',
            'card_bg': '#ffffff',
            'primary': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'error': '#e74c3c',
            'text_dark': '#2c3e50',
            'text_light': '#7f8c8d'
        }
        
        self.root.configure(bg=self.colors['main_bg'])
        
        # Queue for thread-safe GUI updates
        self.queue = queue.Queue()
        
        # Setup modern UI
        self.setup_modern_ui()
        self.check_queue()
        
        # Initialize API settings
        self.base_url = "https://www.acko.com"
        self.headers = {
            "Host": "www.acko.com",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "accept": "application/json",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "upgrade-insecure-requests": "1",
            "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "cookie": "trackerid=179aa6e9-ca2f-4298-adfb-7a2079f45239; acko_visit=i184eQX5pfoDbAwrkofEuA; _ga=GA1.1.1738483623.1745154975; FPID=FPID2.2.BNactSqBEJYZy0GtFayP4nbw276RJEZO4ZGxgDvWd%2FQ%3D.1745154975; FPAU=1.2.348938027.1745154976; _gtmeec=e30%3D; _fbp=fb.1.1745154976133.1568369174; user_id=eFLS7co3phjxpwDoNIkrPw:1745155002698:e7fdef44ea0065aa6372165a62d91e0b7d8f1440; _ga_W47KBK64MF=GS1.1.1745154975.1.1.1745155051.0.0.203712065; __cf_bm=nkXwQrar2uE2AYsZ3SErkSYFMOZhGstBL4KGaawfcBk-1745234838-1.0.1.1-qCl9aKP2EGODZq8VThqc3uOeYjpF0fvFX53rZj3FShkGG1UVJOC5wassxGuhHNJnhgq.eaEa7mvPNx9_TetCE9i5ef9tlHgtVXRWFTrqLKs",
        }
    
    def setup_modern_ui(self):
        """Setup professional dashboard layout with sidebar"""
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['header'], height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🚗 Vehicle Information Dashboard",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors['header'],
            fg='white'
        ).pack(side=tk.LEFT, padx=20, pady=10)
        
        # Status indicator in header
        self.status_indicator = tk.Label(
            header_frame,
            text="● Ready",
            font=("Segoe UI", 10),
            bg=self.colors['header'],
            fg=self.colors['success']
        )
        self.status_indicator.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['main_bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left sidebar
        sidebar = tk.Frame(main_container, bg=self.colors['sidebar'], width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Sidebar title
        tk.Label(
            sidebar,
            text="Vehicle Tools",
            font=("Segoe UI", 16, "bold"),
            bg=self.colors['sidebar'],
            fg='white',
            pady=20
        ).pack()
        
        # Input card in sidebar
        input_card = tk.Frame(sidebar, bg=self.colors['card_bg'], padx=15, pady=15)
        input_card.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            input_card,
            text="Vehicle Registration Number:",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark']
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.vehicle_entry = tk.Entry(
            input_card,
            font=("Segoe UI", 12),
            bd=2,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=self.colors['primary']
        )
        self.vehicle_entry.pack(fill=tk.X, pady=(0, 10))
        self.vehicle_entry.bind('<Return>', lambda e: self.fetch_all_data())
        
        # Fetch buttons in sidebar
        btn_style = {'font': ("Segoe UI", 10), 'padx': 20, 'pady': 8, 'bd': 0, 'cursor': 'hand2'}
        
        self.fetch_all_btn = tk.Button(
            input_card,
            text="🔍 Fetch All Information",
            command=self.fetch_all_data,
            bg=self.colors['primary'],
            fg='white',
            **btn_style
        )
        self.fetch_all_btn.pack(fill=tk.X, pady=5)
        
        # Quick action buttons
        actions_frame = tk.Frame(sidebar, bg=self.colors['sidebar'], pady=20)
        actions_frame.pack(fill=tk.X, padx=10)
        
        tk.Label(
            actions_frame,
            text="Quick Actions:",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['sidebar'],
            fg='white'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Individual action buttons
        self.vehicle_btn = tk.Button(
            actions_frame,
            text="📋 Vehicle Details",
            command=lambda: self.fetch_specific_data("vehicle"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark'],
            **{**btn_style, 'padx': 15}
        )
        self.vehicle_btn.pack(fill=tk.X, pady=2)
        
        self.puc_btn = tk.Button(
            actions_frame,
            text="🌿 Pollution Details",
            command=lambda: self.fetch_specific_data("puc"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark'],
            **{**btn_style, 'padx': 15}
        )
        self.puc_btn.pack(fill=tk.X, pady=2)
        
        self.challan_btn = tk.Button(
            actions_frame,
            text="🚨 Challan Details",
            command=lambda: self.fetch_specific_data("challan"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark'],
            **{**btn_style, 'padx': 15}
        )
        self.challan_btn.pack(fill=tk.X, pady=2)
        
        # Clear button
        self.clear_btn = tk.Button(
            actions_frame,
            text="🗑️ Clear Output",
            command=self.clear_output,
            bg=self.colors['warning'],
            fg='white',
            **btn_style
        )
        self.clear_btn.pack(fill=tk.X, pady=10)
        
        # Right content area
        content_area = tk.Frame(main_container, bg=self.colors['main_bg'])
        content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Output header
        output_header = tk.Frame(content_area, bg=self.colors['card_bg'])
        output_header.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            output_header,
            text="API Response Output",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['card_bg'],
            fg=self.colors['text_dark']
        ).pack(side=tk.LEFT, padx=15, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            output_header,
            mode='indeterminate',
            length=150
        )
        self.progress.pack(side=tk.RIGHT, padx=15)
        
        # Output text area with modern styling
        output_frame = tk.Frame(content_area, bg=self.colors['card_bg'], relief=tk.FLAT)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(output_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Modern text widget
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=25,
            font=("Consolas", 10),
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            bg='#f8f9fa',
            fg=self.colors['text_dark'],
            insertbackground=self.colors['primary'],
            borderwidth=0,
            highlightthickness=1,
            highlightcolor='#ddd'
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        scrollbar.config(command=self.output_text.yview)
        
        # Configure text tags for better formatting
        self.output_text.tag_config("header", 
                                   foreground=self.colors['primary'],
                                   font=("Consolas", 11, "bold"))
        self.output_text.tag_config("success", 
                                   foreground=self.colors['success'])
        self.output_text.tag_config("error", 
                                   foreground=self.colors['error'])
        self.output_text.tag_config("warning", 
                                   foreground=self.colors['warning'])
        self.output_text.tag_config("info", 
                                   foreground=self.colors['text_light'])
        self.output_text.tag_config("json_key", 
                                   foreground='#8e44ad',
                                   font=("Consolas", 10, "bold"))
        
        # Footer
        footer = tk.Frame(self.root, bg=self.colors['text_dark'], height=40)
        footer.pack(fill=tk.X)
        footer.pack_propagate(False)
        
        tk.Label(
            footer,
            text="Data sourced from Acko APIs • Professional Dashboard v2.0",
            font=("Segoe UI", 9),
            bg=self.colors['text_dark'],
            fg='#95a5a6'
        ).pack(pady=10)
    
    def update_status(self, message, status_type="info"):
        """Update status indicator with color coding"""
        colors = {
            "info": self.colors['text_light'],
            "success": self.colors['success'],
            "warning": self.colors['warning'],
            "error": self.colors['error']
        }
        color = colors.get(status_type, self.colors['text_light'])
        self.status_indicator.config(text=f"● {message}", fg=color)
    
    def print_to_gui(self, text, tag=None):
        """Print text to GUI output area (thread-safe)"""
        self.queue.put((text, tag))
    
    def check_queue(self):
        """Check queue for messages from threads"""
        try:
            while True:
                text, tag = self.queue.get_nowait()
                if tag:
                    self.output_text.insert(tk.END, text + "\n", tag)
                else:
                    self.output_text.insert(tk.END, text + "\n")
                self.output_text.see(tk.END)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)
    
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
        self.update_status("Output cleared", "info")
    
    def validate_input(self):
        """Validate vehicle number input"""
        vehicle_number = self.vehicle_entry.get().strip().upper()
        if not vehicle_number:
            self.print_to_gui("❌ Error: Please enter a vehicle registration number", "error")
            self.update_status("No vehicle number entered", "error")
            return None
        return vehicle_number
    
    def set_loading_state(self, loading=True):
        """Show/hide loading animation and disable buttons"""
        state = tk.DISABLED if loading else tk.NORMAL
        self.fetch_all_btn.config(state=state)
        self.vehicle_btn.config(state=state)
        self.puc_btn.config(state=state)
        self.challan_btn.config(state=state)
        self.clear_btn.config(state=state)
        
        if loading:
            self.progress.start(10)
            self.update_status("Processing...", "info")
        else:
            self.progress.stop()
    
    def fetch_all_data(self):
        """Fetch all data types in sequence"""
        vehicle_number = self.validate_input()
        if not vehicle_number:
            return
        
        self.set_loading_state(True)
        self.clear_output()
        
        thread = threading.Thread(target=self._fetch_all_data_thread, args=(vehicle_number,))
        thread.daemon = True
        thread.start()
    
    def fetch_specific_data(self, data_type):
        """Fetch specific type of data"""
        vehicle_number = self.validate_input()
        if not vehicle_number:
            return
        
        self.set_loading_state(True)
        self.update_status(f"Fetching {data_type}...", "info")
        
        thread = threading.Thread(target=self._fetch_specific_data_thread, args=(vehicle_number, data_type))
        thread.daemon = True
        thread.start()
    
    def _fetch_all_data_thread(self, vehicle_number):
        """Thread function to fetch all data"""
        try:
            urls = [
                ("vehicle", f"{self.base_url}/asset_service/api/assets/search/vehicle/{vehicle_number}?validate=false&source=vas_fastag"),
                ("puc", f"{self.base_url}/vas/api/v1/pucs?registration-number={vehicle_number}"),
                ("challan", f"{self.base_url}/vas/api/v1/challans/?registration-number={vehicle_number}&source=CHALLAN_PAGE")
            ]
            
            for data_type, url in urls:
                self.print_to_gui("\n" + "═" * 60, "header")
                self.print_to_gui(f"FETCHING {data_type.upper()} DETAILS", "header")
                self.print_to_gui("═" * 60 + "\n", "header")
                
                response_data = self._fetch_url(url, data_type)
                
                if response_data:
                    # Handle different response formats
                    if response_data.get('status_code') == 200:
                        self._display_json_data(response_data.get('data', {}), data_type)
                    elif response_data.get('status_code') == 204:
                        self.print_to_gui(f"✅ No data found (Status: 204)", "success")
                    elif response_data.get('status_code') == 429:
                        # Rate limiting specific message for PUC
                        if data_type == "puc":
                            self.print_to_gui("❌ PUC API is rate limiting requests", "error")
                            self.print_to_gui("⚠️  Please wait a few minutes before trying again", "warning")
                        else:
                            self.print_to_gui(f"❌ Rate limited (429) for {data_type}", "error")
                    else:
                        self.print_to_gui(f"❌ Failed to fetch {data_type} data (Status: {response_data.get('status_code')})", "error")
                else:
                    self.print_to_gui(f"❌ Failed to fetch {data_type} data", "error")
            
            self.print_to_gui("\n" + "═" * 60, "header")
            self.print_to_gui("✅ ALL DATA FETCH COMPLETED", "success")
            self.print_to_gui("═" * 60, "header")
            
            self.update_status("All data fetched successfully!", "success")
            
        except Exception as e:
            self.print_to_gui(f"❌ Error in fetch_all_data_thread: {str(e)}", "error")
            self.update_status("Error occurred", "error")
        finally:
            self.set_loading_state(False)
    
    def _fetch_specific_data_thread(self, vehicle_number, data_type):
        """Thread function to fetch specific data"""
        try:
            url_map = {
                "vehicle": f"{self.base_url}/asset_service/api/assets/search/vehicle/{vehicle_number}?validate=false&source=vas_fastag",
                "puc": f"{self.base_url}/vas/api/v1/pucs?registration-number={vehicle_number}",
                "challan": f"{self.base_url}/vas/api/v1/challans/?registration-number={vehicle_number}&source=CHALLAN_PAGE"
            }
            
            url = url_map.get(data_type)
            if not url:
                self.print_to_gui(f"❌ Unknown data type: {data_type}", "error")
                return
            
            self.print_to_gui("\n" + "═" * 60, "header")
            self.print_to_gui(f"FETCHING {data_type.upper()} DETAILS", "header")
            self.print_to_gui("═" * 60 + "\n", "header")
            
            response_data = self._fetch_url(url, data_type)
            
            if response_data:
                if response_data.get('status_code') == 200:
                    self._display_json_data(response_data.get('data', {}), data_type)
                    self.update_status(f"{data_type.capitalize()} data fetched", "success")
                elif response_data.get('status_code') == 204:
                    self.print_to_gui(f"✅ No data found (Status: 204)", "success")
                    self.update_status(f"No {data_type} data found", "info")
                elif response_data.get('status_code') == 429:
                    if data_type == "puc":
                        self.print_to_gui("❌ PUC API is rate limiting requests", "error")
                        self.print_to_gui("⚠️  Please wait a few minutes before trying again", "warning")
                    else:
                        self.print_to_gui(f"❌ Rate limited (429) for {data_type}", "error")
                    self.update_status(f"Rate limited for {data_type}", "error")
                else:
                    self.print_to_gui(f"❌ Failed to fetch {data_type} data (Status: {response_data.get('status_code')})", "error")
                    self.update_status(f"Failed to fetch {data_type}", "error")
            else:
                self.print_to_gui(f"❌ Failed to fetch {data_type} data", "error")
                self.update_status(f"Failed to fetch {data_type}", "error")
                
        except Exception as e:
            self.print_to_gui(f"❌ Error: {str(e)}", "error")
            self.update_status("Error occurred", "error")
        finally:
            self.set_loading_state(False)
    
    def _fetch_url(self, url, data_type=None):
        """Fetch data from URL with error handling and rate limiting protection"""
        try:
            # Add delay to avoid rate limiting, especially for PUC
            if data_type == "puc":
                time.sleep(2)  # Longer delay for PUC API
            else:
                time.sleep(1)  # Normal delay for other APIs
            
            response = requests.get(url, headers=self.headers, stream=True, timeout=30)
            status_code = response.status_code
            
            if status_code == 404:
                self.print_to_gui(f"⚠️  404 Not Found: {url}", "warning")
                return {'status_code': 404, 'data': None}
            
            if status_code == 204:
                # Handle 204 No Content response
                return {'status_code': 204, 'data': None}
            
            if status_code == 429:
                # Rate limited - show specific message for PUC
                if data_type == "puc":
                    self.print_to_gui(f"⚠️  PUC API rate limited. Please try again after some time.", "warning")
                else:
                    self.print_to_gui(f"⚠️  Rate limited (429). Please wait...", "warning")
                return {'status_code': 429, 'data': None}
            
            # Handle content encoding
            encoding = response.headers.get("Content-Encoding", "")
            raw = response.raw.read()
            
            if "br" in encoding:
                decoded = brotli.decompress(raw).decode("utf-8")
            elif "gzip" in encoding:
                decoded = zlib.decompress(raw, zlib.MAX_WBITS | 16).decode("utf-8")
            elif "deflate" in encoding:
                decoded = zlib.decompress(raw).decode("utf-8")
            else:
                decoded = raw.decode("utf-8", errors='ignore')
            
            try:
                data = json.loads(decoded)
            except json.JSONDecodeError:
                # If it's not JSON, return as string
                data = decoded
            
            return {'status_code': status_code, 'data': data}
            
        except Exception as e:
            self.print_to_gui(f"❌ Fetch error: {str(e)}", "error")
            return None
    
    def _display_json_data(self, data, data_type):
        """Display JSON data in formatted way - FIXED VERSION"""
        try:
            if data is None:
                self.print_to_gui("No data available", "warning")
                return
            
            # Handle rate limiting specifically for PUC
            if data_type == "puc" and isinstance(data, dict) and data.get('status_code') == 429:
                self.print_to_gui("❌ PUC Data: Rate Limited by API", "error")
                self.print_to_gui("💡 Tip: Wait a few minutes and try again", "warning")
                return
            
            # Check if data is a string (as shown in your image)
            if isinstance(data, str):
                # Try to parse it as JSON first
                if data.strip().startswith('{') or data.strip().startswith('['):
                    try:
                        parsed_data = json.loads(data)
                        data = parsed_data
                    except json.JSONDecodeError:
                        # If it's not valid JSON, display as raw text
                        self._handle_text_format_data(data, data_type)
                        return
                else:
                    # Display as raw text
                    self._handle_text_format_data(data, data_type)
                    return
            
            # Format based on data type
            if data_type == "vehicle":
                self._format_vehicle_data(data)
            elif data_type == "puc":
                self._format_puc_data(data)
            elif data_type == "challan":
                self._format_challan_data(data)
            else:
                # Generic JSON display
                if isinstance(data, (dict, list)):
                    pretty_json = json.dumps(data, indent=2, ensure_ascii=False)
                    self.print_to_gui(pretty_json, "info")
                else:
                    self.print_to_gui(str(data), "info")
                
        except Exception as e:
            self.print_to_gui(f"❌ Display error: {str(e)}", "error")
            self.print_to_gui(str(data), "info")
    
    def _handle_text_format_data(self, data_text, data_type):
        """Handle text format data like in your screenshot"""
        lines = data_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for headers
            if line.startswith('---'):
                self.print_to_gui(line, "header")
            elif 'FETCHING' in line or 'ALL DATA FETCH' in line:
                self.print_to_gui(line, "header")
            elif 'Failed' in line or 'Error' in line:
                self.print_to_gui(line, "error")
            elif 'No data' in line or 'challan_free_since_date' in line:
                self.print_to_gui(line, "success")
            elif data_type == "challan" and line.startswith('{'):
                # Try to parse JSON lines
                try:
                    json_data = json.loads(line)
                    pretty_json = json.dumps(json_data, indent=2, ensure_ascii=False)
                    self.print_to_gui(pretty_json, "info")
                except:
                    self.print_to_gui(line, "info")
            else:
                self.print_to_gui(line, "info")
    
    def _format_vehicle_data(self, data):
        """Format vehicle data for display - FIXED VERSION"""
        if isinstance(data, dict):
            self.print_to_gui("📋 VEHICLE INFORMATION", "header")
            self.print_to_gui("-" * 40, "info")
            
            for key, value in data.items():
                if value is None:
                    continue
                    
                if isinstance(value, (dict, list)):
                    if key == 'vehicle_details' and isinstance(value, dict):
                        self.print_to_gui("\n🔧 DETAILED SPECIFICATIONS", "header")
                        self.print_to_gui("-" * 40, "info")
                        for sub_key, sub_value in value.items():
                            if sub_value is not None:
                                self.print_to_gui(f"{sub_key.replace('_', ' ').title():25}: {sub_value}", "info")
                    continue
                
                # Handle the format from your image
                display_key = key.replace('_', ' ').title()
                self.print_to_gui(f"{display_key:25}: {value}", "info")
        
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    self._format_vehicle_data(item)
        else:
            # Display as is
            self.print_to_gui(str(data), "info")
    
    def _format_puc_data(self, data):
        """Format PUC data for display"""
        if isinstance(data, list):
            if not data:
                self.print_to_gui("🌿 No PUC certificates found", "warning")
                return
                
            self.print_to_gui(f"🌿 POLLUTION CERTIFICATES ({len(data)})", "header")
            self.print_to_gui("-" * 40, "info")
            
            for i, cert in enumerate(data, 1):
                if isinstance(cert, dict):
                    self.print_to_gui(f"\nCertificate #{i}", "header")
                    for key, value in cert.items():
                        if value is not None:
                            self.print_to_gui(f"{key.replace('_', ' ').title():25}: {value}", "info")
                else:
                    self.print_to_gui(f"Certificate #{i}: {cert}", "info")
        elif isinstance(data, dict):
            self.print_to_gui("🌿 PUC DETAILS", "header")
            self.print_to_gui("-" * 40, "info")
            for key, value in data.items():
                if value is not None:
                    self.print_to_gui(f"{key.replace('_', ' ').title():25}: {value}", "info")
        else:
            self.print_to_gui(str(data), "info")
    
    def _format_challan_data(self, data):
        """Format challan data for display - FIXED VERSION"""
        if isinstance(data, dict):
            # Handle the format from your screenshot
            if 'data' in data:
                challan_list = data['data']
                if isinstance(challan_list, list):
                    self.print_to_gui(f"🚨 TRAFFIC CHALLAN STATUS", "header")
                    self.print_to_gui("-" * 40, "info")
                    
                    if not challan_list:
                        self.print_to_gui("✅ No pending challans found", "success")
                    
                    # Display other metadata
                    for key, value in data.items():
                        if key != 'data' and value is not None:
                            if 'challan_free_since_date' in key:
                                self.print_to_gui(f"{key.replace('_', ' ').title():30}: {value}", "success")
                            else:
                                self.print_to_gui(f"{key.replace('_', ' ').title():30}: {value}", "info")
                    
                    # Display challans if any
                    if challan_list:
                        self.print_to_gui(f"\n📋 PENDING CHALLANS ({len(challan_list)})", "header")
                        self.print_to_gui("-" * 40, "info")
                        for i, challan in enumerate(challan_list, 1):
                            self.print_to_gui(f"\nChallan #{i}", "header")
                            if isinstance(challan, dict):
                                for key, value in challan.items():
                                    if value is not None:
                                        self.print_to_gui(f"{key.replace('_', ' ').title():25}: {value}", "info")
                            else:
                                self.print_to_gui(str(challan), "info")
                else:
                    self.print_to_gui("Invalid challan data format", "error")
            else:
                # Display all dictionary data
                self.print_to_gui("🚨 CHALLAN INFORMATION", "header")
                self.print_to_gui("-" * 40, "info")
                for key, value in data.items():
                    if value is not None:
                        self.print_to_gui(f"{key.replace('_', ' ').title():25}: {value}", "info")
        
        elif isinstance(data, list):
            self.print_to_gui(f"🚨 TRAFFIC CHALLANS ({len(data)})", "header")
            self.print_to_gui("-" * 40, "info")
            
            if not data:
                self.print_to_gui("✅ No pending challans found", "success")
                return
            
            for i, challan in enumerate(data, 1):
                self.print_to_gui(f"\nChallan #{i}", "header")
                if isinstance(challan, dict):
                    for key, value in challan.items():
                        if value is not None:
                            self.print_to_gui(f"{key.replace('_', ' ').title():25}: {value}", "info")
                else:
                    self.print_to_gui(str(challan), "info")
        else:
            self.print_to_gui(str(data), "info")

# Main application
def main():
    root = tk.Tk()
    
    # Set window icon and styles
    try:
        root.iconbitmap(default='icon.ico')  # Add an icon file if available
    except:
        pass
    
    app = ProfessionalVehicleInfoGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()