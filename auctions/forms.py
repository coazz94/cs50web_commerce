from django import forms




class CreateListing(forms.Form):

    title = forms.CharField(label="", required = True, 
    widget= forms.Textarea
    (attrs={'placeholder':'Title','value':'Test','style':'margin-top:20px;height:2rem'}))

    description = forms.CharField(label="",required= True,
    widget= forms.Textarea
    (attrs={'placeholder':'Description','style':'margin-top:2px;height:10rem'}))

    price = forms.DecimalField(label="",required= True, decimal_places=2, max_value=10000, min_value=0.1,
    widget= forms.NumberInput
    (attrs={'placeholder':'price','style':'margin-top:2px;height:2rem'}))

    url = forms.CharField(label="",required= True,
    widget= forms.URLInput
    (attrs={'placeholder':'url','style':'margin-top:2px;height:2rem'}))

    #image = forms.CharField(label="",required= True,
    #widget= forms.Textarea
    #(attrs={'placeholder':'Description','style':'margin-top:1rem;height:10rem'}))

"""
            name
            description
            image
            url
            price 
"""