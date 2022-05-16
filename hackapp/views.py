from django.shortcuts import render
from .models import Employee

#from django.http import HttpResponse
from django.http import JsonResponse

import requests
import json

REST_API_ENDPOINT = "http://localhost:8001/api/"

# MVT
# M - Model
# V - View - Controller(vs MVC)
# T - Template(Html, Css, Js)

# MVC
# M - Model
# V - View(Html, Css, Js)
# C - Controller - View(Django)

language_dict = {"af-ZA":["af-ZA-AdriNeural","af-ZA-WillemNeural"],
                "am-ET":["am-ET-MekdesNeural","am-ET-AmehaNeural"],
                "ar-DZ":["ar-DZ-AminaNeural","ar-DZ-IsmaelNeural"],
                "ar-BH":["ar-BH-LailaNeural","ar-BH-AliNeural"],
                "ar-EG":["ar-EG-SalmaNeural","ar-EG-ShakirNeural"],
                "ar-IQ":["ar-IQ-RanaNeural","ar-IQ-BasselNeural"],
                "ar-JO":["ar-JO-SanaNeural","ar-JO-TaimNeural"],
                "ar-KW":["ar-KW-NouraNeural","ar-KW-FahedNeural"],
                "ar-LY":["ar-LY-ImanNeural","ar-LY-OmarNeural"],
                "ar-MA":["ar-MA-MounaNeural","ar-MA-JamalNeural"],
                "ar-QA":["ar-QA-AmalNeural","ar-QA-MoazNeural"],
                "ar-SA":["ar-SA-ZariyahNeural","ar-SA-HamedNeural"],
                "ar-SY":["ar-SY-AmanyNeural","ar-SY-LaithNeural"],
                "ar-TN":["ar-TN-ReemNeural","ar-TN-HediNeural"],
                "ar-AE":["ar-AE-FatimaNeural","ar-AE-HamdanNeural"],
                "ar-YE":["ar-YE-MaryamNeural","ar-YE-SalehNeural"],
                "bn-BD":["bn-BD-NabanitaNeural","bn-BD-PradeepNeural"],
                "bn-IN":["bn-IN-TanishaaNeural New","bn-IN-BashkarNeural New"],
                "bg-BG":["bg-BG-KalinaNeural","bg-BG-BorislavNeural"],
                "my-MM":["my-MM-NilarNeural","my-MM-ThihaNeural"],
                "ca-ES":["ca-ES-AlbaNeural","ca-ES-EnricNeural"],
                "zh-HK":["zh-HK-HiuMaanNeural","zh-HK-WanLungNeural"],
                "zh-CN":["zh-CN-XiaochenNeural","zh-CN-YunxiNeural"],
                "zh-TW":["zh-TW-HsiaoChenNeural","zh-TW-YunJheNeural"],
                "hr-HR":["hr-HR-GabrijelaNeural","hr-HR-SreckoNeural"],
                "cs-CZ":["cs-CZ-VlastaNeural","cs-CZ-AntoninNeural"],
                "da-DK":["da-DK-ChristelNeural","da-DK-JeppeNeural"],
                "nl-BE":["nl-BE-DenaNeural","nl-BE-ArnaudNeural"],
                "nl-NL":["nl-NL-FennaNeural","nl-NL-MaartenNeural"],
                "en-AU":["en-AU-NatashaNeural","en-AU-WilliamNeural"],
                "en-CA":["en-CA-ClaraNeural","en-CA-LiamNeural"],
                "en-HK":["en-HK-YanNeural","en-HK-SamNeural"],
                "en-IN":["en-IN-NeerjaNeural","en-IN-PrabhatNeural"],
                "en-IE":["en-IE-EmilyNeural","en-IE-ConnorNeural"],
                "en-KE":["en-KE-AsiliaNeural","en-KE-ChilembaNeural"],
                "en-NZ":["en-NZ-MollyNeural","en-NZ-MitchellNeural"],
                "en-NG":["en-NG-EzinneNeural","en-NG-AbeoNeural"],
                "en-PH":["en-PH-RosaNeural","en-PH-JamesNeural"],
                "en-SG":["en-SG-LunaNeural","en-SG-WayneNeural"],
                "en-ZA":["en-ZA-LeahNeural","en-ZA-LukeNeural"],
                "en-TZ":["en-TZ-ImaniNeural","en-TZ-ElimuNeural"],
                "en-GB":["en-GB-LibbyNeural","en-GB-RyanNeural"],
                "en-US":["en-US-JennyNeural","en-US-ChristopherNeural"],
                "et-EE":["et-EE-AnuNeural","et-EE-KertNeural"],
                "fil-PH":["fil-PH-BlessicaNeural","fil-PH-AngeloNeural"],
                "fi-FI":["fi-FI-SelmaNeural","fi-FI-HarriNeural"],
                "fr-BE":["fr-BE-CharlineNeural","fr-BE-GerardNeural"],
                "fr-CA":["fr-CA-SylvieNeural","fr-CA-AntoineNeural"],
                "fr-FR":["fr-FR-DeniseNeural","fr-FR-HenriNeural"],
                "fr-CH":["fr-CH-ArianeNeural","fr-CH-FabriceNeural"],
                "gl-ES":["gl-ES-SabelaNeural","gl-ES-RoiNeural"],
                "de-AT":["de-AT-IngridNeural","de-AT-JonasNeural"],
                "de-DE":["de-DE-KatjaNeural","de-DE-ConradNeural"],
                "de-CH":["de-CH-LeniNeural","de-CH-JanNeural"],
                "el-GR":["el-GR-AthinaNeural","el-GR-NestorasNeural"],
                "gu-IN":["gu-IN-DhwaniNeural","gu-IN-NiranjanNeural"],
                "he-IL":["he-IL-HilaNeural","he-IL-AvriNeural"],
                "hi-IN":["hi-IN-SwaraNeural","hi-IN-MadhurNeural"],
                "hu-HU":["hu-HU-NoemiNeural","hu-HU-TamasNeural"],
                "is-IS":["is-IS-GudrunNeural New","is-IS-GunnarNeural New"],
                "id-ID":["id-ID-GadisNeural","id-ID-ArdiNeural"],
                "ga-IE":["ga-IE-OrlaNeural","ga-IE-ColmNeural"],
                "it-IT":["it-IT-IsabellaNeural","it-IT-DiegoNeural"],
                "ja-JP":["ja-JP-NanamiNeural","ja-JP-KeitaNeural"],
                "jv-ID":["jv-ID-SitiNeural","jv-ID-DimasNeural"],
                "kn-IN":["kn-IN-SapnaNeural New","kn-IN-GaganNeural New"],
                "kk-KZ":["kk-KZ-AigulNeural New","kk-KZ-DauletNeural New"],
                "km-KH":["km-KH-SreymomNeural","km-KH-PisethNeural"],
                "ko-KR":["ko-KR-SunHiNeural","ko-KR-InJoonNeural"],
                "lo-LA":["lo-LA-KeomanyNeural New","lo-LA-ChanthavongNeural New"],
                "lv-LV":["lv-LV-EveritaNeural","lv-LV-NilsNeural"],
                "lt-LT":["lt-LT-OnaNeural","lt-LT-LeonasNeural"],
                "mk-MK":["mk-MK-MarijaNeural New","mk-MK-AleksandarNeural New"],
                "ms-MY":["ms-MY-YasminNeural","ms-MY-OsmanNeural"],
                "ml-IN":["ml-IN-SobhanaNeural New","ml-IN-MidhunNeural New"],
                "mt-MT":["mt-MT-GraceNeural","mt-MT-JosephNeural"],
                "mr-IN":["mr-IN-AarohiNeural","mr-IN-ManoharNeural"],
                "nb-NO":["nb-NO-PernilleNeural","nb-NO-FinnNeural"],
                "ps-AF":["ps-AF-LatifaNeural New","ps-AF-GulNawazNeural New"],
                "fa-IR":["fa-IR-DilaraNeural","fa-IR-FaridNeural"],
                "pl-PL":["pl-PL-ZofiaNeural","pl-PL-MarekNeural"],
                "pt-BR":["pt-BR-FranciscaNeural","pt-BR-AntonioNeural"],
                "pt-PT":["pt-PT-RaquelNeural","pt-PT-DuarteNeural"],
                "ro-RO":["ro-RO-AlinaNeural","ro-RO-EmilNeural"],
                "ru-RU":["ru-RU-SvetlanaNeural","ru-RU-DmitryNeural"],
                "sr-RS":["sr-RS-SophieNeural New","sr-RS-NicholasNeural New"],
                "si-LK":["si-LK-ThiliniNeural New","si-LK-SameeraNeural New"],
                "sk-SK":["sk-SK-ViktoriaNeural","sk-SK-LukasNeural"],
                "sl-SI":["sl-SI-PetraNeural","sl-SI-RokNeural"],
                "so-SO":["so-SO-UbaxNeural","so-SO-MuuseNeural"],
                "es-AR":["es-AR-ElenaNeural","es-AR-TomasNeural"],
                "es-BO":["es-BO-SofiaNeural","es-BO-MarceloNeural"],
                "es-CL":["es-CL-CatalinaNeural","es-CL-LorenzoNeural"],
                "es-CO":["es-CO-SalomeNeural","es-CO-GonzaloNeural"],
                "es-CR":["es-CR-MariaNeural","es-CR-JuanNeural"],
                "es-CU":["es-CU-BelkysNeural","es-CU-ManuelNeural"],
                "es-DO":["es-DO-RamonaNeural","es-DO-EmilioNeural"],
                "es-EC":["es-EC-AndreaNeural","es-EC-LuisNeural"],
                "es-SV":["es-SV-LorenaNeural","es-SV-RodrigoNeural"],
                "es-GQ":["es-GQ-TeresaNeural","es-GQ-JavierNeural"],
                "es-GT":["es-GT-MartaNeural","es-GT-AndresNeural"],
                "es-HN":["es-HN-KarlaNeural","es-HN-CarlosNeural"],
                "es-MX":["es-MX-DaliaNeural","es-MX-JorgeNeural"],
                "es-NI":["es-NI-YolandaNeural","es-NI-FedericoNeural"],
                "es-PA":["es-PA-MargaritaNeural","es-PA-RobertoNeural"],
                "es-PY":["es-PY-TaniaNeural","es-PY-MarioNeural"],
                "es-PE":["es-PE-CamilaNeural","es-PE-AlexNeural"],
                "es-PR":["es-PR-KarinaNeural","es-PR-VictorNeural"],
                "es-ES":["es-ES-ElviraNeural","es-ES-AlvaroNeural"],
                "es-UY":["es-UY-ValentinaNeural","es-UY-MateoNeural"],
                "es-US":["es-US-PalomaNeural","es-US-AlonsoNeural"],
                "es-VE":["es-VE-PaolaNeural","es-VE-SebastianNeural"],
                "su-ID":["su-ID-TutiNeural","su-ID-JajangNeural"],
                "sw-KE":["sw-KE-ZuriNeural","sw-KE-RafikiNeural"],
                "sw-TZ":["sw-TZ-RehemaNeural","sw-TZ-DaudiNeural"],
                "sv-SE":["sv-SE-SofieNeural","sv-SE-MattiasNeural"],
                "ta-IN":["ta-IN-PallaviNeural","ta-IN-ValluvarNeural"],
                "ta-SG":["ta-SG-VenbaNeural","ta-SG-AnbuNeural"],
                "ta-LK":["ta-LK-SaranyaNeural","ta-LK-KumarNeural"],
                "te-IN":["te-IN-ShrutiNeural","te-IN-MohanNeural"],
                "th-TH":["th-TH-AcharaNeural","th-TH-PremwadeeNeural"],
                "th-TH":["th-TH-PremwadeeNeural","th-TH-NiwatNeural"],
                "tr-TR":["tr-TR-EmelNeural","tr-TR-AhmetNeural"],
                "uk-UA":["uk-UA-PolinaNeural","uk-UA-OstapNeural"],
                "ur-IN":["ur-IN-GulNeural","ur-IN-SalmanNeural"],
                "ur-PK":["ur-PK-UzmaNeural","ur-PK-AsadNeural"],
                "uz-UZ":["uz-UZ-MadinaNeural","uz-UZ-SardorNeural"],
                "vi-VN":["vi-VN-HoaiMyNeural","vi-VN-NamMinhNeural"],
                "cy-GB":["cy-GB-NiaNeural","cy-GB-AledNeural"],
                "zu-ZA":["zu-ZA-ThandoNeural","zu-ZA-ThembaNeural"]}

# Create your views here.


def get_voicenames_vw(request):
    print("Inside if loop of get_voicenames_vw")

    if request.method == "POST":
        language_id = request.POST['language_id']
        print("language_id")
        print(language_id)
        try:
            voice_names = language_dict[language_id]
            print("voice_names")
            print(voice_names)
            voice_names_data = []

            # '-'.join([voice_name_split[0], voice_name_split[1]])
            for voice_name in voice_names:
                voice_name_split = voice_name.split('-')
                voice_names_data.append({'id': voice_name, 'title': voice_name_split[2]})
        except Exception as ex:
            data = {}
            data['error_message'] = 'Error'
            return JsonResponse(data)

        print(voice_names_data)
        return JsonResponse(voice_names_data, safe=False)

def name_pronunciation_vw(request):
    if request.method == 'POST':
        print("Inside if loop of name_pronunciation_vw")
        #preferred_name_text = request.POST.get('emp_preferred_name')
        #name_text = request.POST.get('emp_name')
        #print("name_text: ")
        #print(name_text)

        name_text = None
        std_ctm_pronunciation = None
        language = None
        voice_name = None
        speaking_style = None
        standard_pronunciation = None
        custom_pronunciation = None

        emp_id_or_name = request.GET.get('emp_id_or_name')
        print(emp_id_or_name)
        std_ctm_pronunciation = request.POST['std_ctm_pronunciation']
        print("Printing Radio button value")
        print(std_ctm_pronunciation)

        language = request.POST.get('languageselect')
        voice_name = request.POST.get('voiceselect')
        speaking_style = request.POST.get('voicestyleselect')
        print("Printing Dropdown values")
        print(language)
        print(voice_name)
        print(speaking_style)

        if std_ctm_pronunciation == 'STD':
            standard_pronunciation = True
            language = 'en-US'
            voice_name = 'en-US-JennyNeural'
        elif std_ctm_pronunciation == 'CTM':
            custom_pronunciation = True

        try:
            employee = Employee.objects.get(emp_id=emp_id_or_name)
            name_text = employee.emp_name
            preferred_name_text = employee.emp_preferred_name

            if preferred_name_text is not None and preferred_name_text != '':
                name_text = preferred_name_text

            print("name_text: ")
            print(name_text)
        except Employee.DoesNotExist:
            employee = None
            if emp_id_or_name is None:
                emp_id_or_name = ''

        name_input_data = { "name_text": name_text, "language": language, "std_ctm_pronunciation": std_ctm_pronunciation, "voice_name": voice_name, "speaking_style": speaking_style, "audio_file": "" }

        print(employee)
        headers = {'Content-type': 'application/json'}

        try:

            # and (employee.custom_pronunciation_audio is None or employee.custom_pronunciation_audio == '')
            if ((standard_pronunciation is True and (employee.std_pronunciation_audio is None or employee.std_pronunciation_audio == '')) or
                    (custom_pronunciation is True)):
                print("REST API Post is Required")
                # Convert post input data/request and get the reponse data
                # Post data to REST API
                response = requests.post(url=REST_API_ENDPOINT, data=json.dumps(name_input_data), headers=headers)
                print(response)
                name_pronunciation = response.json()
                print("name_pronunciation")
                print(name_pronunciation)

                # Saving details to DB
                if name_pronunciation['data']['audio_file'] is not None and name_pronunciation['data']['audio_file'] != '':
                    if standard_pronunciation is True:
                        employee.std_pronunciation_audio = name_pronunciation['data']['audio_file']
                    elif custom_pronunciation is True:
                        employee.custom_pronunciation_audio = name_pronunciation['data']['audio_file']
                    print("Save Data is Required")
                    employee.save()
            else:
                print("REST API Post is not Required")
                audio_file = None
                if standard_pronunciation is True:
                    audio_file = employee.std_pronunciation_audio
                elif custom_pronunciation is True:
                    audio_file = employee.custom_pronunciation_audio
                name_pronunciation = {"status":"success","data":{"id": employee.emp_id,
                                                                 "name_text": name_text,
                                                                 "audio_file": audio_file}}
                print(name_pronunciation)
        except Exception as ex:
            print("Failed to access REST API")
            print(ex)
            name_pronunciation = None

        context = {'data': {"emp_id_or_name": emp_id_or_name,
                            "standard_pronunciation": standard_pronunciation,
                            'custom_pronunciation': custom_pronunciation,
                            'employee': employee, "name_pronunciation": name_pronunciation}}
        return render(request, "home.html", context)
    elif request.method == 'GET':
        print("Inside elif loop of name_pronunciation_vw")
        emp_id_or_name = request.GET.get('emp_id_or_name')
        print(emp_id_or_name)
        employees = Employee.objects.all()
        print(employees)
        try:
            employee = Employee.objects.get(emp_id=emp_id_or_name)
        except Employee.DoesNotExist:
            employee = None
            if emp_id_or_name is None:
                emp_id_or_name = ''

        context = {'data': {"emp_id_or_name": emp_id_or_name, 'employee': employee}}
        print(context)
        return render(request, "home.html", context)