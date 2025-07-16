def build_will_prompt(data):
    return f"""
You are an expert Zambian estate lawyer. Draft a clear, legally enforceable LAST WILL AND TESTAMENT.

Testator: {data['testator_name']}
Beneficiaries:
{data['beneficiaries']}

Executor: {data['executor_name']}
Residuary Clause:
{data.get('residuary','Not specified')}

Special Requests:
{data.get('special_requests','None')}

Structure:
1. Heading & Declaration
2. Appointment of Executor
3. Gifts to Beneficiaries
4. Residuary Clause
5. Funeral Wishes
6. Signatures & Witnesses

Use plain precise language, cite relevant Zambian Wills Act provisions by section number, and ensure formal execution language.
"""
