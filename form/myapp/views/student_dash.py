from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

def stu_dashboar(request)