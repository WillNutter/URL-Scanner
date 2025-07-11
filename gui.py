import tkinter as tk
from tkinter import messagebox
import urllib.request
import urllib.error
import socket
from urllib.parse import urlparse

def check_url(url, timeout=5):
    try:
        req = urllib.request.Request(url, method='HEAD')
        response = urllib.request.urlopen(req, timeout=timeout)
        final_url = response.geturl()
        parsed = urlparse(final_url)
        hostname = parsed.hostname
        ip_address = socket.gethostbyname(hostname)
        return {
            'original_url': url,
            'final_url': final_url,
            'ip': ip_address,
            'status': 'OK'
        }
    except urllib.error.HTTPError as e:
        return {'original_url': url, 'error': f'HTTP Error {e.code}', 'status': 'Failed'}
    except urllib.error.URLError as e:
        return {'original_url': url, 'error': f'URL Error: {e.reason}', 'status': 'Failed'}
    except socket.gaierror:
        return {'original_url': url, 'error': 'Could not resolve host', 'status': 'Failed'}
    except Exception as e:
        return {'original_url': url, 'error': f'Unexpected error: {str(e)}', 'status': 'Failed'}

def analyze_urls(urls, output_box, fail_box):
    output_box.delete(1.0, tk.END)
    fail_box.delete(1.0, tk.END)
    non_working = []

    for url in urls:
        url = url.strip()
        if not url:
            continue
        result = check_url(url)
        if result['status'] == 'OK':
            output_box.insert(tk.END, f"✔ {url}\n")
            output_box.insert(tk.END, f"  → Final URL: {result['final_url']}\n")
            output_box.insert(tk.END, f"  → IP Address: {result['ip']}\n\n")
        else:
            output_box.insert(tk.END, f"✖ {url}\n")
            output_box.insert(tk.END, f"  → Error: {result['error']}\n\n")
            non_working.append(url)

    if non_working:
        fail_box.insert(tk.END, "=== Non-working URLs ===\n")
        for bad_url in non_working:
            fail_box.insert(tk.END, f"- {bad_url}\n")

def launch_gui():
    root = tk.Tk()
    root.title("URL Scanner / Link Checker")
    root.geometry("800x600")

    tk.Label(root, text="Enter URLs (one per line):").pack()
    input_box = tk.Text(root, height=10)
    input_box.pack(padx=10, pady=5, fill='x')

    tk.Label(root, text="Results:").pack()
    output_box = tk.Text(root, height=15, wrap='word')
    output_box.pack(padx=10, pady=5, fill='both', expand=True)

    tk.Label(root, text="Non-working URLs:").pack()
    fail_box = tk.Text(root, height=5, wrap='word', bg='#fdd')
    fail_box.pack(padx=10, pady=5, fill='x')

    analyze_button = tk.Button(
        root, text="Analyze",
        command=lambda: analyze_urls(input_box.get("1.0", tk.END).splitlines(), output_box, fail_box)
    )
    analyze_button.pack(pady=5)

    root.mainloop()