from django import forms

# ─── Legal Scenario Input ────────────────────────────────────────────────────────

class ScenarioForm(forms.Form):
    scenario = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your legal scenario…'}),
        label="Describe the legal scenario"
    )


# ─── Contract & Transactional Drafting ───────────────────────────────────────────

# yourapp/forms.py
from django import forms

# ─── NDA ─────────────────────────────────────────────────────────────────────────

class NDAForm(forms.Form):
    party_a        = forms.CharField(
        label="Disclosing Party",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Acme Corp'})
    )
    party_b        = forms.CharField(
        label="Receiving Party",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Beta LLC'})
    )
    effective_date = forms.DateField(
        label="Effective Date",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    term           = forms.CharField(
        label="Term / Duration",
        max_length=50,
        help_text="e.g. 2 years"
    )
    exclusions     = forms.CharField(
        label="Additional Exclusions",
        required=False,
        widget=forms.Textarea(attrs={'rows':2}),
        help_text="What to exclude from confidentiality"
    )


# ─── Sale of Goods ───────────────────────────────────────────────────────────────

class SaleForm(forms.Form):
    party_a        = forms.CharField(
        label="Seller",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Acme Suppliers'})
    )
    party_b        = forms.CharField(
        label="Buyer",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Retail Co.'})
    )
    effective_date = forms.DateField(
        label="Effective Date",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    term           = forms.CharField(
        label="Purchase Price",
        max_length=50,
        help_text="e.g. USD 10,000"
    )
    delivery_terms = forms.CharField(
        label="Delivery Terms",
        widget=forms.Textarea(attrs={'rows':2}),
        help_text="e.g. Cost Insurance Freight port of entry"
    )


# ─── Lease Agreement ────────────────────────────────────────────────────────────

class LeaseForm(forms.Form):
    party_a          = forms.CharField(
        label="Lessor",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Landlord Ltd.'})
    )
    party_b          = forms.CharField(
        label="Lessee",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Tenant Inc.'})
    )
    effective_date   = forms.DateField(
        label="Effective Date",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    term             = forms.CharField(
        label="Lease Term",
        max_length=50,
        help_text="e.g. 12 months"
    )
    property_desc    = forms.CharField(
        label="Property Description",
        widget=forms.Textarea(attrs={'rows':3}),
        help_text="Full address and unit details"
    )
    rent_amount      = forms.DecimalField(
        label="Rent Amount",
        max_digits=12,
        decimal_places=2,
        help_text="e.g. 1500.00"
    )
    security_deposit = forms.DecimalField(
        label="Security Deposit",
        max_digits=12,
        decimal_places=2,
        required=False,
        help_text="Optional: held against damage"
    )


# ─── Employment Contract ────────────────────────────────────────────────────────

# core/forms.py

from django import forms

class EmploymentForm(forms.Form):
    party_a = forms.CharField(
        label="Employer Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'ABC (Pty) Ltd',
        })
    )
    party_b = forms.CharField(
        label="Employee Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'John Doe',
        })
    )
    effective_date = forms.DateField(
        label="Effective Date",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    position = forms.CharField(
        label="Position / Title",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Software Engineer'})
    )
    compensation = forms.CharField(
        label="Compensation",
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'USD 5,000 per month'})
    )
    benefits = forms.CharField(
        label="Benefits (comma‑separated)",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Health insurance, pension'})
    )
    notice_period = forms.CharField(
        label="Notice Period",
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': '1 month'})
    )
    non_compete = forms.BooleanField(
        label="Include Non‑Compete Clause?", required=False
    )
    non_compete_term = forms.CharField(
        label="Non‑Compete Duration",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '6 months'})
    )
    dispute_resolution = forms.CharField(
        label="Dispute Resolution",
        initial="Arbitration under LCIA Rules in Lusaka",
        widget=forms.TextInput()
    )


# ─── Wills & Estate Planning ─────────────────────────────────────────────────────

from django import forms

class WillForm(forms.Form):
    testator_name = forms.CharField(
        label="Testator’s Full Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-200 focus:outline-none',
            'placeholder': 'John Doe'
        })
    )
    executor_name = forms.CharField(
        label="Executor’s Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-md focus:ring-indigo-200 focus:outline-none',
            'placeholder': 'Jane Smith'
        })
    )
    residuary = forms.CharField(
        label="Residuary Clause (what happens to the rest)",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full p-2 h-20 border border-gray-300 rounded-md focus:ring-indigo-200 focus:outline-none',
            'placeholder': 'E.g. The rest of my estate to be divided equally among my children'
        })
    )
    special_requests = forms.CharField(
        label="Special requests (guardianship, funeral wishes, etc.)",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full p-2 h-20 border border-gray-300 rounded-md focus:ring-indigo-200 focus:outline-none',
            'placeholder': 'E.g. I wish for a simple funeral service'
        })
    )



# ─── Petitions & Court Documents ─────────────────────────────────────────────────

class PetitionForm(forms.Form):
    petitioner_name        = forms.CharField(label="Petitioner’s Name", max_length=200)
    respondent_name        = forms.CharField(label="Respondent’s Name", max_length=200)
    court                  = forms.CharField(label="Court (e.g. High Court of Zambia)", max_length=200)
    jurisdiction           = forms.CharField(
        label="Jurisdictional Basis",
        widget=forms.Textarea(attrs={'rows':2}),
        help_text="On what constitutional or statutory ground this court has jurisdiction"
    )
    facts                  = forms.CharField(
        widget=forms.Textarea(attrs={'rows':4}),
        label="Factual Background"
    )
    legal_basis            = forms.CharField(
        widget=forms.Textarea(attrs={'rows':4}),
        label="Legal Basis / Grounds"
    )
    supporting_authorities = forms.CharField(
        widget=forms.Textarea(attrs={'rows':3}),
        required=False,
        label="Supporting Authorities (cases, statutes)"
    )
    relief_sought          = forms.CharField(
        widget=forms.Textarea(attrs={'rows':3}),
        label="Relief Sought"
    )
