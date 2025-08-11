import requests
import random
import string
import time
import re
from datetime import datetime

print("🤖 SCITE.AI SIGNUP BOT - INDONESIAN NAMES VERSION")
print("="*50)

# The working signup endpoint
SIGNUP_ENDPOINT = "https://scite.ai/api/users/register"

def get_indonesian_name():
    """Get a random Indonesian name from ninjaname.net"""
    try:
        print("🔄 Getting Indonesian name from ninjaname.net...")
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        response = session.get("http://ninjaname.net/indonesian_name.php", timeout=10)
        
        if response.status_code == 200:
            html_content = response.text
            
            # Look for all divs with background-color:#f9f3dd (there are usually 2: form and names)
            name_section_pattern = r'<div style="background-color:#f9f3dd; padding:10px;">\s*(.*?)</div>'
            name_section_matches = re.findall(name_section_pattern, html_content, re.DOTALL)
            
            print(f"Found {len(name_section_matches)} sections to check...")
            
            # Find the section that contains names (with bullet points)
            for i, section in enumerate(name_section_matches):
                if '&bull;' in section:
                    print(f"Found names in section {i+1}")
                    
                    # Extract individual names from bullet points
                    name_pattern = r'&bull;\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+[A-Z][a-z]+)*)<br/>'
                    names = re.findall(name_pattern, section)
                    
                    if names:
                        # Pick a random name from the list
                        selected_name = random.choice(names)
                        
                        # Clean up the name (remove extra words that don't look like proper names)
                        name_words = selected_name.split()
                        
                        # Keep only 2-3 words that look like proper names
                        clean_words = []
                        for word in name_words:
                            if len(word) > 1 and word.isalpha() and word[0].isupper():
                                clean_words.append(word)
                                if len(clean_words) >= 3:  # Limit to 3 words max
                                    break
                        
                        if len(clean_words) >= 2:  # Need at least first and last name
                            final_name = ' '.join(clean_words)
                            print(f"👤 Found Indonesian name: {final_name}")
                            return final_name
            
            print("⚠️  Could not extract names from sections, trying fallback patterns...")
            
            # Fallback patterns if the main extraction fails
            fallback_patterns = [
                r'<h2[^>]*>([^<]+)</h2>',
                r'<h1[^>]*>([^<]+)</h1>',
                r'<div[^>]*class[^>]*name[^>]*>([^<]+)</div>',
                r'<p[^>]*>\s*([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*</p>',
                r'<span[^>]*>\s*([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*</span>',
            ]
            
            for pattern in fallback_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                for match in matches:
                    name = match.strip()
                    # Filter out generic text and validate as a real name
                    if (len(name) > 3 and 
                        not any(word in name.lower() for word in ['generator', 'name', 'indonesian', 'random', 'ninja', 'website', 'click', 'generate', 'page', 'title', 'fake']) and
                        re.match(r'^[A-Za-z\s]+$', name)):
                        
                        words = name.split()
                        # Check if it looks like a valid name (2-3 words, proper length)
                        if 2 <= len(words) <= 3 and all(len(word) >= 2 and word.isalpha() for word in words):
                            print(f"👤 Found Indonesian name (fallback): {name}")
                            return name
        
        print("⚠️  Could not extract name from ninjaname.net, using fallback...")
        
    except Exception as e:
        print(f"❌ Error getting Indonesian name: {e}")
    
    # Fallback Indonesian names
    first_names = ["Agus", "Budi", "Citra", "Dewi", "Eko", "Fitri", "Gita", "Hadi", "Indira", "Joko"]
    middle_names = ["", "Pratama", "Wijaya", "Sari", "Putra", "Putri", "Kusuma", "Utama", "Indah", "Candra"]
    last_names = ["Santoso", "Wibowo", "Prasetyo", "Handoko", "Sujanto", "Rahmawati", "Nugroho", "Setiawan", "Maharani", "Perdana"]
    
    first = random.choice(first_names)
    middle = random.choice(middle_names)
    last = random.choice(last_names)
    
    if middle:
        name = f"{first} {middle} {last}"
    else:
        name = f"{first} {last}"
    
    print(f"👤 Using fallback Indonesian name: {name}")
    return name

def create_email_from_name(name):
    """Create email from Indonesian name"""
    try:
        # Clean the name: remove extra spaces, convert to lowercase
        clean_name = re.sub(r'\s+', ' ', name.strip().lower())
        
        # Remove non-alphabetic characters except spaces
        clean_name = re.sub(r'[^a-z\s]', '', clean_name)
        
        # Join words together
        email_base = ''.join(clean_name.split())
        
        # Generate unique number (3 digits)
        unique_number = random.randint(100, 999)
        
        # Choose email provider
        providers = ["gmail.com", "outlook.com", "yahoo.com", "hotmail.com"]
        provider = random.choice(providers)
        
        email = f"{email_base}{unique_number}@{provider}"
        
        print(f"📧 Generated email from name: {email}")
        return email
        
    except Exception as e:
        print(f"❌ Error creating email from name: {e}")
        # Fallback
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"indonesianuser{random_suffix}@gmail.com"

def save_account_to_list(email, password, name):
    """Save account to sciteaccount.txt in email|password format"""
    try:
        # Append to sciteaccount.txt file
        with open("sciteaccount.txt", "a", encoding="utf-8") as f:
            f.write(f"{email}|{password}\n")
        
        print(f"✅ Account saved to sciteaccount.txt: {email}")
        
    except Exception as e:
        print(f"⚠️  Error saving to sciteaccount.txt: {e}")

def create_scite_account():
    """Create a new Scite.ai account"""
    print("\n🤖 Starting account creation...")
    
    # Get Indonesian name and create matching email
    indonesian_name = get_indonesian_name()
    matching_email = create_email_from_name(indonesian_name)
    custom_password = "Jawkills123@!"
    
    user_data = {
        "email": matching_email,
        "password": custom_password,
        "name": indonesian_name
    }
    
    print(f"📧 Email: {user_data['email']}")
    print(f"🔐 Password: {user_data['password']}")
    print(f"👤 Name: {user_data['name']}")
    
    # Setup session with proper headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'Origin': 'https://scite.ai',
        'Referer': 'https://scite.ai/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    })
    
    try:
        print("\n🚀 Sending signup request...")
        response = session.post(SIGNUP_ENDPOINT, json=user_data, timeout=15)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 201:
            print("🎉 ACCOUNT CREATED SUCCESSFULLY!")
            
            try:
                user_info = response.json()
                print(f"\n✅ Account Details:")
                print(f"   Name: {user_info.get('name', 'N/A')}")
                print(f"   Email: {user_info.get('email', 'N/A')}")
                print(f"   Slug: {user_info.get('slug', 'N/A')}")
                print(f"   Email Verified: {user_info.get('emailVerified', False)}")
                print(f"   Plan: {user_info.get('subscription', {}).get('plan', 'N/A')}")
                print(f"   Profile URL: https://scite.ai/users/{user_info.get('slug', 'N/A')}")
                
                # Save to main account list (email|password format)
                save_account_to_list(user_data['email'], user_data['password'], user_data['name'])
                
                return user_info
                
            except Exception as e:
                print(f"⚠️  Could not parse response JSON: {e}")
                print(f"Raw response: {response.text[:500]}...")
                return {"success": True, "raw_response": response.text}
                
        elif response.status_code == 400:
            print("❌ BAD REQUEST - Check data format")
            try:
                error_info = response.json()
                print(f"Error details: {error_info}")
            except:
                print(f"Error response: {response.text[:300]}...")
                
        elif response.status_code == 409:
            print("⚠️  ACCOUNT ALREADY EXISTS - Email might be taken")
            print("Trying with different email...")
            return create_scite_account()  # Retry with new email
            
        elif response.status_code == 422:
            print("❌ VALIDATION ERROR")
            try:
                error_info = response.json()
                print(f"Validation errors: {error_info}")
            except:
                print(f"Error response: {response.text[:300]}...")
                
        else:
            print(f"❌ UNEXPECTED ERROR: {response.status_code}")
            print(f"Response: {response.text[:300]}...")
            
    except requests.exceptions.Timeout:
        print("⏱️  Request timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("🔌 Connection error")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False
    
    return False

def create_multiple_accounts(count=1):
    """Create multiple Scite.ai accounts"""
    print(f"\n🔄 Creating {count} account(s)...")
    
    successful_accounts = []
    
    for i in range(count):
        print(f"\n--- Account {i+1}/{count} ---")
        
        result = create_scite_account()
        if result:
            successful_accounts.append(result)
            print(f"✅ Account {i+1} created successfully!")
        else:
            print(f"❌ Failed to create account {i+1}")
        
        # Wait between accounts to be respectful
        if i < count - 1:
            print("⏳ Waiting 3 seconds before next account...")
            time.sleep(3)
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"Successfully created: {len(successful_accounts)}/{count} accounts")
    
    # Show summary of created accounts
    if successful_accounts:
        print(f"\n📋 CREATED ACCOUNTS SUMMARY:")
        for i, account in enumerate(successful_accounts, 1):
            if isinstance(account, dict) and 'email' in account:
                print(f"   {i}. {account.get('email', 'N/A')} - {account.get('slug', 'N/A')}")
            else:
                print(f"   {i}. Account created successfully")
    
    return len(successful_accounts)

# Main execution
if __name__ == "__main__":
    print("🎯 Scite.ai Account Creation Bot Ready!")
    print(" Using password: Jawkills123@!")
    print("📝 All accounts will be saved to: sciteaccount.txt (email|password format)")
    
    # Ask how many accounts to create
    try:
        num_accounts = int(input("\nHow many accounts do you want to create? (1-5): ") or "1")
        num_accounts = max(1, min(5, num_accounts))  # Limit between 1-5
    except:
        num_accounts = 1
    
    print(f"\n🚀 Creating {num_accounts} account(s)...")
    
    start_time = time.time()
    success_count = create_multiple_accounts(num_accounts)
    end_time = time.time()
    
    print(f"\n⏱️  Total time: {end_time - start_time:.2f} seconds")
    print(f"🎉 Successfully created {success_count} account(s)!")
    
    if success_count > 0:
        print(f"\n📝 All accounts saved to: sciteaccount.txt")
    
    print("\n" + "="*50)
    print("✅ Bot execution completed!")
