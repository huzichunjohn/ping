from django import forms
from netaddr import IPAddress, AddrFormatError

class PingForm(forms.Form):
    network_range = forms.CharField(label='the network range', max_length=31)

    def clean_network_range(self):
	data = self.cleaned_data['network_range']
	try:
	    start_ip, end_ip = data.split('-')
	
	    if not start_ip or not end_ip:
		raise forms.ValidationError('the start ip or the end ip is None.')
	    elif IPAddress(start_ip) > IPAddress(end_ip):
		raise forms.ValidationError('the end ip must great than the start ip.')	
	except AddrFormatError:
	    raise forms.ValidationError('the ip address is not valid.')    
	except ValueError:
	    raise forms.ValidationError('the network range is split by "-".')
	return data
