from .models import Note
from .forms import NoteForm
import datetime
from tickets.forms import SearchForm
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from authentication.models import User
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

@login_required(login_url='/accounts/login/')
def note_list(request):
    if request.user.role < 3:

        notes = Note.objects.all()
        form_fields = {}
        form_fields['text'] = ''
        form_fields['user'] = ''
        start_date = datetime.datetime.now() - datetime.timedelta(60)
        end_date = datetime.datetime.now() + datetime.timedelta(60)

        form = SearchForm(request.GET or None, request.FILES or None, initial=form_fields)
        return render(request, 'note_list.html', {'title':'Lista note', 'notes': notes, 'form': form, 'start_date': start_date.strftime('%d/%m/%Y'), 'end_date': end_date.strftime('%d/%m/%Y')})
    return HttpResponseRedirect('/dashboard')

@login_required(login_url='/accounts/login/')
def save_note(request):
    assigned_to = request.POST.get('assigned_to', '')
    print('ASSIGNED TO: '+assigned_to)
    txt = request.POST.get('note', '')
    print('NOTE: '+txt)
    user_created_by = request.POST.get('user', '')
    print('USER: '+user_created_by)
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')

    note = Note()
    first_name = assigned_to.split()[0]
    last_name = assigned_to.split()[1]
    user_assigned = User.objects.get(first_name=first_name, last_name=last_name)
    note.assigned_to = user_assigned
    note.note = txt
    note.created_by = User.objects.get(pk=user_created_by)
    note.start_date = start_date
    note.end_date = end_date
    note.save()

    return JsonResponse({'success': True})

@login_required(login_url='/accounts/login/')
def note(request, id):
    if request.user.role < 3:
        note = Note.objects.get(pk=id)
        return render(request, 'note.html', {'title':'Nota', 'note':note,})
    return HttpResponseRedirect('/dashboard')

@login_required(login_url='/accounts/login/')
def note_edit(request, id):
    if request.user.role < 3:

        note = Note.objects.get(pk=id)
        form_fields = {}
        form_fields['assigned_to'] = note.assigned_to
        form_fields['note'] = note.note
        form_fields['created_by'] = note.created_by
        form_fields['start_date'] = note.start_date
        form_fields['end_date'] = note.end_date


        form = NoteForm(request.POST or None, request.FILES or None, initial=form_fields)
        if form.is_valid():
            form.save()

        return render(request, 'note_edit.html', {'title':'Modifica nota', 'form': form, 'note': note})
    return HttpResponseRedirect('/dashboard')


@login_required(login_url='/accounts/login/')
def save_mod_note(request):
    assigned_to = request.POST.get('assigned_to', '')
    user_assigned = User.objects.get(pk=assigned_to)
    print('ASSIGNED TO: '+assigned_to)

    txt = request.POST.get('note', '')
    print('NOTE: '+txt)

    user_created_by_pk = request.POST.get('created_by', '')
    user_created_by = User.objects.get(pk=user_created_by_pk)
    print('USER: '+str(user_created_by))

    id = request.POST.get('id', '')
    print('ID: '+id)

    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')

    note = Note.objects.get(pk=id)
    note.assigned_to = user_assigned
    note.note = txt
    note.created_by = user_created_by
    note.start_date = start_date
    note.end_date = end_date
    note.save()

    return HttpResponseRedirect('/nota/'+id)


@login_required(login_url='/accounts/login/')
def delete_note(request):
    if request.user.role < 3:

        user_created_by_pk = request.POST.get('user', '')
        user_created_by = User.objects.get(pk=user_created_by_pk)
        print('USER: '+str(user_created_by))

        id = request.POST.get('pk', '')
        print('ID: '+id)

        note = Note.objects.get(pk=id)
        note.delete()

        return JsonResponse({'success': True})
    return HttpResponseRedirect('/dashboard')


@login_required(login_url='/accounts/login/')
def search_notes(request):
    form_fields = {}
    form_fields['text'] = ''
    form_fields['user'] = ''
    form = SearchForm(request.GET or None, request.FILES or None, initial=form_fields)


    text = request.GET.get('text','')
    userpk = request.GET.get('user', '')
    date = request.GET.get('date', '')

    notequeryset = Q()

    if text:
        print("TEXT: " +text)
        notequeryset &= (Q(note__icontains=text))

    if userpk:
        user = User.objects.get(pk=userpk)
        print(user)
        notequeryset &= (Q(assigned_to=user))

    if date:
        start_date = datetime.datetime.strptime(date.split(' - ')[0], '%m/%d/%Y')
        end_date = datetime.datetime.strptime(date.split(' - ')[1], '%m/%d/%Y')
        notequeryset &= (
        Q(start_date__gte=start_date)&
        Q(start_date__lte=end_date)
        )


    notes = Note.objects.filter(notequeryset).distinct()
    # for ticket in tickets:
    #     print(ticket)

    return render(request, 'note_list.html', {'title':'Lista note', 'notes': notes, 'form': form})
