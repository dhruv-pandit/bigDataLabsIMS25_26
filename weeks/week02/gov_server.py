#!/usr/bin/env python3
"""
Amianta Government Financial Services Server

This server is designed to simulate a compromised system for a cybersecurity
challenge. It features:
- In-memory file generation to avoid leaving traces on disk.
- A legitimate-looking process name and PID file for realistic discovery.
- Basic authentication with a randomly generated password.
- A hidden directory (.secret) containing sensitive, "corrupt" files.
- A self-destructing message that acts as a primary clue to the hidden directory.
- Plain-text directory listings for easy terminal interaction.
- A restructured directory tree that hides the sensitive files behind multiple layers.
"""

# The 'setproctitle' library is used to change the process name for realism.
# This makes 'amianta-financial-services' appear in process listings (e.g., 'ps aux').
try:
    import setproctitle
    setproctitle.setproctitle("amianta-financial-services")
except ImportError:
    # This ensures the script still runs if the library isn't installed.
    pass

from http.server import SimpleHTTPRequestHandler, HTTPServer
import random
import string
from datetime import datetime, timedelta
import os
import threading
import time

# --- Configuration Section ---
# This section defines the server's basic, dynamic settings.
# The password and port are randomized on each run to make the challenge repeatable.

# Generates a random 3-character password. This is used for basic authentication.
PASSWORD = "".join(random.choices(string.ascii_lowercase + string.digits, k=3))
# Assigns a random port number from the unprivileged range (1024-65535).
PORT = random.randint(1024, 65535)

# Write a PID (Process ID) file in a temporary directory.
# This provides a realistic way for an attacker to find the process on the system.
with open("/tmp/amianta-financial-services.pid", "w") as f:
    f.write(str(os.getpid()))

# --- File Number Generation ---
# These variables are now in the global scope so they can be accessed by all methods.
TOTAL_FILES = 250_000
CORRUPT_FILES = random.randint(500, 2000)
LEGIT_FILES = TOTAL_FILES - CORRUPT_FILES

# --- File Content Data ---
# These lists are used to generate the content for the different file types,
# giving them a sense of realism and variety.

# Lists for generating legitimate financial records.
GOV_DEPTS = ["health", "education", "transport", "justice", "defense", "agriculture", "energy", "finance", "foreign_affairs", "internal_security", "infrastructure"]
LEGIT_RECEIVERS = [
    "national_bank", "state_contractor_1", "state_contractor_2", "state_contractor_3",
    "municipal_service", "public_utility", "government_supplier", "civil_service_fund",
    "amianta_university_system", "national_research_lab", "public_works_commission", "state_hospital_network"
]
LEGIT_PURPOSES = [
    "salary payment", "office supplies", "equipment maintenance", "infrastructure contract",
    "public service grant", "utility payment", "professional services", "training program",
    "public-sector payroll", "research and development", "infrastructure upkeep", "social welfare funding"
]

# Lists for generating corrupt financial records. These names and purposes are
# designed to look suspicious and hint at illicit activities.
CORRUPT_RECEIVERS = [
    "cayman_account_1", "cayman_account_2", "swiss_bank_4567", "luxembourg_trust_789",
    "panama_corp_1", "panama_corp_2", "bermuda_holding", "bahamas_trust",
    "global_consulting_ltd", "international_services_inc", "strategic_partners_llc",
    "transatlantic_ventures", "pacific_assets_corp", "european_investments",
    "lobbyist_association", "political_consultant_1", "political_consultant_2",
    "former_official_1", "former_official_2", "family_member_1", "family_member_2",
    "urban_development_initiative", "sustainable_growth_foundation",
    "public-private_partnership", "economic_stimulus_fund",
    "offshore_investment_group", "shadow_company_x", "private_equity_fund_z",
    "sovereign_wealth_front", "international_foundations_group"
]

CORRUPT_PURPOSES = [
    "consulting fee", "advisory services", "facilitation payment", "processing fee",
    "expedited service", "special project", "confidential agreement", "strategic partnership",
    "retainer for special counsel", "undisclosed services", "private sector cooperation",
    "discretionary allocation", "security consultation", "reimbursement of travel expenses",
    "classified R&D project funding", "undocumented asset acquisition", "political influence campaign expenses",
    "special liaison office contingency fund", "national security discretionary spending"
]

# --- Server Handler Class ---
# This class defines how the server responds to HTTP requests.

class AmiantaHandler(SimpleHTTPRequestHandler):
    # 'filesystem' is an in-memory dictionary that acts as the server's file system.
    # Keys are file paths (e.g., "/confidential_tip.txt"), and values are the file contents.
    filesystem = {}
    # 'deletion_timer' tracks files that are set to self-destruct.
    # This prevents the timer from being started multiple times for the same file.
    deletion_timer = {}

    @classmethod
    def generate_filesystem(cls):
        """Generates all files and directory listings in memory."""
        cls._generate_files("legit", LEGIT_FILES)

        cls._generate_files("corrupt", CORRUPT_FILES)

        cls._generate_directory_listings(LEGIT_FILES, CORRUPT_FILES)
    
    @classmethod
    def _generate_files(cls, file_type, count):
        """A generic method to generate a specified number of files of a given type."""
        for i in range(count):
            if file_type == "legit":
                dept = random.choice(GOV_DEPTS)
                receiver = random.choice(LEGIT_RECEIVERS)
                purpose = random.choice(LEGIT_PURPOSES)
                amount = random.randint(1_000, 500_000)
                date = (datetime.now() - timedelta(days=random.randint(1, 1095))).strftime("%Y-%m-%d")
                reference = f"GOV-{dept[:3].upper()}-{random.randint(100000, 999999)}"

                extra_details = random.choice([
                    "", f"\n\nContract ID: {random.randint(1000, 9999)}",
                    f"\n\nApproved by: {random.choice(['Minister', 'Director', 'Committee'])} of {dept.capitalize()} Department",
                    f"\n\nPayment terms: Net 30, verified by internal audit team.",
                    f"\n\nFor public record. Reference: {random.randint(100000, 999999)}-{random.randint(100, 999)}"
                ])

                cls.filesystem[f"/transactions/records/gov_{i:06d}.txt"] = f"""Government of Amianta
                    Transaction Record
                    ===================
                    Date: {date}
                    From: {dept.capitalize()} Department (GOV-{dept[:3].upper()})
                    To: {receiver.replace("_", " ").title()}
                    Amount: ${amount:,}
                    Purpose: {purpose}
                    Reference: {reference}
                    Status: Processed
                    {extra_details}""".encode("utf-8")
            
            elif file_type == "corrupt":
                receiver = random.choice(CORRUPT_RECEIVERS)
                purpose = random.choice(CORRUPT_PURPOSES)
                amount = random.randint(1_000_000, 50_000_000)
                date = (datetime.now() - timedelta(days=random.randint(1, 1095))).strftime("%Y-%m-%d")
                reference = f"SPECIAL-{random.randint(1000, 9999)}"

                narrative = random.choice([
                    "This payment is for special, highly classified services. Discretion is paramount.",
                    "Funds transferred to Project VANGUARD. No paper trail should exist.",
                    "Discretionary funding for a black ops mission. Refer to code-word 'Blackbird' only.",
                    "As agreed, payment for offshore consultancy. Keep this file off the public network.",
                    "Reimbursement for undisclosed expenses related to the foreign liaison office."
                ])

                cls.filesystem[f"/transactions/.secret/project_phoenix_{i:04d}.txt"] = f"""CONFIDENTIAL TRANSACTION RECORD
                    =================================
                    Date: {date}
                    From: The Master's Office
                    To: {receiver.replace("_", " ").title()}
                    Amount: ${amount:,}
                    Purpose: {purpose}
                    Reference: {reference}

                    Narrative:
                    {narrative}

                    Notes:
                    - Do not include in public records
                    - Process through offshore account if possible
                    - Contact: private@amianta.gov
                    - Authorization: Minister's private seal required
                    """.encode("utf-8")

        # Add the new "smoking gun" file to the root. This is the primary clue.
        if file_type == "legit":
            cls.filesystem["/confidential_tip.txt"] = """
FROM: Anonyma C.
TO: Financial Services Staff
SUBJECT: URGENT: Ledger Discrepancy

This message is time-sensitive and will self-destruct in 10 minutes.

I've discovered a major discrepancy in the public-facing ledger.
I believe a number of transactions are being routed to a location
that is not listed in the standard directories.

It's a very specific **secret** folder, separate from the main
records. You won't find it linked anywhere. These are sensitive files
that you must locate and review immediately. There's something
very strange with the figures.

Do not discuss this with anyone.
Proceed with extreme caution.
""".encode("utf-8")

    @staticmethod
    def _generate_text_listing(files, path, footer=""):
        """Generates a plain text directory listing formatted for a terminal."""
        num_total = len(files)
        num_shown = min(10, num_total)
        remaining = num_total - num_shown
        
        listing = f"Directory listing for {path}\n"
        if num_total > 0:
            listing += f"Total files: {num_total}\n"
        listing += "-" * 50 + "\n"
        
        for f in files[:num_shown]:
            listing += f"{f}\n"

        if remaining > 0:
            listing += f"\n... {remaining} more files not shown.\n"
        
        if footer:
            listing += f"\n{footer}\n"
        
        return listing.encode("utf-8")

    @classmethod
    def _generate_directory_listings(cls, LEGIT_FILES, CORRUPT_FILES):
        """Generates all plain text directory listings."""
        
        # Root directory listing: only shows 'transactions/' and the tip message.
        root_files = ["transactions/", "confidential_tip.txt"]
        
        listing = f"Directory listing for /\n\n"
        listing += "-" * 50 + "\n"
        for f in root_files:
            listing += f"{f}\n"

        cls.filesystem["/"] = listing.encode("utf-8")
        
        # Transactions directory listing (of subfolders with file counts)
        # This is the section to modify
        transactions_dirs = [
            "records/"
        ]
        
        listing = f"Directory listing for /transactions/\n\n"
        listing += f"Total subdirectories: {len(transactions_dirs)+1}\n"
        listing += "-" * 50 + "\n"
        for dir_name in transactions_dirs:
            listing += f"{dir_name}\n"
        
        cls.filesystem["/transactions/"] = listing.encode("utf-8")
        
        # Listings for the subdirectories.
        all_legit_files = [f"gov_{i:06d}.txt" for i in range(LEGIT_FILES)]
        cls.filesystem["/transactions/records/"] = AmiantaHandler._generate_text_listing(
            all_legit_files, "/transactions/records/"
        )
        
        all_corrupt_files = [f"project_phoenix_{i:04d}.txt" for i in range(CORRUPT_FILES)]
        cls.filesystem["/transactions/.secret/"] = AmiantaHandler._generate_text_listing(
            all_corrupt_files, "/transactions/.secret/",
            "WARNING: Authorized Personnel Only"
        )
    
    def check_auth(self):
        """Handles basic authentication by checking the Authorization header against the password."""
        auth = self.headers.get("Authorization", "")
        if auth != PASSWORD:
            self.send_response(401)
            self.send_header("WWW-Authenticate", "Basic realm=\"Amianta Government\"")
            self.end_headers()
            self.wfile.write(b"401 Unauthorized: Password required")
            return False
        return True

    def do_GET(self):
        """Handles HTTP GET requests by serving the correct file or directory listing."""
        if not self.check_auth():
            return

        # Handle path normalization
        path = self.path
        if not path.endswith("/"):
            if path in self.filesystem:
                content = self.filesystem[path]
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                path += "/"

        if path == "/confidential_tip.txt":
            if path in self.filesystem and path not in self.deletion_timer:
                print("Confidential tip accessed. Initiating self-destruct sequence.")
                def delete_file():
                    time.sleep(600)
                    if path in self.filesystem:
                        print(f"Confidential tip deleted at {datetime.now()}.")
                        del self.filesystem[path]
                        AmiantaHandler._generate_directory_listings(LEGIT_FILES, CORRUPT_FILES)
                
                deletion_thread = threading.Thread(target=delete_file)
                deletion_thread.daemon = True
                deletion_thread.start()
                self.deletion_timer[path] = deletion_thread

        if path in self.filesystem:
            content = self.filesystem[path]
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404)

# Generate all files when starting the server
AmiantaHandler.generate_filesystem()

HTTPServer(("localhost", PORT), AmiantaHandler).serve_forever()