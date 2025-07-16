def build_petition_prompt(data):
    return f"""
You are a seasoned Zambian litigator. Draft a PETITION to the {data['court']}.

Petitioner: {data['petitioner_name']}
Respondent: {data['respondent_name']}

I. Jurisdiction & Venue  
State why {data['court']} has jurisdiction.

II. Facts  
{data['facts']}

III. Legal Basis / Grounds  
{data['legal_basis']}

IV. Supporting Authorities  
{data.get('supporting_authorities','None provided')}

V. Relief Sought  
{data['relief_sought']}

Structure as a formal petition:
- Title/Cause
- Parties & Capacity
- Jurisdiction
- Statement of Facts
- Grounds
- Prayer for Relief
- Signature Block
Use formal petition language, cite Constitution or statutes, and number each paragraph.
"""
