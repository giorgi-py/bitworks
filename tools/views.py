from django.shortcuts import render

# Create your views here.
def tools_view(r):
    return render(r, 'tools.html')

# views.py - Step 2: Enhanced view with HTMX support
import socket
import re
import requests
from django.shortcuts import render
from django.http import JsonResponse

def perform_port_check(host, port, timeout):
    """Basic port checking function"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            return {
                'status': 'open',
                'message': f'Port {port} is open on {host}',
                'success': True
            }
        else:
            return {
                'status': 'closed',
                'message': f'Port {port} is closed on {host}',
                'success': False
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error checking port: {str(e)}',
            'success': False
        }

def validate_host(request):
    """Real-time host validation"""
    if request.method == 'POST':
        host = request.POST.get('host', '').strip()
        
        if not host:
            return render(request, 'partials/validation_message.html', {
                'message': '',
                'valid': True
            })
        
        # Basic validation
        if is_valid_host(host):
            return render(request, 'partials/validation_message.html', {
                'message': 'Valid host',
                'valid': True
            })
        else:
            return render(request, 'partials/validation_message.html', {
                'message': 'Invalid host format',
                'valid': False
            })

def is_valid_host(host):
    """Validate host format (IP or domain)"""
    # IP address pattern
    ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    
    # Domain pattern (basic)
    domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    
    return re.match(ip_pattern, host) or re.match(domain_pattern, host)

def check_port_view(request):
    x_forward = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward:
        ip = x_forward.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if request.method == 'POST':
        host = request.POST.get('host')
        port = int(request.POST.get('port'))
        timeout = int(request.POST.get('timeout', 5))
        print (host, port, timeout)
        
        # Port checking logic
        result = perform_port_check(host, port, timeout)
        
        # Check if request is from HTMX
        if request.headers.get('HX-Request'):
            # Return partial HTML for HTMX
            return render(request, 'partials/port_result.html', {
                'result': result,
                'host': host,
                'port': port
            })
        else:
            # Return full page for regular POST
            return render(request, 'check_port.html', {
                'result': result,
                'host': host,
                'port': port,
                'ip': ip
            })
    
    return render(request, 'check_port.html', {'ip': ip})

# def check_port_view(r):
#     return render(r, 'check_port.html')

def dns_lookup_view(r):
    return render(r, 'dns_lookup.html')

# # # # # DNS LOOKUP SECTION # # # # #

try:
    import dns.resolver
    import dns.reversename
    import dns.exception
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False


def dns_lookup_view(request):
    if request.method == 'POST':
        domain = request.POST.get('domain', '').strip()
        lookup_type = request.POST.get('lookup_type')
        dns_server = request.POST.get('dns_server', 'default')
        custom_dns = request.POST.get('custom_dns', '').strip()
        timeout = int(request.POST.get('timeout', 5))
        
        # Perform DNS lookup
        if lookup_type == 'all':
            result = perform_all_dns_lookup(domain, dns_server, custom_dns, timeout)
        else:
            result = perform_single_dns_lookup(domain, lookup_type, dns_server, custom_dns, timeout)
        
        return render(request, 'dns_lookup.html', {
            'result': result,
            'domain': domain,
            'lookup_type': lookup_type
        })
    
    return render(request, 'dns_lookup.html')

def perform_all_dns_lookup(domain, dns_server, custom_dns, timeout):
    """Perform lookup for all common DNS record types"""
    record_types = ['A', 'AAAA', 'MX', 'CNAME', 'NS', 'TXT', 'SOA']
    results = {}
    
    for record_type in record_types:
        try:
            result = perform_single_dns_lookup(domain, record_type, dns_server, custom_dns, timeout)
            if result['success'] and result['records']:
                results[record_type] = result['records']
        except Exception:
            continue
    
    if results:
        return {
            'success': True,
            'lookup_type': 'all',
            'results': results,
            'message': f'DNS lookup completed for {domain}'
        }
    else:
        return {
            'success': False,
            'message': f'No DNS records found for {domain}',
            'results': {}
        }

def perform_single_dns_lookup(domain, record_type, dns_server, custom_dns, timeout):
    """Perform DNS lookup for a specific record type"""
    if not DNS_AVAILABLE:
        return fallback_dns_lookup(domain, record_type)
    
    try:
        # Configure DNS resolver
        resolver = dns.resolver.Resolver()
        resolver.timeout = timeout
        
        # Set DNS server
        if dns_server == 'custom' and custom_dns:
            resolver.nameservers = [custom_dns]
        elif dns_server != 'default':
            resolver.nameservers = [dns_server]
        
        # Handle reverse DNS lookup
        if record_type == 'PTR':
            if is_valid_ip(domain):
                query_domain = dns.reversename.from_address(domain)
            else:
                return {
                    'success': False,
                    'message': 'PTR lookup requires an IP address',
                    'records': []
                }
        else:
            query_domain = domain
        
        # Perform the lookup
        answers = resolver.resolve(query_domain, record_type)
        records = []
        
        for answer in answers:
            record_data = {
                'value': str(answer),
                'ttl': answers.ttl
            }
            
            # Add specific formatting for different record types
            if record_type == 'MX':
                record_data['priority'] = answer.preference
                record_data['exchange'] = str(answer.exchange)
            elif record_type == 'SOA':
                record_data.update({
                    'mname': str(answer.mname),
                    'rname': str(answer.rname),
                    'serial': answer.serial,
                    'refresh': answer.refresh,
                    'retry': answer.retry,
                    'expire': answer.expire,
                    'minimum': answer.minimum
                })
            elif record_type == 'SRV':
                record_data.update({
                    'priority': answer.priority,
                    'weight': answer.weight,
                    'port': answer.port,
                    'target': str(answer.target)
                })
            
            records.append(record_data)
        
        return {
            'success': True,
            'message': f'{record_type} records found for {domain}',
            'records': records,
            'record_type': record_type
        }
        
    except dns.resolver.NXDOMAIN:
        return {
            'success': False,
            'message': f'Domain {domain} does not exist',
            'records': []
        }
    except dns.resolver.NoAnswer:
        return {
            'success': False,
            'message': f'No {record_type} records found for {domain}',
            'records': []
        }
    except dns.exception.Timeout:
        return {
            'success': False,
            'message': f'DNS lookup timed out for {domain}',
            'records': []
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error performing DNS lookup: {str(e)}',
            'records': []
        }

def fallback_dns_lookup(domain, record_type):
    """Fallback DNS lookup using socket (limited functionality)"""
    if record_type == 'A':
        try:
            ip = socket.gethostbyname(domain)
            return {
                'success': True,
                'message': f'A record found for {domain}',
                'records': [{'value': ip, 'ttl': 'N/A'}],
                'record_type': 'A'
            }
        except socket.gaierror:
            return {
                'success': False,
                'message': f'Could not resolve {domain}',
                'records': []
            }
    else:
        return {
            'success': False,
            'message': f'{record_type} lookup requires dnspython library',
            'records': []
        }

def is_valid_ip(ip):
    """Check if string is a valid IP address"""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False