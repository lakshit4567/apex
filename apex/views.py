from datetime import date 
from django.shortcuts import render, redirect
from django.contrib.auth.admin import User
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .decoraters import *
from .filters import *
from .task import *
from .helper import *
from django.contrib import messages
# Create your views here.


#Admin Dashboard View 
@login_required(login_url='login') # decorator for required login
@allowed_users(allowed_roles=['admin'])# allowed user decorator only admin can access this view
def Admin_Dashboard(request):
    today = date.today()

    # filtering data for dashboard page grahs
    es = essentialitemStock.objects.filter(ES_Date__year=today.year, 
                                           ES_Date__month=today.month,
                                           ES_Date=today).values()
    upd = EssentialItemUsePerDay.objects.filter(EPD_Date__year=today.year,
                                                EPD_Date__month=today.month,
                                                EPD_Date=today).values()
    s = Sale.objects.filter(Sale_date__year=today.year).values()
    rw = rawMaterial.objects.filter(RM_Date__year=today.year,
                                    RM_Date__month=today.month,).values()
    fm = FMstock.objects.filter(FM_Date__year=today.year).values()

    # extracting data from filtered accordingly in dictionary formate
    dic_weight = dic_key_val.dict_for_raw(
        dic=rw, key='RM_Date', value='RM_coilWeight')
    check_for_null_values(d=dic_weight)
    dic_scrap = dic_key_val.dict_for_raw(
        dic=rw, key='RM_Date', value='RM_scrapWeight')
    check_for_null_values(d=dic_scrap)
    fm_weight = dic_key_val.dict_for_raw(
        dic=fm, key='FM_Date', value='FM_Weight')
    check_for_null_values(d=fm_weight)
    fm_scrap = dic_key_val.dict_for_raw(
        dic=fm, key='FM_Date', value='FM_scrapWeight')
    check_for_null_values(d=fm_scrap)
    fm_flow_q = dic_key_val.dict_for_fm(
        dic=fm, key='FM_Date', value='FM_Quantity')
    fm_flow_s = dic_key_val.dict_for_fm(
        dic=s, key='Sale_date', value='Sale_Quantity')
    es_stock = dic_key_val.dict(dic=es, key='Type', value='ES_Quantity')
    es_usage = dic_key_val.dict(dic=upd, key='EPD_Type', value='EPD_Quantity')

    # dumping all dictionaries in json
    dict = json.dumps(dic_weight)
    dict_s = json.dumps(dic_scrap)
    dic_f_w = json.dumps(fm_weight)
    dic_f_s = json.dumps(fm_scrap)
    dic_f_q = json.dumps(fm_flow_q)
    dic_flow_s = json.dumps(fm_flow_s)
    dic_es = json.dumps(es_stock)
    dic_usage = json.dumps(es_usage)

    #loading dumped data 
    rw_month = json.loads(dict)
    rw_s_month = json.loads(dict_s)
    fm_w = json.loads(dic_f_w)
    fm_s = json.loads(dic_f_s)
    f_q = json.loads(dic_f_q)
    f_s = json.loads(dic_flow_s)
    es_s = json.loads(dic_es)
    es_u = json.loads(dic_usage)

    # rendering all message in notfication modal in reverse order so the new message is always on top
    all_ms = Messages.objects.all().order_by("-id")
    header = 'Overview'

    # rendering last 5 messages for dropdown notification in reverse order
    ms = Messages.objects.filter().order_by('-id')[:5]

    # rendering count of all messages
    ms_count = str(Messages.objects.filter(seen__exact='False').count())

    #rendering scrap material table
    scrap_t = Scrape.objects.all()
    for i in scrap_t:
        print(i.t_id)
        
        
    # user_name = scrap_t.t_id
    # print(user_name)


    return render(request, 'apex/overview.html', {'header': header, 'ms': ms, 'ms_count': ms_count, 'all_ms': all_ms,
                                                'scrap_t': scrap_t, 'rw_month': rw_month, 'rw_s_month': rw_s_month, 'fm_w': fm_w,
                                                'fm_s': fm_s, 'f_q': f_q, 'f_s': f_s, 'es_s': es_s, 'es_u': es_u})




# user account page view
@login_required(login_url='login') # decorator for required login
def User_Account(request):
    # rendering time on emplayee account tab
    time = Timmer.objects.filter().last()
    a_time = str(time.active_time)
    d_time = str(time.inactive_time)
    
    # rendering all message in notfication modal in reverse order so the new message is always on top
    all_ms = Messages.objects.all().order_by("-id")

    # rendering last 5 messages for dropdown notification in reverse order
    ms = Messages.objects.filter().order_by('-id')[:5]

     # rendering count of all messages
    ms_count = str(Messages.objects.filter(seen__exact='False').count())

    header = 'Account'
    context = {}

    #geting user data for my account tab
    data = Register.objects.get(user__id=request.user.id)

    #rendering user data for employee account tab
    data1 = Register.objects.all()

    #rendering deleted tables data on deleted tables tab
    d_tables = Deleted_tables.objects.all()
    
   # passing data in context
    context['room_code'] = data.user.username
    context['data'] = data
    context['data1'] = data1
    context['header'] = header
    context['ms_count'] = ms_count
    context['ms'] = ms
    context['all_ms'] = all_ms
    context['d_tables'] = d_tables
    context['a_time'] = a_time
    context['d_time'] = d_time

    return render(request, 'apex/user_account.html', context)



# Raw material page view
@login_required(login_url='login') # decorator for required login
def User_Raw_Material(request):
    # geting start and end date from date filters
    try:
        startDate = request.GET['start_date']
        endDate = request.GET['end_date']
    except:
        startDate = None
        endDate = None

    #filtering raw table in graph
    if startDate and endDate != None:
        # rendering raw data from date filters to graph
        rw_data = rawMaterial.objects.filter(RM_Date__gte=startDate, RM_Date__lte=endDate).values()
        
        # extracting grade and coilweight from filtered data
        d_weight = dic_key_val.dict(dic=rw_data, key='RM_Grade', value='RM_coilWeight')

        # dumping extracted data
        dict = json.dumps(d_weight)

        # laoding data
        raw = json.loads(dict)

    else:
        # rending all raw data to graph
        rw_data = rawMaterial.objects.values()

        # extracting grade and coilweight from filtered data
        d_weight = dic_key_val.dict(dic=rw_data, key='RM_Grade', value='RM_coilWeight')

        # dumping extracted data    
        dict = json.dumps(d_weight)

        # laoding data
        raw = json.loads(dict)

    
    # rendering all message in notfication modal in reverse order so the new message is always on top
    all_ms = Messages.objects.all().order_by("-id")

    # rendering last 5 messages for dropdown notification in reverse order
    ms = Messages.objects.filter().order_by('-id')[:5]

    # rendering count of all messages
    ms_count = str(Messages.objects.filter(seen__exact='False').count())

    header = 'Raw Material Stock'

    # rendering raw material data in table
    data = rawMaterial.objects.all()

    #rendering log table for raw material data
    log = LogTable.objects.filter(Table_name__exact='Raw Material')

    # date filters 
    rawFilter = RMFilter(request.GET, queryset=data)
    data = rawFilter.qs

    # getting users to to check if their access provided by admin
    us = User.objects.get(id=request.user.id)
    rg = Register.objects.get(user=us)

    #Context
    d = {'data': data, 'log': log, 'myFilter': rawFilter,  'header': header, 'ms': ms, 'ms_count': ms_count, 'all_ms': all_ms, 'raw': raw, 'd_access': str(rg.delete_access),
        'role': str(rg.userRole),'username':'saif','room_code':'admin'}
    return render(request, 'apex/user_raw_material.html', d)



@login_required(login_url='login')# decorator for required login
def User_UnFinished_Material(request):
    # geting start and end date from date filters
    try:
        startDate = request.GET['start_date']
        endDate = request.GET['end_date']
    except:
        startDate = None
        endDate = None

    if startDate and endDate != None:
        # rendering ufm data from date filters to graph
        ufm_data = UFMstock.objects.filter(
            UFM_date__gte=startDate, UFM_date__lte=endDate).values()
        sale_data = Sale.objects.filter(
            Stock__exact='Un-Finished Material Stock', Sale_date__gte=startDate, Sale_date__lte=endDate).values()

        # extracting grade and ufm type from filtered data
        d_quantity = dic_key_val.dict(
            dic=ufm_data, key='UFM_type', value='UFM_Quantity')

        # extracting grade and sale type from filtered data
        d_sale = dic_key_val.dict(
            dic=sale_data, key='Sale_Type', value='Sale_Quantity')
        
        # dumping data in json
        dict_q = json.dumps(d_quantity)
        dict_sale = json.dumps(d_sale)

        #loading in json
        quantity = json.loads(dict_q)
        sale = json.loads(dict_sale)

    else:

        # rendering ufm data in graph
        ufm_data = UFMstock.objects.values()
        sale_data = Sale.objects.filter(
            Stock__exact='Un-Finished Material Stock').values()

         # extracting grade and ufm type from filtered data
        d_quantity = dic_key_val.dict(
            dic=ufm_data, key='UFM_type', value='UFM_Quantity')

        # extracting grade and sale type from filtered data
        d_sale = dic_key_val.dict(
            dic=sale_data, key='Sale_Type', value='Sale_Quantity')

        
        dict_q = json.dumps(d_quantity)
        dict_sale = json.dumps(d_sale)
        quantity = json.loads(dict_q)
        sale = json.loads(dict_sale)
        # print(d_sale,'sale')
        # print(d_quantity)

    # rendering all message in notfication modal in reverse order so the new message is always on top
    all_ms = Messages.objects.all().order_by("-id")

    # rendering last 5 messages for dropdown notification in reverse order
    ms = Messages.objects.filter().order_by('-id')[:5]

     # rendering count of all messages
    ms_count = str(Messages.objects.filter(seen__exact='False').count())

    header = 'Un-Finished Material Stock'

    # rendering data in ufm table
    data = UFMstock.objects.all()

    # rendering data in fm table
    data3 = FMstock.objects.all()

    # rendering sales data
    data2 = Sale.objects.filter(Stock__exact='Un-Finished Material Stock')

    # rendering logtable
    log = LogTable.objects.filter(
        Table_name__exact='Un-Finished Material Stock')

    # filters
    UFfilter = UFMFilter(request.GET, queryset=data)
    Ufsale = ufsaleFilter(request.GET, queryset=data2)
    data2 = Ufsale.qs
    data = UFfilter.qs

   # getting users to to check if their access provided by admin
    us = User.objects.get(id=request.user.id)
    rg = Register.objects.get(user=us)
    # context
    d = {'data': data, 'log': log, 'data2': data2, 'header': header, 'ms_count': ms_count, 'ms': ms, 'data3': data3, 'all_ms': all_ms,
         'UFfilter': UFfilter, 'Ufsale': Ufsale, 'quantity': quantity, 'sale': sale, 'd_access': str(rg.delete_access),
         'role': str(rg.userRole)}
    return render(request, 'apex/user_unfinished_material.html', d)



#Finished Material View
@login_required(login_url='login')
def User_Finished_Material(request):
    # geting start and end date from date filters
    
    try:
        startDate = request.GET['start_date']
        endDate = request.GET['end_date']
    except:
        startDate = None
        endDate = None
    if startDate and endDate != None:
        # rendering fm data and sale data from date filters to graph
        fm_data = FMstock.objects.filter(
            FM_Date__gte=startDate, FM_Date__lte=endDate).values()
        sale_data = Sale.objects.filter(
            Stock__exact='Finished Material Stock', Sale_date__gte=startDate, Sale_date__lte=endDate).values()
        
        # extracting quantity and type from filtered data
        d_quantity = dic_key_val.dict(
            dic=fm_data, key='materialType', value='FM_Quantity')
        d_sale = dic_key_val.dict(
            dic=sale_data, key='Sale_Type', value='Sale_Quantity')

        # dumping data in json
        dict_q = json.dumps(d_quantity)
        dict_sale = json.dumps(d_sale)
        
        #loading data in json
        quantity = json.loads(dict_q)
        sale = json.loads(dict_sale)

    else:
        # rendering fm data and sale data in graph
        fm_data = FMstock.objects.values()
        sale_data = Sale.objects.filter(
            Stock__exact='Finished Material Stock').values()

        # extracting quantity and type from filtered data
        d_quantity = dic_key_val.dict(
            dic=fm_data, key='materialType', value='FM_Quantity')
        d_sale = dic_key_val.dict(
            dic=sale_data, key='Sale_Type', value='Sale_Quantity')
        
        #dumps data in json
        dict_q = json.dumps(d_quantity)
        dict_sale = json.dumps(d_sale)
        
        #loads data in json
        quantity = json.loads(dict_q)
        sale = json.loads(dict_sale)

    # rendering all message in notfication modal in reverse order so the new message is always on top
    all_ms = Messages.objects.all().order_by("-id")
    
    # rendering last 5 messages for dropdown notification in reverse order
    ms = Messages.objects.filter().order_by('-id')[:5]
    
    # rendering count of all messages
    ms_count = str(Messages.objects.filter(seen__exact='False').count())
    
    header = 'Finished Material Stock'

    # rendering data in fm table
    data = FMstock.objects.all()

    #rendering rawMaterial data in table
    coil = rawMaterial.objects.all()
    
    #rendering Sale data in table
    data2 = Sale.objects.filter(Stock__exact='Finished Material Stock')
    
    #rendering Logtable 
    log = LogTable.objects.filter(Table_name__exact='Finished Material Stock')
    
    #filters
    fmstockfilter = FMfilter(request.GET, queryset=data)
    fmsale = fsaleFilter(request.GET, queryset=data2)
    data2 = fmsale.qs
    data = fmstockfilter.qs

   # getting users to to check if their access provided by admin
    us = User.objects.get(id=request.user.id)
    rg = Register.objects.get(user=us)

    #context
    d = {'data': data, 'log': log, 'data2': data2, 'fmstockfilter': fmstockfilter, 'header': header, 'coil': coil, 'ms_count': ms_count, 'ms': ms, 'all_ms': all_ms,  'fmstockfilter': fmstockfilter,
         'fmsale': fmsale, 'quantity': quantity, 'sale': sale, 'd_access': str(rg.delete_access),
         'role': str(rg.userRole)}
    return render(request, 'apex/user_finished_material.html', d)

# @unautherized_user

# essential material page view
@login_required(login_url='login')
def User_Essential_Material(request):
    # rendering graphs from filters
    try:
        startDate = request.GET['start_date']
        endDate = request.GET['end_date']
    except:
        startDate = None
        endDate = None

    if startDate and endDate != None:
        # rendering data from date filters to graph
        es = essentialitemStock.objects.filter(
            ES_Date__gte=startDate, ES_Date__lte=endDate).values()
        
        #extracting type and its quantity from es table
        d = dic_key_val.dict(dic=es, key='Type', value='ES_Quantity')
        # dumping in json
        dict = json.dumps(d)

        # loading in json
        cylinder = json.loads(dict)

    else:
        # rendering total es data in graph 
        es = essentialitemStock.objects.values()
        d = dic_key_val.dict(dic=es, key='Type', value='ES_Quantity')
        # dumping json
        dict = json.dumps(d)

        #loading json
        cylinder = json.loads(dict)

    # rendering all message in notfication modal in reverse order so the new message is always on top
    all_ms = Messages.objects.all().order_by("-id")
    
    # rendering last 5 messages for dropdown notification in reverse order
    ms = Messages.objects.filter().order_by('-id')[:5]
    
    # rendering count of all messages
    ms_count = str(Messages.objects.filter(seen__exact='False').count())

    
    header = 'Essential Item Stock'
    
    # rendering es stock data in table
    data = essentialitemStock.objects.all()
    
    # rendering es user per day data in es table
    data2 = EssentialItemUsePerDay.objects.all()

    # rendering es log table
    log = LogTable.objects.filter(Table_name__exact='Essential Item Stock')
    
    # date filters
    emfilter = EMfilter(request.GET, queryset=data)
    usage = usageFilter(request.GET, queryset=data2)
    data2 = usage.qs
    data = emfilter.qs

    # getting users to to check if their access provided by admin
    us = User.objects.get(id=request.user.id)
    rg = Register.objects.get(user=us)

    # context
    d = {'data': data, 'log': log, 'data2': data2, 'header': header, 'ms_count': ms_count, 'ms': ms, 'all_ms': all_ms,  'emfilter': emfilter, 'usage': usage, 'cylinder': cylinder, 'd_access': str(rg.delete_access),
         'role': str(rg.userRole),'room_code':rg.user,'del_access':rg.delete_access,'user_role':rg.userRole}
    return render(request, 'apex/user_essential_material.html', d)


#Delete View
@unautherized_user
def delete(request):
    # checks the request Method
    if request.method == 'POST':
        #getting the inputs values
        id = request.POST.get('sid')
        pi = Register.objects.get(pk=id)
        
        #deleting the user 
        pi.delete()
        # returning in Json if true
        return JsonResponse({'status': 1})
    else:
        # returning in Json if false
        return JsonResponse({'status': 0})


# Notification sending view
def n_send(request):
    # checks the request Method
    if request.method == "POST":
        # getting the inputs values
        name = request.POST['p_name']
        size = request.POST['p_size']
        thickness = request.POST['p_thickness']
        order = request.POST['p_quantity']
        user = User.objects.get(id=request.user.id)
        rs = Register.objects.get(user=user)
        role = rs.userRole
        
        # Check the user is active or not
        if role == 'Active':
            text = "{} sent a notifcation for table: {} Subject: {}, Operation: {}, Reason: {}".format(
                user.username, name, size, thickness, order)
            alertmessages.empty(subject='Notification Alert',
                                text=text, stock_count='')
        else:
            text = "{} sent a notifcation for table: {} Subject: {}, Operation: {}, Reason: {}".format(
                user.username, name, size, thickness, order)
            alertmessages.empty(subject='Request Access',
                                text=text, stock_count='')
        
        # returning in Json 
        return JsonResponse({'status': 'Save'})
    else:
        return JsonResponse({'status': 0})

# this is our login system
@unauthenticated_user
def Login(request):
    if request.method == 'POST':
        u = request.POST['email']
        p = request.POST['password']
        user = authenticate(request, username=u, password=p)

        if user is not None:
            login(request, user)
            register = Register.objects.get(user=user.id)
            status = register.status
            if status == 'Approved':
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You are not approved')

        else:
            messages.error(request, 'Wrong Credentials')
            # print('nothing happend')
    d = {}
    return render(request, 'auth/login.html')

# register page function
def register(request):
    return render(request, 'auth/register.html')

# this function get raw data
def get_rw_grade(request, *args, **kwargs):
    selected_id = kwargs.get('id')
    print(selected_id)
    rw_grade = list(rawMaterial.objects.filter(id=selected_id).values())
    return JsonResponse({'data': rw_grade})

# this functions saves raw data
@unautherized_user
def raw_save(request):
    if request.method == 'GET':

        rw_id_val = list(rawMaterial.objects.values())
        return JsonResponse({'data': rw_id_val})

    if request.method == "POST":
        date = request.POST['r_date']
        # print(date)
        thickness = request.POST['r_thickness']
        size = request.POST['r_size']
        grade = request.POST['r_grade']
        weight = request.POST['r_weight']
        s_weight = request.POST['sc_weight']
        raw_vendor = request.POST['raw_vendor']
        user = User.objects.get(id=request.user.id)
        raw = rawMaterial(register=user, RM_Date=date, RM_Thickness=thickness, RM_Size=size, RM_Grade=grade, RM_coilWeight=weight,
                          RM_scrapWeight=s_weight,Vendor =raw_vendor)
        raw.save()
        raw_save = rawMaterial.objects.values()
        raw_data1 = list(raw_save)
        # print(raw_data1)
        return JsonResponse({'status': 'Save', 'raw_data1': raw_data1})
    else:
        return JsonResponse({'status': 0})

# this function deletes raw data
@del_access
@unautherized_user
def raw_delete(request):
    if request.method == "POST":
        raw_id = request.POST['sid']
        user = User.objects.get(id=request.user.id)
        logsave.logg(regid=user.id, tbid=raw_id,
                     operation='Entry Deleted', tname='Raw Material')
        raw = rawMaterial.objects.get(id=raw_id)
        raw.delete()
        sc = Scrape.objects.get(t_id=raw_id)
        sc.delete()
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})

# this function saves unfinished material data not getting used for now
@unautherized_user
def uf_save(request):
    if request.method == 'POST':
        date = request.POST['uf_date']
        fmid = request.POST['f_id']
        print(fmid, 'fmid')
        weight = request.POST['uf_weight']
        quantity = request.POST['uf_quantity']
        fm_id = FMstock.objects.get(id=fmid)
        print(fm_id, 'fm_id')
        user = User.objects.get(id=request.user.id)
        uf = UFMstock(UFM_date=date, UFM_Weight=weight,
                      UFM_Quantity=quantity, register=user, FMid=fm_id)
        uf.save()
        # print('error')
        uf_val = UFMstock.objects.values()
        uf_data = list(uf_val)
        return JsonResponse({'status': 'Save', 'uf_data': uf_data})
    else:
        return JsonResponse({'Status': 0})

# this function deletes unfinished material data
@del_access
@unautherized_user
def uf_delete(request):
    if request.method == "POST":
        uf_id = request.POST['sid']
        user = User.objects.get(id=request.user.id)
        logsave.logg(regid=user.id, tbid=uf_id, operation='Entry Deleted',
                     tname='Un-Finished Material Stock')
        uf = UFMstock.objects.get(id=uf_id)
        uf.delete()
        # sc = Scrape.objects.get(t_id=uf_id)
        # sc.delete()

        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})

# this function saves finished material data
@unautherized_user
def fm_save(request):
    # if request.method =='GET':
    #     rm_val = rawMaterial.objects
    if request.method == 'POST':
        rm_id = request.POST['raw_id']
        rm_size = request.POST['raw_size']
        date = request.POST['fmat_date']
        rm_grade = request.POST['raw_grade']
        rm_weight = request.POST['raw_weight']
        fm_type = request.POST['fmat_type']
        fm_thickness = request.POST['fmat_thickness']
        fm_size = request.POST['fmat_size']
        fm_weight = request.POST['fmat_weight']
        fm_quantity = request.POST['fmat_quantity']
        fm_scrape = request.POST['fmat_scrape']
        uf_thickness = request.POST['uf_thickness']
        uf_size = request.POST['uf_size']
        uf_weight = request.POST['uf_weight']
        uf_quantity = request.POST['uf_quantity']
        rm = rawMaterial.objects.get(id=rm_id)

        rw = rawMaterial.objects.filter(id__exact=rm_id)
        rw_data = rw.values()
        rw_dic = rw_data[0]
        rw_weight = int(rw_dic['RM_coilWeight'])

        if rw_weight < int(rm_weight):
            return JsonResponse({'status': 1})
            # messages.info(request,'Not Enough Weight in Raw Material')

        else:
            user = User.objects.get(id=request.user.id)
            fm = FMstock(UF_Weight=uf_weight, coilUID=rm, Size=rm_size, FM_Date=date, Grade=rm_grade, coilWeight=rm_weight, materialType=fm_type,
                         FM_Thickness=fm_thickness, FM_Size=fm_size, FM_Weight=fm_weight, FM_Quantity=fm_quantity, FM_scrapWeight=fm_scrape,
                         UF_Thickness=uf_thickness, UF_Size=uf_size, UF_Quantity=uf_quantity, register=user)

            fm.save()
            fm_val = FMstock.objects.values()
            fm_data = list(fm_val)
            return JsonResponse({'status': 'Save', 'fm_data': fm_data})

    else:
        return JsonResponse({'status': 0})

# this function deletes finished material data
@del_access
@unautherized_user
def fm_delete(request):
    try:
        if request.method == "POST":
            uf_id = request.POST['sid']
            uf = FMstock.objects.get(id=uf_id)
            user = User.objects.get(id=request.user.id)
            logsave.logg(regid=user.id, tbid=uf_id,
                         operation='Entry Deleted', tname='Finished Material Stock')
            uf.delete()
            sc = Scrape.objects.get(t_id = uf_id)
            sc.delete()
            return JsonResponse({'status': 1})
    except:
        return JsonResponse({'status': 0})

# this function gets rm id to fm page
def get_s_type(request, *args, **kwargs):
    selected_id = kwargs.get('id')
    print(selected_id)
    s_type = list(FMstock.objects.filter(id=selected_id).values())
    print(s_type, 'ajax values')
    return JsonResponse({'data': s_type})

# this function saves finsihed material data
@unautherized_user
def sale_save(request):
    if request.method == 'GET':
        # rw_id_val = list(rawMaterial.objects.values())
        # return JsonResponse({'data':rw_id_val})
        s_id_val = list(FMstock.objects.values())
        return JsonResponse({'data': s_id_val})
    try:
        if request.method == "POST":

            fm_id = request.POST['fmsales_id']
            date = request.POST['sales_date']
            sales_quantity = request.POST['sales_quantity']
            sales_weight = request.POST['sales_weight']
            sale_type = request.POST['s_m_type']
            sale_sold = request.POST['sale_sold']
            fmcoil = FMstock.objects.get(id=fm_id)

            fm = FMstock.objects.filter(id__exact=fm_id)
            fm_data = fm.values()
            fm_dic = fm_data[0]
            fm_weight = int(fm_dic['FM_Weight'])
            fm_quantity = int(fm_dic['FM_Quantity'])

            if fm_weight < int(sales_weight):
                return JsonResponse({'status': 1})
                print('not enough weight in stock')
            elif fm_quantity < int(sales_quantity):
                return JsonResponse({'status': 2})
                print('not enough quantity in stock')

            else:
                # print(fmcoil,date,fm_id,sales_quantity,sales_weight)
                user = User.objects.get(id=request.user.id)
                sale = Sale(register=user, FMcoilUID=fmcoil, Sale_date=date, Sale_Weight=sales_weight,
                            Sale_Quantity=sales_quantity, Stock='Finished Material Stock', Sale_Type=sale_type,To =sale_sold)

                sale.save()
                sale_val = Sale.objects.filter(
                    Stock__exact='Finished Material Stock').values()
                sale_data = list(sale_val)
                # print(sale_data,'sale data')
                return JsonResponse({'status': 'Save', 'sale_data': sale_data})
    except:
        return JsonResponse({'status': 0})

# this function deletes unfinished material data
@del_access
@unautherized_user
def sale_delete(request):
    try:
        if request.method == "POST":
            uf_id = request.POST['sid']
            user = User.objects.get(id=request.user.id)
            logsave.logg(regid=user.id, tbid=uf_id,
                         operation='Sales Entry Deleted', tname='Finished Material Stock')
            uf = Sale.objects.get(id=uf_id)
            uf.delete()

            return JsonResponse({'status': 1})
    except:
        return JsonResponse({'status': 0})

#this function gets ufm id to ufm sale
def get_us_type(request, *args, **kwargs):
    selected_id = kwargs.get('id')
    print(selected_id)
    us_type = list(UFMstock.objects.filter(id=selected_id).values())
    # print(s_type,'ajax values')
    return JsonResponse({'data': us_type})

# this function saves unfinished sale data
@unautherized_user
def usale_save(request):
    if request.method == 'GET':
        # rw_id_val = list(rawMaterial.objects.values())
        # return JsonResponse({'data':rw_id_val})
        us_id_val = list(UFMstock.objects.values())
        return JsonResponse({'data': us_id_val})
    try:
        if request.method == "POST":
            us_m_type = request.POST['us_m_type']
            ufm_id = request.POST['ufmsales_id']
            date = request.POST['sales_date']
            sales_quantity = request.POST['sales_quantity']
            sales_weight = request.POST['sales_weight']
            sale_sold = request.POST['usale_sold']

            ufmcoil = UFMstock.objects.get(id=ufm_id)

            uf = UFMstock.objects.filter(id__exact=ufm_id)
            uf_data = uf.values()
            uf_dic = uf_data[0]
            uf_weight = int(uf_dic['UFM_Weight'])
            uf_quantity = int(uf_dic['UFM_Quantity'])

            if uf_weight < int(sales_weight):
                return JsonResponse({'status': 1})
                print('not enough weight in stock')
            elif uf_quantity < int(sales_quantity):
                return JsonResponse({'status': 2})
                print('not enough quantity in stock')
            else:
                # print(ufmcoil,date,fm_id,sales_quantity,sales_weight)
                user = User.objects.get(id=request.user.id)
                sale = Sale(register=user, UFcoilID=ufmcoil, Sale_date=date, Sale_Weight=sales_weight,
                            Sale_Quantity=sales_quantity, Stock='Un-Finished Material Stock', Sale_Type=us_m_type,To =sale_sold)

                sale.save()
                sale_val = Sale.objects.filter(
                    Stock__exact='Un-Finished Material Stock').values()
                sale_data = list(sale_val)
                # print(sale_data,'sale data')
                return JsonResponse({'status': 'Save', 'sale_data': sale_data})
    except:
        return JsonResponse({'status': 0})

# this function deletes unfinished sales data
@del_access
@unautherized_user
def usale_delete(request):
    try:
        if request.method == "POST":
            uf_id = request.POST['sid']
            user = User.objects.get(id=request.user.id)
            logsave.logg(regid=user.id, tbid=uf_id, operation='Sales Entry Deleted',
                         tname='Un-Finished Material Stock')
            uf = Sale.objects.get(id=uf_id)
            uf.delete()

            return JsonResponse({'status': 1})
    except:
        return JsonResponse({'status': 0})

# this function saves essential material data
@unautherized_user
def es_save(request):
    try:
        if request.method == "POST":
            date = request.POST['es_date']
            type = request.POST['es_type']
            quantity = request.POST['es_quantity']
            size = request.POST['es_size']
            user = User.objects.get(id=request.user.id)
            es = essentialitemStock(
                Type=type, ES_Quantity=quantity, ES_Size=size, ES_Date=date, register=user)
            es.save()
            es_val = essentialitemStock.objects.values()
            es_data = list(es_val)
            return JsonResponse({'status': 'Save', 'es_data': es_data})

    except:
        return JsonResponse({'status': 0})

# this function deletes essentiol material data
@del_access
@unautherized_user
def es_delete(request):
    try:
        if request.method == "POST":
            uf_id = request.POST['sid']
            uf = essentialitemStock.objects.get(id=uf_id)
            user = User.objects.get(id=request.user.id)
            logsave.logg(regid=user.id, tbid=uf_id,
                         operation='Entry Deleted', tname='Essential Item Stock')
            uf.delete()

            return JsonResponse({'status': 1})
    except:
        return JsonResponse({'status': 0})

# this function gets es id to user per day 
def get_es_type(request, *args, **kwargs):
    selected_id = kwargs.get('id')
    print(selected_id)
    es_type = list(essentialitemStock.objects.filter(id=selected_id).values())
    return JsonResponse({'data': es_type})

# this functions saves use per day data
@unautherized_user
def upd_save(request):
    if request.method == 'GET':
        # rw_id_val = list(rawMaterial.objects.values())
        # return JsonResponse({'data':rw_id_val})
        es_id_val = list(essentialitemStock.objects.values())
        return JsonResponse({'data': es_id_val})

    try:
        if request.method == "POST":
            date = request.POST['upd_date']
            type = request.POST['upd_type']
            quantity = request.POST['upd_quantity']
            size = request.POST['upd_size']
            id = request.POST['upd_id']
            es_id = essentialitemStock.objects.get(id=id)

            upd = essentialitemStock.objects.filter(id__exact=id)
            es_data = upd.values()
            es_dic = es_data[0]
            # es_size = int(es_dic['EPD_Size'])
            es_quantity = int(es_dic['ES_Quantity'])

            if es_quantity < int(quantity):
                return JsonResponse({"status": 1})
                print('not enough quantity in stock')

            user = User.objects.get(id=request.user.id)
            upd = EssentialItemUsePerDay(
                EPD_UID=es_id, EPD_Type=type, EPD_Quantity=quantity, EPD_Size=size, EPD_Date=date, register=user)
            upd.save()
            upd_val = EssentialItemUsePerDay.objects.values()
            es_val = essentialitemStock.objects.values()
            e_data = list(es_val)
            upd_data = list(upd_val)
            return JsonResponse({'status': 'Save', 'upd_data': upd_data, 'e_data': e_data})

    except:
        return JsonResponse({'status': 0})

# this function deletes upd data(use per day data)
@del_access
@unautherized_user
def upd_delete(request):
    try:
        if request.method == "POST":
            uf_id = request.POST['sid']
            uf = EssentialItemUsePerDay.objects.get(id=uf_id)
            user = User.objects.get(id=request.user.id)
            logsave.logg(regid=user.id, tbid=uf_id,
                         operation='Entry Deleted', tname='Essential Item Stock')
            uf.delete()

            return JsonResponse({'status': 1})
    except:
        return JsonResponse({'status': 0})

# this function updates user page info
@unautherized_user
def user_save(request):
    try:
        if request.method == "POST":
            id = request.POST['u_id']
            fname = request.POST['first_name']
            lname = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            # print(id, fname, lname, email, password)
            user = User.objects.get(id=request.user.id)
            rg = Register.objects.get(user=user)
            user.set_password(password)
            user.first_name = fname
            user.last_name = lname
            user.email = email
            rg.First_Name = fname
            rg.Last_Name = lname
            rg.UserName = email
            rg.save()
            user.save()
            print(rg)
            return JsonResponse({'status': 'Save'})
    except:
        return JsonResponse({'status': 0})

# this function updates data
@unautherized_user
def user_delete(request):
    try:
        if request.method == "POST":
            id = request.POST['sid']
            # user = User.objects.get()
            reg = Register.objects.get(id=id)
            us = reg.UserName
            user = User.objects.get(username=us)
            reg.delete()
            user.delete()

            return JsonResponse({'status': 1})
    except:
        return JsonResponse({'status': 0})

# this is our logout data
def Logout(request):
    logout(request)
    return redirect('login')

#this function saves register page info
@unauthenticated_user
def register(request):
    if request.method == 'POST':
        fname = request.POST['f_name']
        lname = request.POST['l_name']
        email = request.POST['email']
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            if User.objects.filter(username=email).exists():
                messages.error(request, 'That username is taken')
                print("Email exists")
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=email, password=password2, first_name=fname, last_name=lname)
                Register.objects.create(
                    user=user, First_Name=fname, Last_Name=lname, UserName=email, delete_access='False')
                user.save()

                # ms.stock_count = ''
                alertmessages.empty(subject='Account Created',
                                    text=email, stock_count='')
                # print('You are now registered and can log in')
                messages.success(
                    request, 'You are now registered and can log in')
                return redirect('login')
        else:
            messages.error(request, 'Error!, Passwords do not match')
            return redirect('register')
    return render(request, 'auth/register.html')

# this function save timmer info
@unautherized_user
def save_timmer(request):
    try:
        if request.method == "POST":
            a_time = request.POST['ac_time']
            d_time = request.POST['dc_time']
            t = Timmer.objects.create()
            t.active_time = a_time
            t.inactive_time = d_time
            t.save()
            t_val = Timmer.objects.values()
            timmer_data = list(t_val)
            return JsonResponse({'status': 'Save', 'timmer_data': timmer_data})
    except:
        return JsonResponse({'status': 0})

# this function save role/stauts/delete access data
def p_user(request):
    try:
        if request.method == "POST":
            role = request.POST['rl']
            status = request.POST['st']
            del_access = request.POST['del_access']
            id = request.POST['sid']
            rg = Register.objects.get(id=id)
            rg.status = status
            rg.userRole = role
            rg.delete_access = del_access
            # n = Notification.objects.create()
            # n.register = rg.user
            # n.text = 'Delete Access {} Current access {}'.format(del_access,role)
            # n.save()
            rg.save()
            print(rg)
            return JsonResponse({"status": 'Save'})
    except:
        return JsonResponse({"status": 0})

# this is our notification alert system
def noti_alert(request):
    try:
        # if request.method == 'POST':
        b = request.GET['button']
        if b == 'clicked':
            msg = Messages.objects.values()
            for i in msg:
                id = i['id']
                m = Messages.objects.get(id=id)
                m.seen = 'True'
                m.save()
        return JsonResponse({'status': 'Save'})
    except:
        return JsonResponse({'status': 0})
