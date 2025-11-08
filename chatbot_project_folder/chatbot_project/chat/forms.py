from django import forms
from django.shortcuts import render, redirect
class MessageForm(forms.Form):
    message = forms.CharField(max_length=500, widget=forms.TextInput(attrs={
        'placeholder': 'Ask Dave anything...'
    }))


def chat_view(request):
    global current_question

    form = MessageForm()  # <-- always create form first

    if request.method == 'POST':

        # Clear chat button
        if 'clear' in request.POST:
            Message.objects.all().delete()
            current_question = None
            return redirect('chat')

        # Send button
        if 'send' in request.POST:
            form = MessageForm(request.POST)  # bind POST data
            if form.is_valid():
                user_message = form.cleaned_data['message']
                Message.objects.create(sender='User', text=user_message)

                bot_message = generate_bot_response(user_message)
                Message.objects.create(sender='Dave', text=bot_message)

                return redirect('chat')

    # Fetch all messages
    messages = Message.objects.all().order_by('timestamp')
    return render(request, 'chat/chat.html', {'messages': messages, 'form': form})
