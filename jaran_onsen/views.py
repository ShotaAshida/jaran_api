from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .forms import jaranOnsenForm
from django.shortcuts import redirect
from .models import jaranOnsen, jaranOnsenPost
import urllib.request
from xml.dom.minidom import parseString


# Create your views here.
def jaran_onsen_list(request): 
	onsens = jaranOnsen.objects.order_by('id') 
	return render(request, 'jaran_onsen/jaran_onsen_list.html', {'onsens': onsens})

def jaran_onsen_detail(request, onsen_id):
	onsen = get_object_or_404(jaranOnsen, onsen_id=onsen_id)
	return render(request, 'jaran_onsen/jaran_onsen_detail.html', {'onsen': onsen})

def jaran_onsen_api(request):
	if request.method == "POST":
		form = jaranOnsenForm(request.POST)
		#onsen = jaranOnsen() 
		onsens = [] 
		if form.is_valid():		
			parseJaranXml(onsens, form)
			#return redirect('jaran_onsen_detail', onsen_id=onsen.onsen_id)
			return render(request, 'jaran_onsen/jaran_onsens_added.html', {'onsens' : onsens})
	else:
		form = jaranOnsenForm()
	return render(request, 'jaran_onsen/jaran_onsen_api.html', {form: form})

'''def jaran_onsens_added(request):
	onsens =  get_object_or_404(onsens=onsens)
	return render(request, 'jaran_onsen/jaran_onsens_added.html', {'onsens': onsens})'''


def parseJaranXml(onsens, form):
	key = "peg16a7c976570"
	try:
		url = "http://jws.jalan.net/APICommon/OnsenSearch/V1/?key=" + key + "&l_area=" + str(form.data['l_area']) + "&count=" + str(form.data['count']) + "&xml_ptn=" + str(form.data['xml_ptn'])
		xml = urllib.request.urlopen(url)

	except urllib.error.HTTPError as error:
		pass

	dom = parseString(xml.read())
	num_of_rlts = int(nodeValueNoneCheck(dom.getElementsByTagName('NumberOfResults')[0], True))
	onsen_names = dom.getElementsByTagName('OnsenName')
	onsen_name_kanas = dom.getElementsByTagName('OnsenNameKana')
	onsen_ids = dom.getElementsByTagName('OnsenID')
	onsen_addresses = dom.getElementsByTagName('OnsenAddress')
	regions = dom.getElementsByTagName('Region')
	prefectures = dom.getElementsByTagName('Prefecture')
	large_areas = dom.getElementsByTagName('LargeArea')
	small_areas = dom.getElementsByTagName('SmallArea')
	nature_of_onsens = dom.getElementsByTagName('NatureOfOnsen')
	onsen_area_names = dom.getElementsByTagName('OnsenAreaName')
	onsen_area_name_kanas = dom.getElementsByTagName('OnsenAreaNameKana')
	onsen_area_ids = dom.getElementsByTagName('OnsenAreaID')
	onsen_area_urls = dom.getElementsByTagName('OnsenAreaURL')
	onsen_area_captions = dom.getElementsByTagName('OnsenAreaCaption')

	for i in range(0, num_of_rlts):
		onsen = jaranOnsen()
		onsen.onsen_name = nodeValueNoneCheck(onsen_names[i])
		onsen.onsen_name_kana = nodeValueNoneCheck(onsen_name_kanas[i])
		onsen.onsen_id = nodeValueNoneCheck(onsen_ids[i], True)
		onsen.onsen_address = nodeValueNoneCheck(onsen_addresses[i])
		onsen.regions = nodeValueNoneCheck(regions[i])
		onsen.prefectures = nodeValueNoneCheck(prefectures[i])
		onsen.large_area = nodeValueNoneCheck(large_areas[i])
		onsen.small_area = nodeValueNoneCheck(small_areas[i])
		onsen.nature_of_onsen = nodeValueNoneCheck(nature_of_onsens[i])
		onsen.onsen_area_name = nodeValueNoneCheck(onsen_area_names[i])
		onsen.onsen_area_name_kana = nodeValueNoneCheck(onsen_area_name_kanas[i])
		onsen.onsen_area_id = nodeValueNoneCheck(onsen_area_ids[i], True)
		onsen.onsen_area_url = nodeValueNoneCheck(onsen_area_urls[i])
		onsen.onsen_area_caption = nodeValueNoneCheck(onsen_area_captions[i])
		onsens.append(onsen)
		onsen.save()

def nodeValueNoneCheck(element, id = False):
	if element.firstChild != None: 
		return element.firstChild.nodeValue
	else:
		if id:
			return 0
		else:	
			return "None"	 
