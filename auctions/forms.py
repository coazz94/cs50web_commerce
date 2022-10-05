form django import forms


class NewPageForm(forms.Form):
    pagename = forms.CharField(label="", required = True, 
    widget= forms.Textarea
    (attrs={'placeholder':'Enter Title','value':'TEst','class':'col-lg-4','style':'margin-top:1rem;height:2rem'}))


    content = forms.CharField(label="",required= True,
    widget= forms.Textarea
    (attrs={'placeholder':'Enter markdown content','class':'col-lg-5','style':'top:1rem;height:40%'}))

