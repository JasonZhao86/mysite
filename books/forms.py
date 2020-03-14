from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=3)
    email = forms.EmailField(required=False, label="邮箱地址")
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        message = self.cleaned_data["message"]
        words = len(message.split())
        if words > 4:
            raise forms.ValidationError("不得多于4个单词")
        return self.cleaned_data