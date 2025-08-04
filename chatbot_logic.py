import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Global dictionary to store conversation states for different sessions
conversations = {}

def get_conversation_state(session_id: str) -> Dict:
    """Get or initialize conversation state for a session"""
    if session_id not in conversations:
        conversations[session_id] = {
            'step': 'start',
            'user_data': {},
            'context': {}
        }
    return conversations[session_id]

def update_conversation_state(session_id: str, step: str, user_data: Dict = None, context: Dict = None):
    """Update conversation state"""
    state = get_conversation_state(session_id)
    state['step'] = step
    if user_data:
        state['user_data'].update(user_data)
    if context:
        state['context'].update(context)

def extract_keywords(message: str) -> List[str]:
    """Extract and normalize keywords from user message"""
    message = message.lower().strip()
    # Remove punctuation and split into words
    words = re.findall(r'\b\w+\b', message)
    return words

def contains_keywords(message: str, keywords: List[str]) -> bool:
    """Check if message contains any of the specified keywords"""
    message_words = extract_keywords(message)
    return any(keyword.lower() in message_words for keyword in keywords)

def process_chat_message(message: str, session_id: str) -> Tuple[str, Optional[List[str]]]:
    """
    Main function to process chat messages based on the ITR filing flowchart
    Returns (response_message, quick_options)
    """
    state = get_conversation_state(session_id)
    current_step = state['step']
    user_data = state['user_data']
    
    # Handle global commands first
    if contains_keywords(message, ['start over', 'restart', 'reset']):
        update_conversation_state(session_id, 'start', {}, {})
        return "Let's start fresh! Are you ready to begin your ITR filing process?", ['yes', 'help', 'which itr form']
    
    if contains_keywords(message, ['help', 'support', 'assistance']):
        help_text = """
        I can help you with ITR filing! Here's what I can assist you with:
        
        📋 **ITR Form Selection**: Find the right ITR form based on your income sources
        📄 **Document Checklist**: Get a list of required documents
        💰 **Tax Calculation**: Calculate your tax liability
        🔗 **Aadhaar Linking**: Guide you through PAN-Aadhaar linking
        📊 **Filing Process**: Step-by-step filing assistance
        
        Just tell me what you need help with!
        """
        return help_text, ['start filing', 'which itr form', 'document checklist', 'tax calculation']
    
    # Start of the flowchart - Entry point
    if current_step == 'start':
        if contains_keywords(message, ['start', 'begin', 'file', 'filing', 'yes', 'proceed']):
            update_conversation_state(session_id, 'check_aadhaar_link')
            return "Great! Let's begin your ITR filing process. First, I need to verify - Is your Aadhaar linked with your PAN?", ['yes', 'no', 'not sure']
        
        elif contains_keywords(message, ['which', 'itr', 'form', 'type']):
            return get_itr_form_guide(), ['start filing', 'more info', 'help']
        
        else:
            return "Welcome to ITR Filing Assistant! I'll help you file your Income Tax Return step by step. Ready to start?", ['start filing', 'help', 'which itr form']
    
    # Check Aadhaar-PAN linking
    elif current_step == 'check_aadhaar_link':
        if contains_keywords(message, ['yes', 'linked', 'done', 'completed']):
            update_conversation_state(session_id, 'select_filer_type')
            return "Perfect! Your Aadhaar is linked with PAN. Now, let me identify what type of filer you are. Are you an Individual taxpayer?", ['individual', 'company', 'professional', 'other entity']
        
        elif contains_keywords(message, ['no', 'not linked', 'unlinked']):
            update_conversation_state(session_id, 'guide_aadhaar_linking')
            return get_aadhaar_linking_guide(), ['done linking', 'need help', 'continue anyway']
        
        elif contains_keywords(message, ['not sure', 'dont know', 'unsure', 'check']):
            return """
            You can check if your Aadhaar is linked with PAN by:
            
            🌐 **Online**: Visit the Income Tax e-filing portal
            📱 **SMS**: Send SMS to 567678 or 56161
            📞 **Call**: Contact IT helpdesk at 1800-103-0025
            
            Is your Aadhaar linked with PAN?
            """, ['yes', 'no', 'will check later']
        
        else:
            return "I need to know about your Aadhaar-PAN linking status to proceed. Is your Aadhaar linked with your PAN?", ['yes', 'no', 'not sure']
    
    # Guide for Aadhaar linking
    elif current_step == 'guide_aadhaar_linking':
        if contains_keywords(message, ['done', 'linked', 'completed']):
            update_conversation_state(session_id, 'select_filer_type')
            return "Excellent! Now that your Aadhaar is linked, let's proceed. What type of filer are you?", ['individual', 'company', 'professional', 'other entity']
        
        elif contains_keywords(message, ['continue', 'anyway', 'proceed']):
            update_conversation_state(session_id, 'select_filer_type')
            return "I recommend linking Aadhaar with PAN for smooth processing, but let's continue. What type of filer are you?", ['individual', 'company', 'professional', 'other entity']
        
        else:
            return get_aadhaar_linking_guide(), ['done linking', 'continue anyway', 'need help']
    
    # Select filer type
    elif current_step == 'select_filer_type':
        if contains_keywords(message, ['individual', 'person', 'salaried', 'employee']):
            update_conversation_state(session_id, 'individual_type_selection', {'filer_type': 'individual'})
            return "Great! You're an individual taxpayer. Now let me understand your income sources better. What's your primary income source?", ['salary', 'business', 'profession', 'multiple sources']
        
        elif contains_keywords(message, ['company', 'corporate', 'corporation']):
            update_conversation_state(session_id, 'company_filing', {'filer_type': 'company'})
            return "You're filing for a Company. You'll need to use ITR-6 form. Do you have all required company documents ready?", ['yes', 'no', 'what documents']
        
        elif contains_keywords(message, ['professional', 'ca', 'tax professional', 'agent']):
            update_conversation_state(session_id, 'professional_filing', {'filer_type': 'professional'})
            return "You're a Tax Professional. You can proceed with professional tools and ITR-6 form. Do you need access to professional features?", ['yes', 'client filing', 'bulk filing']
        
        elif contains_keywords(message, ['other', 'entity', 'trust', 'aop', 'boi', 'llp']):
            update_conversation_state(session_id, 'entity_filing', {'filer_type': 'entity'})
            return "You're filing for a Non-Company Entity (AOP, BOI, LLP, Trust). You'll need ITR-5 or ITR-7. What type of entity is this?", ['trust', 'aop', 'boi', 'llp', 'other']
        
        else:
            return "I need to identify your filer type to guide you to the right ITR form. Are you an Individual, Company, Tax Professional, or Other Entity?", ['individual', 'company', 'professional', 'other entity']
    
    # Individual type selection
    elif current_step == 'individual_type_selection':
        if contains_keywords(message, ['salary', 'salaried', 'employee', 'wage']):
            update_conversation_state(session_id, 'check_income_limit', {'income_type': 'salary'})
            return "You have salary income. What's your annual income range? This helps determine the right ITR form.", ['below 50 lakh', 'above 50 lakh', 'not sure']
        
        elif contains_keywords(message, ['business', 'trade', 'commerce']):
            update_conversation_state(session_id, 'business_income_check', {'income_type': 'business'})
            return "You have business income. Is your business turnover below ₹2 crores and you want to use presumptive taxation?", ['yes presumptive', 'no regular', 'what is presumptive']
        
        elif contains_keywords(message, ['profession', 'professional', 'freelance', 'consultant']):
            update_conversation_state(session_id, 'profession_income_check', {'income_type': 'profession'})
            return "You have professional income. Is your professional receipt below ₹50 lakhs and you want to use presumptive taxation?", ['yes presumptive', 'no regular', 'what is presumptive']
        
        elif contains_keywords(message, ['multiple', 'various', 'different', 'mixed']):
            update_conversation_state(session_id, 'multiple_income_check')
            return get_multiple_income_guide(), ['salary + capital gains', 'salary + house property', 'business + other', 'need help']
        
        else:
            return "What's your primary source of income? This helps me recommend the right ITR form.", ['salary', 'business', 'profession', 'multiple sources']
    
    # Check income limit for salaried individuals
    elif current_step == 'check_income_limit':
        if contains_keywords(message, ['below', 'under', '50', 'less']):
            update_conversation_state(session_id, 'check_other_income', {'income_range': 'below_50L'})
            return "Your income is below ₹50 lakhs. Do you have any other income sources like house property, capital gains, or other sources?", ['only salary', 'house property', 'capital gains', 'other sources']
        
        elif contains_keywords(message, ['above', 'over', '50', 'more', 'higher']):
            update_conversation_state(session_id, 'itr2_recommendation', {'income_range': 'above_50L'})
            return "Since your income is above ₹50 lakhs, you need to file ITR-2. Shall we proceed with ITR-2 filing process?", ['yes proceed', 'tell me more', 'what documents needed']
        
        elif contains_keywords(message, ['not sure', 'unsure', 'dont know']):
            return """
            To determine your income range, consider:
            
            💰 **Gross Salary**: Before deductions
            🏠 **House Property**: Rental income (if any)
            📈 **Capital Gains**: From investments (if any)
            💼 **Other Sources**: Interest, dividends etc.
            
            What's your approximate total annual income?
            """, ['below 50 lakh', 'above 50 lakh', 'need calculation help']
        
        else:
            return "I need to know your income range to suggest the right ITR form. Is your total annual income below or above ₹50 lakhs?", ['below 50 lakh', 'above 50 lakh', 'not sure']
    
    # Check other income sources
    elif current_step == 'check_other_income':
        if contains_keywords(message, ['only salary', 'just salary', 'salary only']):
            update_conversation_state(session_id, 'itr1_recommendation', {'final_form': 'ITR-1'})
            return self.get_itr1_recommendation(), ['proceed with ITR-1', 'document checklist', 'tax calculation']
        
        elif contains_keywords(message, ['house', 'property', 'rental', 'rent']):
            update_conversation_state(session_id, 'itr2_recommendation', {'final_form': 'ITR-2', 'reason': 'house_property'})
            return "Since you have house property income along with salary, you need to file ITR-2. Ready to proceed?", ['yes proceed', 'document checklist', 'tell me more']
        
        elif contains_keywords(message, ['capital', 'gains', 'shares', 'mutual fund', 'stocks']):
            update_conversation_state(session_id, 'check_capital_gains_amount')
            return "You have capital gains. Is your Long Term Capital Gains under section 112A less than ₹1.25 lakhs?", ['yes under 1.25L', 'no above 1.25L', 'what is 112A']
        
        elif contains_keywords(message, ['other', 'sources', 'interest', 'dividend']):
            update_conversation_state(session_id, 'itr2_recommendation', {'final_form': 'ITR-2', 'reason': 'other_sources'})
            return "Since you have other sources of income, you need to file ITR-2. Shall we proceed with the filing process?", ['yes proceed', 'document checklist', 'what documents needed']
        
        else:
            return "Apart from salary, do you have income from house property, capital gains, or other sources?", ['only salary', 'house property', 'capital gains', 'other sources']
    
    # Check capital gains amount
    elif current_step == 'check_capital_gains_amount':
        if contains_keywords(message, ['yes', 'under', 'below', '1.25']):
            update_conversation_state(session_id, 'itr1_possible', {'capital_gains': 'under_1.25L'})
            return "Since your LTCG under 112A is below ₹1.25L, you might still be eligible for ITR-1. Do you have any carry forward losses from previous years?", ['no losses', 'yes have losses', 'what are carry forward losses']
        
        elif contains_keywords(message, ['no', 'above', 'over', '1.25']):
            update_conversation_state(session_id, 'itr2_recommendation', {'final_form': 'ITR-2', 'reason': 'capital_gains_high'})
            return "Since your capital gains exceed ₹1.25L, you need to file ITR-2. Ready to start the filing process?", ['yes proceed', 'document checklist', 'tax calculation']
        
        elif contains_keywords(message, ['what', '112a', 'section']):
            return """
            **Section 112A** refers to Long Term Capital Gains (LTCG) on:
            
            📈 **Listed Equity Shares**
            💰 **Equity Mutual Funds**
            🎯 **Units of business trust**
            
            If your LTCG under section 112A is ≤ ₹1.25 lakhs, you might still use ITR-1.
            
            What's your LTCG amount under section 112A?
            """, ['under 1.25L', 'above 1.25L', 'need help calculating']
        
        else:
            return "I need to know your Long Term Capital Gains amount under section 112A. Is it below ₹1.25 lakhs?", ['yes under 1.25L', 'no above 1.25L', 'what is 112A']
    
    # Business income check
    elif current_step == 'business_income_check':
        if contains_keywords(message, ['yes', 'presumptive', 'simple']):
            update_conversation_state(session_id, 'itr4_recommendation', {'final_form': 'ITR-4', 'taxation': 'presumptive'})
            return self.get_itr4_recommendation(), ['proceed with ITR-4', 'document checklist', 'what is presumptive']
        
        elif contains_keywords(message, ['no', 'regular', 'normal', 'detailed']):
            update_conversation_state(session_id, 'itr3_recommendation', {'final_form': 'ITR-3', 'taxation': 'regular'})
            return "You'll need to file ITR-3 for regular business taxation. This requires detailed books of accounts. Ready to proceed?", ['yes proceed', 'document checklist', 'tell me more about ITR-3']
        
        elif contains_keywords(message, ['what', 'presumptive', 'taxation', 'scheme']):
            return self.get_presumptive_taxation_info(), ['yes use presumptive', 'no regular taxation', 'need more info']
        
        else:
            return "For business income, you can choose presumptive taxation (simplified) or regular taxation. Which would you prefer?", ['presumptive taxation', 'regular taxation', 'what is presumptive']
    
    # Profession income check
    elif current_step == 'profession_income_check':
        if contains_keywords(message, ['yes', 'presumptive', 'simple']):
            update_conversation_state(session_id, 'itr4_recommendation', {'final_form': 'ITR-4', 'taxation': 'presumptive'})
            return self.get_itr4_recommendation(), ['proceed with ITR-4', 'document checklist', 'what is presumptive']
        
        elif contains_keywords(message, ['no', 'regular', 'normal']):
            update_conversation_state(session_id, 'itr3_recommendation', {'final_form': 'ITR-3', 'taxation': 'regular'})
            return "You'll need to file ITR-3 for regular professional taxation. Ready to proceed with detailed filing?", ['yes proceed', 'document checklist', 'tell me more about ITR-3']
        
        elif contains_keywords(message, ['what', 'presumptive', 'professional']):
            return self.get_presumptive_taxation_info(), ['yes use presumptive', 'no regular taxation', 'need more info']
        
        else:
            return "For professional income, you can use presumptive taxation (if receipt < ₹50L) or regular taxation. Which option?", ['presumptive taxation', 'regular taxation', 'what is presumptive']
    
    # Multiple income check
    elif current_step == 'multiple_income_check':
        if contains_keywords(message, ['salary', 'capital', 'gains']):
            update_conversation_state(session_id, 'itr2_recommendation', {'final_form': 'ITR-2', 'reason': 'salary_capital_gains'})
            return "Salary + Capital Gains requires ITR-2 filing. Shall we proceed with ITR-2?", ['yes proceed', 'document checklist', 'tax calculation']
        
        elif contains_keywords(message, ['salary', 'house', 'property']):
            update_conversation_state(session_id, 'itr2_recommendation', {'final_form': 'ITR-2', 'reason': 'salary_house_property'})
            return "Salary + House Property income requires ITR-2. Ready to start filing?", ['yes proceed', 'document checklist', 'tax calculation']
        
        elif contains_keywords(message, ['business', 'other']):
            update_conversation_state(session_id, 'itr3_recommendation', {'final_form': 'ITR-3', 'reason': 'business_multiple'})
            return "Business income with other sources requires ITR-3. Shall we proceed?", ['yes proceed', 'document checklist', 'tell me more']
        
        elif contains_keywords(message, ['help', 'confused', 'not sure']):
            return self.get_income_source_help(), ['salary + capital gains', 'salary + house property', 'business + other', 'start over']
        
        else:
            return self.get_multiple_income_guide(), ['salary + capital gains', 'salary + house property', 'business + other', 'need help']
    
    # ITR-1 recommendation flow
    elif current_step == 'itr1_recommendation':
        if contains_keywords(message, ['proceed', 'yes', 'start', 'itr-1']):
            update_conversation_state(session_id, 'choose_tax_regime')
            return "Great! Let's proceed with ITR-1. First, you need to choose your tax regime. Which tax regime do you want to use?", ['new regime', 'old regime', 'which is better']
        
        elif contains_keywords(message, ['document', 'checklist', 'papers']):
            return self.get_itr1_documents(), ['proceed with ITR-1', 'tax calculation', 'have documents']
        
        elif contains_keywords(message, ['tax', 'calculation', 'calculate']):
            update_conversation_state(session_id, 'tax_calculation')
            return "Let me help you calculate your tax. What's your gross annual salary (before deductions)?", ['enter amount', 'need help', 'use calculator']
        
        else:
            return get_itr1_recommendation(), ['proceed with ITR-1', 'document checklist', 'tax calculation']
    
    # ITR-2 recommendation flow
    elif current_step == 'itr2_recommendation':
        if contains_keywords(message, ['proceed', 'yes', 'start', 'itr-2']):
            update_conversation_state(session_id, 'choose_tax_regime')
            return "Perfect! Let's proceed with ITR-2 filing. Which tax regime would you like to choose?", ['new regime', 'old regime', 'compare regimes']
        
        elif contains_keywords(message, ['document', 'checklist', 'needed']):
            return get_itr2_documents(), ['proceed with ITR-2', 'have documents', 'tax calculation']
        
        elif contains_keywords(message, ['tell me more', 'more info', 'details']):
            return get_itr2_details(), ['proceed with ITR-2', 'document checklist', 'tax calculation']
        
        else:
            return "ITR-2 is required for your income profile. Ready to proceed with filing?", ['yes proceed', 'document checklist', 'tell me more']
    
    # ITR-3 recommendation flow
    elif current_step == 'itr3_recommendation':
        if contains_keywords(message, ['proceed', 'yes', 'start']):
            update_conversation_state(session_id, 'choose_tax_regime')
            return "Excellent! ITR-3 filing requires detailed books of accounts. Which tax regime do you prefer?", ['new regime', 'old regime', 'need guidance']
        
        elif contains_keywords(message, ['document', 'checklist']):
            return self.get_itr3_documents(), ['proceed with ITR-3', 'have documents', 'need help']
        
        elif contains_keywords(message, ['tell me more', 'more about', 'details']):
            return self.get_itr3_details(), ['proceed with ITR-3', 'document checklist', 'presumptive instead']
        
        else:
            return "ITR-3 is for business/professional income with regular taxation. Ready to proceed?", ['yes proceed', 'document checklist', 'tell me more about ITR-3']
    
    # ITR-4 recommendation flow
    elif current_step == 'itr4_recommendation':
        if contains_keywords(message, ['proceed', 'yes', 'start']):
            update_conversation_state(session_id, 'choose_tax_regime')
            return "Great choice! ITR-4 with presumptive taxation is simpler. Which tax regime works better for you?", ['new regime', 'old regime', 'help me choose']
        
        elif contains_keywords(message, ['document', 'checklist']):
            return self.get_itr4_documents(), ['proceed with ITR-4', 'have documents', 'tax calculation']
        
        elif contains_keywords(message, ['what', 'presumptive']):
            return self.get_presumptive_taxation_info(), ['proceed with ITR-4', 'regular taxation instead', 'more questions']
        
        else:
            return self.get_itr4_recommendation(), ['proceed with ITR-4', 'document checklist', 'what is presumptive']
    
    # Choose tax regime
    elif current_step == 'choose_tax_regime':
        if contains_keywords(message, ['new', 'regime', 'new regime']):
            update_conversation_state(session_id, 'enter_personal_details', {'tax_regime': 'new'})
            return "You've selected the New Tax Regime. Now let's enter your personal details. Please provide your PAN number:", ['enter PAN', 'need help', 'what details needed']
        
        elif contains_keywords(message, ['old', 'regime', 'old regime']):
            update_conversation_state(session_id, 'enter_personal_details', {'tax_regime': 'old'})
            return "You've selected the Old Tax Regime. Let's proceed with personal details. Please provide your PAN number:", ['enter PAN', 'need help', 'what details needed']
        
        elif contains_keywords(message, ['which', 'better', 'compare', 'help']):
            return self.get_tax_regime_comparison(), ['new regime', 'old regime', 'calculate for me']
        
        else:
            return "Please choose your tax regime. This affects your tax calculation and deductions.", ['new regime', 'old regime', 'which is better']
    
    # Enter personal details
    elif current_step == 'enter_personal_details':
        if contains_keywords(message, ['pan', 'enter pan']) or re.match(r'[A-Z]{5}[0-9]{4}[A-Z]{1}', message.upper()):
            pan_match = re.search(r'[A-Z]{5}[0-9]{4}[A-Z]{1}', message.upper())
            if pan_match:
                pan = pan_match.group()
                update_conversation_state(session_id, 'residential_status', {'pan': pan})
                return f"PAN {pan} recorded. What's your residential status for tax purposes?", ['resident', 'non-resident', 'not sure']
            else:
                return "Please provide a valid PAN number (format: ABCDE1234F):", ['need help', 'what is PAN format']
        
        elif contains_keywords(message, ['what', 'details', 'needed']):
            return self.get_personal_details_list(), ['enter PAN', 'start entering', 'need help']
        
        elif contains_keywords(message, ['help', 'format']):
            return "PAN format is ABCDE1234F (5 letters + 4 numbers + 1 letter). Please enter your PAN:", ['enter PAN', 'example']
        
        else:
            return "I need your PAN number to proceed. Please enter your PAN (format: ABCDE1234F):", ['enter PAN', 'need help', 'what details needed']
    
    # Residential status
    elif current_step == 'residential_status':
        if contains_keywords(message, ['resident', 'indian resident']):
            update_conversation_state(session_id, 'declare_exempt_income', {'residential_status': 'resident'})
            return "Residential status: Indian Resident. Do you have any exempt income to declare (like agricultural income, etc.)?", ['yes exempt income', 'no exempt income', 'what is exempt income']
        
        elif contains_keywords(message, ['non-resident', 'nri', 'non resident']):
            update_conversation_state(session_id, 'declare_exempt_income', {'residential_status': 'non-resident'})
            return "Residential status: Non-Resident. Do you have any exempt income to declare?", ['yes exempt income', 'no exempt income', 'what is exempt income']
        
        elif contains_keywords(message, ['not sure', 'unsure', 'help']):
            return self.get_residential_status_help(), ['resident', 'non-resident', 'need more help']
        
        else:
            return "Please specify your residential status for tax purposes:", ['resident', 'non-resident', 'not sure']
    
    # Declare exempt income
    elif current_step == 'declare_exempt_income':
        if contains_keywords(message, ['no', 'no exempt', 'none']):
            update_conversation_state(session_id, 'input_income_details')
            return "No exempt income noted. Now let's input your income details. Based on your profile, please provide your income information:", ['salary details', 'start income entry', 'what income needed']
        
        elif contains_keywords(message, ['yes', 'have exempt', 'exempt income']):
            update_conversation_state(session_id, 'enter_exempt_income')
            return "Please specify your exempt income sources and amounts:", ['agricultural income', 'other exempt income', 'need help']
        
        elif contains_keywords(message, ['what', 'exempt', 'income']):
            return self.get_exempt_income_info(), ['yes exempt income', 'no exempt income', 'more examples']
        
        else:
            return "Do you have any exempt income to declare (like agricultural income)?", ['yes exempt income', 'no exempt income', 'what is exempt income']
    
    # Input income details
    elif current_step == 'input_income_details':
        form_type = user_data.get('final_form', 'ITR-1')
        
        if contains_keywords(message, ['salary', 'start', 'proceed']):
            update_conversation_state(session_id, 'verify_tds_advance_tax')
            return f"Let's input your income for {form_type}. First, let's verify your TDS and advance tax payments. Do you have your Form-16 and TDS certificates ready?", ['yes have form-16', 'no need help', 'what is form-16']
        
        elif contains_keywords(message, ['what', 'income', 'needed']):
            return self.get_income_requirements(form_type), ['salary details', 'start income entry', 'document checklist']
        
        else:
            return f"Ready to input income details for {form_type}? Let's start with your primary income source:", ['salary details', 'start income entry', 'what income needed']
    
    # Verify TDS and advance tax
    elif current_step == 'verify_tds_advance_tax':
        if contains_keywords(message, ['yes', 'have', 'ready']):
            update_conversation_state(session_id, 'calculate_tax_liability')
            return "Perfect! With your TDS certificates, let's calculate your tax liability. The system will highlight any mismatches. Ready to calculate?", ['calculate tax', 'yes calculate', 'what calculations']
        
        elif contains_keywords(message, ['no', 'dont have', 'need help']):
            return self.get_tds_help(), ['have documents now', 'proceed anyway', 'download from portal']
        
        elif contains_keywords(message, ['what', 'form-16', 'tds']):
            return self.get_form16_info(), ['yes have form-16', 'no need help', 'download from employer']
        
        else:
            return "Do you have your Form-16 and TDS certificates to verify tax deductions?", ['yes have form-16', 'no need help', 'what is form-16']
    
    # Calculate tax liability
    elif current_step == 'calculate_tax_liability':
        if contains_keywords(message, ['calculate', 'yes', 'proceed']):
            update_conversation_state(session_id, 'check_tax_payable')
            return "Tax calculation completed! The system has processed your income and deductions. Is there any remaining tax payable after TDS?", ['yes tax payable', 'no refund due', 'show calculation']
        
        elif contains_keywords(message, ['what', 'calculations', 'show me']):
            return self.get_tax_calculation_info(), ['calculate tax', 'need help', 'proceed']
        
        else:
            return "Ready to calculate your tax liability based on your income and deductions?", ['calculate tax', 'yes calculate', 'what calculations']
    
    # Check if tax is payable
    elif current_step == 'check_tax_payable':
        if contains_keywords(message, ['yes', 'tax payable', 'owe tax']):
            update_conversation_state(session_id, 'pay_remaining_tax')
            return "You have remaining tax to pay. You can pay online through the IT portal. Would you like guidance on payment methods?", ['pay online', 'payment methods', 'how to pay']
        
        elif contains_keywords(message, ['no', 'refund', 'refund due']):
            update_conversation_state(session_id, 'filing_complete')
            return "Great! You're eligible for a tax refund. Let's complete your filing process. Ready to finalize and submit your ITR?", ['complete filing', 'yes submit', 'review before submit']
        
        elif contains_keywords(message, ['show', 'calculation', 'details']):
            return self.get_tax_summary(), ['yes tax payable', 'no refund due', 'need clarification']
        
        else:
            return "Based on the calculation, is there any remaining tax payable after considering TDS?", ['yes tax payable', 'no refund due', 'show calculation']
    
    # Pay remaining tax
    elif current_step == 'pay_remaining_tax':
        if contains_keywords(message, ['pay', 'online', 'proceed']):
            update_conversation_state(session_id, 'filing_complete')
            return "Tax payment process initiated. Once payment is confirmed, we can complete your filing. Ready to finalize your ITR submission?", ['complete filing', 'verify payment', 'submit ITR']
        
        elif contains_keywords(message, ['payment', 'methods', 'how']):
            return self.get_payment_methods(), ['pay online', 'net banking', 'proceed with payment']
        
        else:
            return "You need to pay the remaining tax before completing filing. Shall we proceed with online payment?", ['pay online', 'payment methods', 'how to pay']
    
    # Filing complete
    elif current_step == 'filing_complete':
        if contains_keywords(message, ['complete', 'submit', 'finalize']):
            update_conversation_state(session_id, 'download_itr_v')
            return "Excellent! Your ITR filing is complete. You can now download your ITR-V (acknowledgment). Would you like to download it?", ['download ITR-V', 'e-verify now', 'what next']
        
        elif contains_keywords(message, ['review', 'check', 'verify']):
            return self.get_filing_summary(user_data), ['looks good', 'complete filing', 'need changes']
        
        else:
            return "Your ITR is ready for submission. Shall we complete the filing process?", ['complete filing', 'yes submit', 'review before submit']
    
    # Download ITR-V
    elif current_step == 'download_itr_v':
        if contains_keywords(message, ['download', 'yes']):
            update_conversation_state(session_id, 'e_verify_itr')
            return "ITR-V downloaded successfully! Now you need to e-verify your ITR within 120 days. How would you like to e-verify?", ['aadhaar OTP', 'demat account', 'bank account', 'what is e-verify']
        
        elif contains_keywords(message, ['e-verify', 'verify now']):
            update_conversation_state(session_id, 'e_verify_itr')
            return "Let's proceed with e-verification. Which method would you prefer for e-verification?", ['aadhaar OTP', 'demat account', 'bank account', 'net banking']
        
        elif contains_keywords(message, ['what next', 'next steps']):
            return self.get_post_filing_steps(), ['download ITR-V', 'e-verify now', 'all done']
        
        else:
            return "Filing completed! Would you like to download your ITR-V acknowledgment?", ['download ITR-V', 'e-verify now', 'what next']
    
    # E-verify ITR
    elif current_step == 'e_verify_itr':
        if contains_keywords(message, ['aadhaar', 'otp']):
            update_conversation_state(session_id, 'verification_complete', {'verify_method': 'aadhaar'})
            return "E-verification via Aadhaar OTP is the most convenient method. You'll receive an OTP on your registered mobile. Process completed!", ['all done', 'download receipt', 'any questions']
        
        elif contains_keywords(message, ['demat', 'account']):
            update_conversation_state(session_id, 'verification_complete', {'verify_method': 'demat'})
            return "E-verification via Demat account selected. Please use your demat account credentials to complete verification. Done!", ['all done', 'download receipt', 'need help']
        
        elif contains_keywords(message, ['bank', 'account', 'net banking']):
            update_conversation_state(session_id, 'verification_complete', {'verify_method': 'bank'})
            return "E-verification via bank account/net banking selected. Use your bank credentials to verify. Process completed!", ['all done', 'download receipt', 'any questions']
        
        elif contains_keywords(message, ['what', 'e-verify', 'verification']):
            return self.get_e_verify_info(), ['aadhaar OTP', 'demat account', 'bank account', 'more options']
        
        else:
            return "Please choose your preferred e-verification method:", ['aadhaar OTP', 'demat account', 'bank account', 'what is e-verify']
    
    # Verification complete - End state
    elif current_step == 'verification_complete':
        if contains_keywords(message, ['done', 'complete', 'finished']):
            return self.get_completion_message(user_data), ['file another ITR', 'start over', 'have questions']
        
        elif contains_keywords(message, ['receipt', 'download']):
            return "You can download your e-verification receipt from the IT portal. Your ITR filing is now complete and verified!", ['all done', 'file another ITR', 'any questions']
        
        elif contains_keywords(message, ['questions', 'help', 'doubt']):
            return "I'm here to help! What questions do you have about your ITR filing?", ['refund status', 'amendment process', 'next year filing', 'start over']
        
        else:
            return self.get_completion_message(user_data), ['all done', 'download receipt', 'any questions']
    
    # Default fallback for unrecognized steps or inputs
    else:
        return "I didn't understand that. Let me help you with your ITR filing. What would you like to do?", ['start filing', 'help', 'which itr form', 'start over']

# Helper functions for generating responses
class ITRResponseGenerator:
    @staticmethod
    def get_itr_form_guide():
        return """ 
        🔍 **ITR Form Selection Guide:**
        
        📝 **ITR-1 (Sahaj)**: Salary, pension, one house property, other sources < ₹50L
        📄 **ITR-2**: Salary + capital gains/multiple house properties, income > ₹50L
        📊 **ITR-3**: Business/Professional income (regular taxation)
        📋 **ITR-4 (Sugam)**: Business/Professional with presumptive taxation
        🏢 **ITR-5**: LLP, AOP, BOI, Trusts
        🏭 **ITR-6**: Companies
        🏛️ **ITR-7**: Trusts, political parties
        
        Which income sources do you have?
        """
    
    @staticmethod
    def get_aadhaar_linking_guide():
        return """
        🔗 **Link Aadhaar with PAN:**
        
        **Online Methods:**
        • 🌐 IT e-filing portal: incometax.gov.in
        • 📱 SMS: Send to 567678 or 56161
        • 🔗 Direct link: eportal.incometax.gov.in/iec/foservices
        
        **Required Information:**
        • PAN Number
        • Aadhaar Number
        • Name (as per Aadhaar)
        
        **Time Required:** Usually instant
        
        Have you completed the linking process?
        """
    
    @staticmethod
    def get_multiple_income_guide():
        return """
        🔄 **Multiple Income Sources Guide:**
        
        **Common Combinations:**
        💼 **Salary + Capital Gains** → ITR-2
        🏠 **Salary + House Property** → ITR-2  
        💰 **Salary + Other Sources** → ITR-2
        🏢 **Business + Other Income** → ITR-3
        📈 **Professional + Investment** → ITR-3
        
        **Key Points:**
        • Multiple sources usually require ITR-2 or ITR-3
        • ITR-1 only for simple salary cases
        • Business income needs ITR-3 or ITR-4
        
        What's your income combination?
        """

# Add the response generator methods to the main processing function
def get_itr_form_guide():
    return ITRResponseGenerator.get_itr_form_guide()

def get_aadhaar_linking_guide(): 
    return ITRResponseGenerator.get_aadhaar_linking_guide()

def get_multiple_income_guide():
    return ITRResponseGenerator.get_multiple_income_guide()

def get_itr1_recommendation():
    return """
    ✅ **ITR-1 (Sahaj) Recommended for you!**
    
    **Perfect for:**
    • 💰 Salary income only
    • 🏠 Income < ₹50 lakhs
    • 🎯 Simple tax situation
    
    **Benefits:**
    • ⚡ Quick and easy filing
    • 📱 Mobile-friendly
    • 🎨 User-friendly interface
    • ⏱️ Minimal time required
    
    **Next Steps:**
    1. Choose tax regime
    2. Enter personal details  
    3. Input salary details
    4. Submit and e-verify
    
    Ready to proceed?
    """

def get_itr2_details():
    return """
    📋 **ITR-2 Details:**
    
    **Use ITR-2 when you have:**
    • 💼 Salary + Capital Gains
    • 🏠 Multiple house properties
    • 💰 Income > ₹50 lakhs
    • 📈 Foreign income/assets
    • 🎯 Carried forward losses
    
    **Additional Requirements:**
    • More detailed information needed
    • Capital gains computation
    • Foreign asset disclosure (if applicable)
    • Schedule for various income sources
    
    **Processing Time:** Slightly longer than ITR-1
    """

def get_itr3_details():
    return """
    📊 **ITR-3 Details:**
    
    **Required for:**
    • 🏢 Business income (regular taxation)
    • 👨‍💼 Professional income (regular taxation) 
    • 📚 Maintained books of accounts
    • 🔄 Multiple income sources with business
    
    **Requirements:**
    • Profit & Loss statement
    • Balance sheet
    • Tax audit (if applicable)
    • Detailed books of accounts
    
    **Note:** More complex than ITR-1/ITR-2
    """

def get_itr4_recommendation():
    return """
    ⚡ **ITR-4 (Sugam) - Great Choice!**
    
    **Presumptive Taxation Benefits:**
    • 📖 No books of accounts required
    • 🧮 Simplified calculations
    • ⏰ Time-saving
    • 📉 Lower compliance burden
    
    **Eligibility:**
    • 🏢 Business turnover < ₹2 crores
    • 👨‍💼 Professional receipt < ₹50 lakhs
    • 💡 Presumptive income scheme
    
    **Tax Rate:**
    • 8% of turnover (digital transactions)
    • 6% for professional services
    
    This makes filing much simpler!
    """

def get_presumptive_taxation_info():
    return """
    💡 **Presumptive Taxation Scheme:**
    
    **How it Works:**
    • 🎯 Declare income as % of turnover
    • 📖 No detailed books needed
    • 🧮 Simplified tax calculation
    
    **Rates:**
    • 8% of business turnover
    • 6% for professional services
    • Higher rates for cash transactions
    
    **Pros:**
    ✅ Simple and quick
    ✅ No audit requirements
    ✅ Lower compliance cost
    
    **Cons:**
    ❌ May pay more tax
    ❌ Limited deductions
    ❌ Less control over income
    
    Still want to use presumptive taxation?
    """

def get_tax_regime_comparison():
    return """
    ⚖️ **Tax Regime Comparison:**
    
    **🆕 New Regime:**
    ✅ Lower tax rates
    ❌ Limited deductions
    ✅ Simple calculation
    ❌ No 80C, HRA benefits
    
    **🔄 Old Regime:** 
    ❌ Higher tax rates
    ✅ Multiple deductions available
    ❌ Complex calculations
    ✅ 80C, HRA, home loan benefits
    
    **Recommendation:**
    • New: If minimal investments/deductions
    • Old: If significant 80C, HRA, home loan
    
    **Tip:** You can switch regimes each year!
    
    Which regime suits your situation?
    """

def get_itr1_documents():
    return """
    📄 **ITR-1 Document Checklist:**
    
    **Essential Documents:**
    • 📋 Form-16 from employer
    • 💳 Salary slips (all months)
    • 📊 TDS certificates
    • 🏦 Bank interest certificates
    • 💰 Investment proofs (80C)
    
    **Optional (if applicable):**
    • 🏠 House rent receipts (HRA)
    • 🏥 Medical bills (80D) 
    • 📚 Donation receipts (80G)
    • 💳 PAN card copy
    • 🆔 Aadhaar card copy
    
    **Digital Copies:** Keep all documents ready in PDF format
    
    Do you have all required documents?
    """

def get_itr2_documents():
    return """
    📋 **ITR-2 Document Checklist:**
    
    **Basic Documents:**
    • 📄 Form-16 from employer  
    • 💳 Salary slips
    • 📊 TDS certificates
    • 🏦 Bank statements
    
    **Additional for ITR-2:**
    • 📈 Capital gains statements
    • 🏠 House property documents
    • 💰 Rental agreements (if any)
    • 🎯 Investment proofs
    • 📉 Loss carry forward details
    
    **Foreign Assets (if any):**
    • 🌍 Foreign bank statements
    • 💱 Foreign investment details
    
    **Time to gather:** Allow 2-3 days for complete documentation
    """

def get_completion_message(user_data):
    form_type = user_data.get('final_form', 'ITR')
    verify_method = user_data.get('verify_method', 'chosen method')
    
    return f"""
    🎉 **Congratulations! ITR Filing Completed Successfully!**
    
    **Summary:**
    • 📋 Form: {form_type} 
    • ✅ E-verified via {verify_method}
    • 📅 Filing Date: {datetime.now().strftime('%Y-%m-%d')}
    
    **What's Next:**
    • 📧 Save confirmation email
    • 📱 Track refund status online
    • 📋 Keep ITR-V for records
    • 🗓️ Next filing: March 2026
    
    **Important Deadlines:**
    • 🎯 Amendment: Before March end
    • 💰 Refund: Usually within 45 days
    
    Thank you for using ITR Filing Assistant! 
    Your taxes are now successfully filed and verified.
    """

# Additional helper functions
def get_exempt_income_info():
    return """
    🔍 **Exempt Income Examples:**
    
    **Common Exempt Sources:**
    • 🌾 Agricultural income
    • 🎁 Gifts < ₹50,000
    • 📚 Scholarship/fellowship
    • 🏆 Awards from government
    • 💰 Life insurance maturity
    • 🏥 Gratuity (within limits)
    • 🎯 PPF withdrawal
    • 💳 HRA (exempt portion)
    
    **Important:**
    • Must be declared even if exempt
    • Affects tax calculation indirectly
    • Required for complete disclosure
    
    Do you have any of these income sources?
    """

def get_personal_details_list():
    return """
    📋 **Personal Details Required:**
    
    **Basic Information:**
    • 🆔 PAN Number
    • 📱 Mobile Number  
    • 📧 Email Address
    • 🏠 Address details
    • 📅 Date of Birth
    
    **Tax Related:**
    • 🌍 Residential Status
    • 💼 Occupation
    • 🏢 Employer details
    • 🏦 Bank account details
    
    **Additional:**
    • 👥 Dependents (if any)
    • 🔗 Aadhaar linking status
    
    Let's start with your PAN number:
    """

def get_residential_status_help():
    return """
    🌍 **Residential Status Guide:**
    
    **Resident:** If you are in India for:
    • 182+ days in current year, OR
    • 60+ days in current year + 365+ days in last 4 years
    
    **Non-Resident:** If you don't meet resident criteria
    
    **Impact on Taxation:**
    • 🏠 Resident: Tax on global income
    • ✈️ Non-Resident: Tax only on India income
    
    **Most Common:** Indian citizens living in India = Resident
    
    Which category applies to you?
    """

def get_income_requirements(form_type):
    requirements = {
        'ITR-1': "Salary income details from Form-16",
        'ITR-2': "Salary + Capital gains/House property details", 
        'ITR-3': "Business/Professional income with books of accounts",
        'ITR-4': "Business/Professional turnover for presumptive taxation"
    }
    
    return f"""
    📊 **Income Details Required for {form_type}:**
    
    **Primary Requirement:**
    {requirements.get(form_type, "Income details as per ITR form")}
    
    **Supporting Documents:**
    • 📋 Form-16 (for salary)
    • 🏦 Bank statements
    • 📊 Investment statements  
    • 🧾 Expense receipts
    • 📈 Capital gains computation
    
    **Preparation Time:** 30-60 minutes
    
    Ready to input your income details?
    """

def get_form16_info():
    return """
    📋 **Form-16 Information:**
    
    **What is Form-16:**
    • 📄 TDS certificate from employer
    • 💰 Shows salary and tax deducted
    • 📅 Issued annually by employer
    • ✅ Essential for ITR filing
    
    **Contains:**
    • Gross salary details
    • Tax deductions (80C, HRA, etc.)
    • TDS amount
    • Net salary paid
    
    **How to Get:**
    • 🏢 Request from HR/Accounts
    • 📧 Usually emailed in April/May
    • 🌐 Download from employer portal
    
    Do you have your Form-16?
    """

def get_tds_help():
    return """
    📊 **TDS Certificate Help:**
    
    **Where to Get TDS Certificates:**
    • 🏢 Form-16: From employer
    • 🏦 Form-16A: From banks (interest)
    • 🏠 Form-16B: From property buyers
    • 📈 Form-16C: From mutual funds
    
    **Online Download:**
    • 🌐 26AS statement from IT portal
    • 📱 View all TDS in one place
    • ✅ Cross-verify with certificates
    
    **If Missing:**
    • Contact deductor directly
    • Use 26AS as alternative
    • File ITR with available info
    
    Can you proceed with available documents?
    """

def get_tax_calculation_info():
    return """
    🧮 **Tax Calculation Process:**
    
    **Steps:**
    1. 💰 Gross Income Calculation
    2. ➖ Deductions (80C, 80D, etc.)
    3. 📊 Taxable Income Determination  
    4. 🎯 Tax Rate Application
    5. 📉 TDS/Advance Tax Adjustment
    6. ✅ Final Tax Payable/Refund
    
    **System Features:**
    • ⚡ Auto-calculation
    • 🔍 Error detection
    • 📋 Mismatch highlighting
    • 💡 Optimization suggestions
    
    **Result:** Exact tax liability and refund amount
    
    Shall we proceed with calculation?
    """

def get_tax_summary():
    return """
    📊 **Tax Summary:**
    
    **Calculation Breakdown:**
    • 💰 Total Income: [Calculated]
    • ➖ Total Deductions: [Applied]
    • 🎯 Taxable Income: [Computed]
    • 📈 Tax Before Relief: [Calculated]
    • 📉 Tax Relief/Rebate: [If applicable]
    • 💳 Total Tax Liability: [Final]
    • 🏦 TDS/Advance Tax: [Paid]
    • ✅ Net Payable/Refund: [Result]
    
    **Next Steps:**
    • Tax Payable: Make payment
    • Refund Due: Complete filing for refund
    
    What's your situation?
    """

def get_payment_methods():
    return """
    💳 **Tax Payment Methods:**
    
    **Online Payment:**
    • 🏦 Net Banking (All major banks)
    • 💳 Credit/Debit Cards
    • 📱 UPI Payment
    • 🌐 IT e-payment portal
    
    **Offline Payment:**
    • 🏢 Bank challan (ITNS 280)
    • 🏦 Authorized bank branches
    
    **Recommended:** Online payment for instant confirmation
    
    **Payment Portal:** onlineservices.nsdl.com/paam/endUserLogin.html
    
    **Required Info:**
    • PAN Number
    • Assessment Year: 2025-26
    • Type of Payment: Income Tax
    
    Ready to make payment?
    """

def get_e_verify_info():
    return """
    ✅ **E-verification Information:**
    
    **What is E-verification:**
    • 📧 Electronic confirmation of ITR
    • ⏰ Must be done within 120 days
    • ✅ Completes the filing process
    • 🚫 ITR invalid without e-verification
    
    **Available Methods:**
    • 🆔 Aadhaar OTP (Recommended)
    • 🏦 Net Banking
    • 💳 Demat Account
    • 📧 EVC (Electronic Verification Code)
    
    **Aadhaar OTP Benefits:**
    • ⚡ Instant verification
    • 📱 SMS OTP to registered mobile
    • 🔒 Secure and convenient
    
    Which method would you prefer?
    """

def get_post_filing_steps():
    return """
    📅 **Post-Filing Steps:**
    
    **Immediate (Within 120 days):**
    • ✅ E-verify your ITR
    • 📧 Save confirmation email
    • 📋 Download ITR-V
    
    **Within 30 days:**
    • 🔍 Check processing status
    • 📱 Track refund (if applicable)
    • 📋 Update bank details if needed
    
    **Important Notes:**
    • 💰 Refund timeline: 45-60 days
    • 📧 All communication via email/SMS
    • 🔔 Enable IT portal notifications
    • 📞 Helpline: 1800-103-0025
    
    **Next Year:** File by July 31, 2026
    
    Any questions about these steps?
    """

def get_filing_summary(user_data):
    form_type = user_data.get('final_form', 'ITR')
    tax_regime = user_data.get('tax_regime', 'Selected')
    filer_type = user_data.get('filer_type', 'Individual')
    
    return f"""
    📋 **Filing Summary - Please Review:**
    
    **ITR Details:**
    • 📄 Form Type: {form_type}
    • 👤 Filer Type: {filer_type.title()}
    • ⚖️ Tax Regime: {tax_regime.title()}
    • 📅 Assessment Year: 2025-26
    
    **Income Sources:** As declared
    **Deductions:** As applicable under chosen regime
    **Tax Status:** Calculated based on inputs
    
    **Next Steps:**
    1. Final submission
    2. Download ITR-V
    3. E-verification
    4. Track status
    
    **Important:** Review all details carefully before submission.
    Once submitted, amendments require separate process.
    
    Does everything look correct?
    """

def get_income_source_help():
    return """
    💡 **Income Source Identification Help:**
    
    **Ask Yourself:**
    • 💼 Do I receive salary/pension? → Salary Income
    • 🏠 Do I own rental property? → House Property  
    • 📈 Did I sell shares/property? → Capital Gains
    • 🏢 Do I run a business? → Business Income
    • 👨‍💼 Am I a freelancer/consultant? → Professional Income
    • 🏦 Do I earn interest/dividends? → Other Sources
    
    **Common Combinations:**
    • Salaried + Investor = Salary + Capital Gains
    • Salaried + Landlord = Salary + House Property
    • Business Owner + Investor = Business + Capital Gains
    
    **Need More Help?**
    List all your income sources, and I'll guide you to the right ITR form.
    
    What income sources do you have?
    """

# Initialize the response generator class methods  
ITRResponseGenerator.get_itr1_recommendation = staticmethod(get_itr1_recommendation)
ITRResponseGenerator.get_itr2_details = staticmethod(get_itr2_details) 
ITRResponseGenerator.get_itr3_details = staticmethod(get_itr3_details)
ITRResponseGenerator.get_itr4_recommendation = staticmethod(get_itr4_recommendation)
ITRResponseGenerator.get_presumptive_taxation_info = staticmethod(get_presumptive_taxation_info)
ITRResponseGenerator.get_tax_regime_comparison = staticmethod(get_tax_regime_comparison)
ITRResponseGenerator.get_itr1_documents = staticmethod(get_itr1_documents)
ITRResponseGenerator.get_itr2_documents = staticmethod(get_itr2_documents)
ITRResponseGenerator.get_completion_message = staticmethod(get_completion_message)
ITRResponseGenerator.get_exempt_income_info = staticmethod(get_exempt_income_info)
ITRResponseGenerator.get_personal_details_list = staticmethod(get_personal_details_list)
ITRResponseGenerator.get_residential_status_help = staticmethod(get_residential_status_help)
ITRResponseGenerator.get_income_requirements = staticmethod(get_income_requirements)
ITRResponseGenerator.get_form16_info = staticmethod(get_form16_info)
ITRResponseGenerator.get_tds_help = staticmethod(get_tds_help)
ITRResponseGenerator.get_tax_calculation_info = staticmethod(get_tax_calculation_info)
ITRResponseGenerator.get_tax_summary = staticmethod(get_tax_summary)
ITRResponseGenerator.get_payment_methods = staticmethod(get_payment_methods)
ITRResponseGenerator.get_e_verify_info = staticmethod(get_e_verify_info)
ITRResponseGenerator.get_post_filing_steps = staticmethod(get_post_filing_steps)
ITRResponseGenerator.get_filing_summary = staticmethod(get_filing_summary)
ITRResponseGenerator.get_income_source_help = staticmethod(get_income_source_help)

# Add missing method references to process_chat_message function
def self_get_method(method_name):
    """Helper to call static methods from ITRResponseGenerator"""
    return getattr(ITRResponseGenerator, method_name, lambda: "Information not available")()

# Update the process_chat_message function to use proper method calls
def process_chat_message_updated(message: str, session_id: str) -> Tuple[str, Optional[List[str]]]:
    """Updated version with proper method calls"""
    # Replace all self.get_method() calls with proper function calls
    return process_chat_message(message, session_id).replace(
        'self.get_itr_form_guide()', get_itr_form_guide()
    ).replace(
        'self.get_aadhaar_linking_guide()', get_aadhaar_linking_guide()
    ).replace(
        'self.get_multiple_income_guide()', get_multiple_income_guide()
    )

# Export the main function
__all__ = ['process_chat_message', 'get_conversation_state', 'update_conversation_state']