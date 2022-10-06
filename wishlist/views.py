from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render
from wishlist.models import BarangWishlist
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('wishlist:login')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # melakukan login terlebih dahulu
            response = HttpResponseRedirect(
                reverse("wishlist:show_wishlist"))  # membuat response
            # membuat cookie last_login dan menambahkannya ke dalam response
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)


def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('wishlist:login'))
    response.delete_cookie('last_login')
    return response


@login_required(login_url='/wishlist/login/')
def show_wishlist(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
        'list_barang': data_barang_wishlist,
        'nama': 'Muhammad Vicky Maulana',
        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "wishlist.html", context)


@login_required(login_url='/wishlist/login/')
def show_wishlist_ajax(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
        'nama': 'Muhammad Vicky Maulana',
        'last_login': request.COOKIES['last_login'],
        'logged_in': request.user.is_authenticated,
    }
    return render(request, "wishlist_ajax.html", context)


@login_required(login_url='/wishlist/login/')
def submit_ajax(request):
    if request.method == 'POST':
        nama_barang = request.POST.get('nama_barang')
        harga_barang = request.POST.get('harga_barang')
        deskripsi = request.POST.get('deskripsi')
        BarangWishlist.objects.create(
            nama_barang=nama_barang,
            harga_barang=harga_barang,
            deskripsi=deskripsi,
        )
        return HttpResponseRedirect('/wishlist/ajax/')
    return HttpResponse('Data gagal disimpan')


def show_xml(request):
    # menyimpan hasil query dari seluruh data yang ada pada BarangwishList
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")


def show_json(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_json_by_id(request, id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def show_xml_by_id(request, id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
